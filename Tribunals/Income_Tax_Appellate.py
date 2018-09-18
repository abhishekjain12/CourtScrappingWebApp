import os
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
from Utils.db import insert_query, update_query, select_one_query, update_history_tracker, select_count_query_other
from Utils.my_proxy import proxy_dict


module_directory = os.path.dirname(__file__)
base_url = "https://www.itat.gov.in/judicial"


def request_pdf(url, case_id, court_name):
    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if res is None:
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


def details_parse(url):
    date_of_order = 'NULL'
    pdf_file = 'NULL'

    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if res is None:
                logging.error("No data for: " + str(url))
                return "NULL"

            soup = BeautifulSoup(res, "html.parser")
            table_list = soup.find_all('section', {'class': None})
            table_soup = BeautifulSoup(str(table_list), "html.parser")
            td_list = table_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 2:
                    date_of_order = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 6:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = a_tag.get('href')

        else:
            logging.error("Failed to get text file for: " + str(url))

        return date_of_order, pdf_file

    except Exception as e:
        logging.error("Failed to parse the details html: %s", e)
        return date_of_order, pdf_file


def parse_html(html_str, court_name, bench):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_list = soup.find_all('table', {'style': 'width:100%; margin-top: 10px; font-size: 12px;'})
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count == 1:
                continue

            appeal_no = "NULL"
            appellant = "NULL"
            respondent = "NULL"
            date_of_order = "NULL"
            filed_by = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    appeal_no = escape_string(str(td.text).strip().replace("\n", ""))

                if select_count_query_other(str(court_name), 'appeal_no', str(appeal_no)):
                    insert_check = True

                    if i == 2:
                        filed_by = escape_string(str(td.text).strip().replace('\n', ''))

                    if i == 3:
                        appellant = escape_string(str(td.text).strip().replace('\n', ''))

                    if i == 4:
                        respondent = escape_string(str(td.text).strip().replace('\n', ''))

                    if i == 5:
                        a_tag = BeautifulSoup(str(td), "html.parser").a
                        details_url = a_tag.get('href')
                        date_of_order, pdf_file = details_parse(details_url)

                        pdf_data = escape_string(request_pdf(pdf_file, appeal_no, court_name))

            if appeal_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (appeal_no, appellant, respondent, date_of_order, " \
                                                               "filed_by, pdf_file, bench_code, pdf_filename) VALUE"\
                                                               " ('" + appeal_no + "', '" + appellant + "', '" + \
                            respondent + "', '" + date_of_order + "', '" + filed_by + "', '" + pdf_file + "', " + \
                            str(bench) + ", '" + court_name + "_" + slugify(appeal_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE appeal_no = '" +
                             str(appeal_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, bench):
    try:
        url = base_url + "/tribunalorders"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
        if emergency_exit['emergency_exit'] == 1:
            update_history_tracker(court_name)
            return True

        update_query("UPDATE Tracker SET Start_Date = '0', End_Date = '0' WHERE Name = '" + str(court_name) + "'")

        payload = "bench=" + str(bench) + \
                  "&appeal_type=&hearingdate=&pronouncementdate=&orderdate=&member=&assesseename="

        response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxy_dict)
        res = response.text

        if res is None:
            logging.error("NO data Found.")
            update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                         str(court_name) + "'")

        if not parse_html(res, court_name, bench):
            logging.error("Failed to parse data from bench: " + str(bench))

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from bench: " + str(bench))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, bench):
    logs.initialize_logger("Income_Tax_Appellate")
    return request_data(court_name, bench)
