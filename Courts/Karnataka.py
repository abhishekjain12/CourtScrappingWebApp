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
from Utils.db import insert_query, update_query, update_history_tracker, select_count_query, \
    select_one_local_query, update_local_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)

base_url = "http://judgmenthck.kar.nic.in"
headers = {
    'Cache-Control': "no-cache"
    }


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
        table_tag = soup.find_all('table', {'class': 'miscTable'})[0]

        table_soup = BeautifulSoup(str(table_tag), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:

            emergency_exit = select_one_local_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name +
                                                    "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count == 1:
                continue

            case_no = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            bench = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1

                if i == 1:
                    judgment_date = escape_string(str(td.decode_contents()))

                if i == 2:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    case_no = escape_string(str(a_tag.text).replace("\n", ""))

                    if select_count_query(str(court_name), str(case_no), 'judgment_date', judgment_date):
                        insert_check = True

                        new_url = base_url + a_tag.get('href')
                        response = requests.request('GET', new_url, headers=headers, proxies=proxy_dict)

                        new_soup = BeautifulSoup(str(response.text), "html.parser")
                        new_td_tag = new_soup.find_all('td', {'headers': 't1'})[0]
                        new_a_href = BeautifulSoup(str(new_td_tag), "html.parser").a.get('href')

                        pdf_file = escape_string(base_url + new_a_href)
                        pdf_data = escape_string(request_pdf(base_url + new_a_href, case_no, court_name))

                if i == 3:
                    judge_name = escape_string(str(td.text))

                if i == 4:
                    petitioner = escape_string(str(td.text))

                if i == 5:
                    respondent = escape_string(str(td.text))

                if i == 6:
                    bench = escape_string(str(td.text))

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + "(case_no, judgment_date, judge_name, petitioner, " \
                                                               "respondent, bench, pdf_file, pdf_filename) VALUE ('" +\
                            case_no + "', '" + judgment_date + "', '" + judge_name + "', '" + petitioner + "', '" + \
                            respondent + "', '" + bench + "', '" + pdf_file + "', '" + court_name + "_" + \
                            slugify(case_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_local_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_local_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def offset_link(html_str, url, querystring, court_name):
    try:
        if not parse_html(html_str, court_name):
            return False

        querystring['sort_by'] = "1"
        querystring['etal'] = "-1"

        soup = BeautifulSoup(html_str, "html.parser")
        div_tag = soup.find_all('div', {'class': 'browse_range'})[0]

        total_records = int(re.findall('\d+', str(div_tag.text))[-1])
        total_calls = ceil(total_records/200)

        next_num = 0
        for page_link in range(0, total_calls):
            next_num += 200

            emergency_exit = select_one_local_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name +
                                                    "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            querystring['offset'] = str(next_num)
            response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)
            res = response.text

            if not parse_html(res, court_name):
                logging.error("Failed for url: " + str(next_num))
                return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data_old(court_name, start_date, end_date):
    try:
        url = base_url + "/judgments/browse"

        update_local_query("UPDATE Tracker SET Start_Date = '" + start_date + "', End_Date = '" + end_date +
                           "' WHERE Name = '" + str(court_name) + "'")

        querystring = {"type": "reported", "value": "Reportable", "sort_by": "1", "order": "ASC", "rpp": "357",
                       "etal": "0", "submit_browse": "Update"}

        response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)
        res = response.text

        if "NO ROWS" in res.upper():
            update_local_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                               str(court_name) + "'")

        if not parse_html(res, court_name):
            logging.error("Failed to parse data old")

        update_local_query("UPDATE Tracker SET status = 'IN_SUCCESS', emergency_exit=true WHERE Name = '" +
                           str(court_name) + "'")
        update_history_tracker(court_name)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        update_local_query("UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" +
                           str(court_name) + "'")
        update_history_tracker(court_name)

        return False


def request_data(court_name, start_date, end_date_):
    try:
        url = base_url + "/judgmentsdsp/browse"

        update_local_query("UPDATE Tracker SET Start_Date = '" + start_date + "', End_Date = '" + end_date_ +
                           "' WHERE Name = '" + str(court_name) + "'")

        querystring = {"type": "reportable", "order": "ASC", "rpp": "200", "value": "Reportable"}

        response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)
        res = response.text

        if "NO ROWS" in res.upper():
            update_local_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                               str(court_name) + "'")

        if not offset_link(res, url, querystring, court_name):
            logging.error("Failed to parse data")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("KARNATAKA")

    if int(start_date) == 2014 or int(end_date) == 2014:
        request_data(court_name, '2014', '2014')
        request_data_old(court_name, '2014', '2014')

    if int(start_date) < 2014 < int(end_date):
        request_data_old(court_name, str(start_date), '2014')
        return request_data(court_name, '2014', str(end_date))
    elif int(start_date) > 2014:
        return request_data(court_name, str(start_date), str(end_date))
    elif int(end_date) < 2014:
        return request_data_old(court_name, str(start_date), str(end_date))
