import datetime
import os
import re
from math import ceil

import requests
import traceback
import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify
from Utils import logs
from Utils.db import insert_query, update_query, select_one_query, update_history_tracker, select_count_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://164.100.138.228/casest/cis/"


def request_pdf(url, case_id, court_name):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if "no data found" in res.lower():
                logging.error("No data for: " + str(case_id))
                return "NULL"

            file_path = module_directory + "/../Data_Files/PDF_Files/" + court_name + "_" + slugify(case_id) + ".pdf"
            fw = open(file_path, "wb")
            fw.write(response.content)

            text_data = ""

            pdf_manager = PDFResourceManager()
            string_io = StringIO()
            pdf_to_text = TextConverter(pdf_manager, string_io, codec='utf-8', laparams=LAParams())
            interpreter = PDFPageInterpreter(pdf_manager, pdf_to_text)
            for page in PDFPage.get_pages(open(file_path, 'rb')):
                interpreter.process_page(page)
                text_data = string_io.getvalue()

            file_path = module_directory + "/../Data_Files/Text_Files/" + court_name + "_" + slugify(case_id) + ".txt"
            fw = open(file_path, "w")
            fw.write(str(text_data))

            return str(text_data)
        else:
            logging.error("Failed to get text file for: " + str(case_id))
            return "NULL"

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(case_id) + ". Error: %s", e)
        return "NULL"


def parse_html(html_str, court_name):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_tag = soup.find_all('table')[1]

        table_soup = BeautifulSoup(str(table_tag), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count <= 2 or tr_count > 17:
                continue

            case_no = "NULL"
            judgment_date = "NULL"
            coram = "NULL"
            type_ = "NULL"
            status = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    case_no = escape_string(str(td.decode_contents()))

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

                    if i == 2:
                        coram = escape_string(str(td.decode_contents()))

                    if i == 3:
                        judgment_date = escape_string(str(td.decode_contents()))

                    if i == 5:
                        type_ = escape_string(str(td.decode_contents()))

                    if i == 6:
                        status = escape_string(str(td.decode_contents()))

                    if i == 4:
                        a_tag = BeautifulSoup(str(td), "html.parser").a
                        pdf_file = escape_string(base_url + a_tag.get('href'))
                        pdf_data = escape_string(request_pdf(base_url + a_tag.get('href'), case_no, court_name))

            if case_no != "NULL" and insert_check and case_no.find("DISCLAIMER") == -1:

                sql_query = "INSERT INTO " + str(court_name) + " (case_no, judgment_date, coram, type, status, " \
                                                               "pdf_file) VALUE ('" + case_no + "', '" + \
                            judgment_date + "', '" + coram + "', '" + type_ + "', '" + status + "', '" + pdf_file + "')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def offset_link(html_str, o_payload, court_name, headers):
    url = base_url + "coram-reported-judgment.php"
    try:
        if not parse_html(html_str, court_name):
            return False

        soup = BeautifulSoup(html_str, "html.parser")
        table_tag = soup.find_all('table')[1]
        table_soup = BeautifulSoup(str(table_tag), "html.parser")
        b_tag = table_soup.find_all('b')[0]
        total_records = int(re.findall('\d+', str(b_tag.decode_contents()))[-1])
        total_calls = ceil(total_records/15)

        next_num = 0
        for page_link in range(0, total_calls):
            next_num += 15

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                break

            payload = o_payload + "&start=" + str(next_num)
            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            if not parse_html(res, court_name):
                logging.error("Failed for url: " + str(next_num))
                return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data(court_name, headers, start_date, end_date_):
    try:
        url = base_url + "coram-reported-judgment.php"

        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=1)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime(str(end_date_), "%d-%m-%Y") + datetime.timedelta(days=1) < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "coram=0" \
                      "&ojtype=1" \
                      "&bench_type=0" \
                      "&reported=Y" \
                      "&startdate=" + str(start_date) + \
                      "&enddate=" + str(end_date) + \
                      "&coramqueryreported=0"

            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            if "NO ROWS" in res.upper():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not offset_link(res, payload, court_name, headers):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        update_query("UPDATE Tracker SET status = 'IN_SUCCESS', emergency_exit=true WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        update_query("UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("HIMACHAL")
    r = requests.request('GET', base_url + 'coram-reported-query.php', proxies=proxy_dict)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cookie': 'PHPSESSID=' + str(requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']),
        'Cache-Control': "no-cache",
    }
    return request_data(court_name, headers, start_date, end_date)
