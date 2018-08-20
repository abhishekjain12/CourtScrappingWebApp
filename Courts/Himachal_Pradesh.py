import datetime
import os
import re
from math import ceil

import requests
import traceback
import logging
import shutil

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify
from Utils import logs
from Utils.db import insert_query, update_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
logs.initialize_logger("HCS")

court_name = "hp"
base_url = "http://164.100.138.228/casest/cis/"

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "PHPSESSID=32vi4meb8as03gul6l2l6usfa4",
    'Cache-Control': "no-cache"
    }


def request_pdf(url, case_id):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if "no data found" in res.lower():
                logging.error("No data for: " + str(case_id))
                return "NULL"

            file_path = module_directory + "/../PDF_Files/HCS_" + str(court_name) + "_" + str(slugify(case_id)) + ".pdf"
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

            file_path = module_directory + "/../Text_Files/HCS_" + str(court_name) + \
                        "_" + str(slugify(case_id)) + ".txt"
            fw = open(file_path, "w")
            fw.write(str(text_data))

            return str(text_data)
        else:
            logging.error("Failed to get text file for: " + str(case_id))
            return "NULL"

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(case_id) + ". Error: %s", e)
        return "NULL"


def parse_html(html_str):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_tag = soup.find_all('table')[1]

        table_soup = BeautifulSoup(str(table_tag), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
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

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    case_no = escape_string(str(td.decode_contents()))

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
                    pdf_data = escape_string(request_pdf(base_url + a_tag.get('href'), case_no))

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, judgment_date, coram, type, status, " \
                                                           "pdf_data, pdf_file) VALUE ('" + case_no + "', '" + \
                        judgment_date + "', '" + coram + "', '" + type_ + "', '" + status + "', '" + pdf_data + \
                        "', '" + pdf_file + "')"
            insert_query(sql_query)

            sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def offset_link(html_str, o_payload, start_date):
    url = base_url + "coram-reported-judgment.php"
    try:
        if not parse_html(html_str):
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

            payload = o_payload + "&start=" + str(next_num)
            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_offset_" +
                      str(start_date).replace("/", "-") + "_" + str(next_num) + ".html", "w")
            fw.write(str(res))

            if not parse_html(res):
                logging.error("Failed for url: " + str(next_num))
                return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data():
    start_date = None
    try:
        url = base_url + "coram-reported-judgment.php"
        start_date = "01-01-1950"

        i = 0
        while True:
            i += 1
            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=1)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime("31-08-2018", "%d-%m-%Y") < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            sql_query = "UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) + \
                        "' WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

            payload = "coram=0" \
                      "&ojtype=1" \
                      "&bench_type=0" \
                      "&reported=Y" \
                      "&startdate=" + str(start_date) + \
                      "&enddate=" + str(end_date) + \
                      "&coramqueryreported=0"

            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)

            res = response.text
            # print(res)

            if "NO ROWS" in res.upper():
                logging.error("NO data Found for start date: " + str(start_date))

                sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                            str(court_name) + "'"
                update_query(sql_query)

                start_date = end_date
                continue

            fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_" +
                      str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
            fw.write(str(res))

            if not offset_link(res, payload, start_date):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        shutil.make_archive(str(court_name) + "_HTML_FILES", 'zip', module_directory + "/../Html_Files")
        shutil.make_archive(str(court_name) + "_TEXT_FILES", 'zip', module_directory + "/../Text_Files")

        sql_query = "UPDATE Tracker SET status = 'IN_SUCCESS' WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)

        return "IN_SUCCESS"

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        sql_query = "UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" + \
                    str(court_name) + "'"
        update_query(sql_query)

        return "IN_FAILED"


print(request_data())
