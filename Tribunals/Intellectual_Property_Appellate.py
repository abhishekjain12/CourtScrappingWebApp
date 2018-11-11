import datetime
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
base_url = "http://www.ipabindia.org/aOrders.aspx"


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


def details_parse(url, appeal_no, court_name):
    date_of_order = 'NULL'
    pdf_file = 'NULL'
    order_type = 'NULL'

    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if res is None:
                logging.error("No data for: " + str(url))
                return "NULL"

            full_details_parse(res, appeal_no, court_name)

            soup = BeautifulSoup(res, "html.parser")
            table_list = soup.find_all('section', {'class': None})
            table_soup = BeautifulSoup(str(table_list), "html.parser")
            td_list = table_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    order_type = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 2:
                    date_of_order = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 6:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    if a_tag is not None:
                        pdf_file = a_tag.get('href')

        else:
            logging.error("Failed to get text file for: " + str(url))

        return date_of_order, pdf_file, order_type

    except Exception as e:
        logging.error("Failed to parse the details html: %s", e)
        return date_of_order, pdf_file, order_type


def full_details_parse(res, appeal_no, court_name):
    try:
        filed_on = 'NULL'
        assessment_year = 'NULL'
        bench_allotted = 'NULL'
        case_status = 'NULL'
        date_of_first_hearing = 'NULL'
        date_of_last_hearing = 'NULL'
        date_of_next_hearing = 'NULL'
        date_of_final_hearing = 'NULL'
        date_of_tribunal_order = 'NULL'
        date_of_pronouncement = 'NULL'
        order_result = 'NULL'

        soup = BeautifulSoup(res, "html.parser")
        table_list = soup.find_all('table', {'class': 'table table-striped table-bordered manage-efects'})
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            if tr_count != 5:
                continue

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 2:
                    filed_on = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 3:
                    assessment_year = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 4:
                    bench_allotted = escape_string(str(td.text).strip().replace("\n", ""))
                if i == 5:
                    case_status = escape_string(str(td.text).strip().replace("\n", ""))

        soup = BeautifulSoup(res, "html.parser")
        table_list = soup.find_all('section', {'id': 'panel2-3'})
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            if tr_count == 1:
                continue

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            if tr_count == 2:
                i = 0
                for td in td_list:
                    i += 1
                    if i == 1:
                        date_of_first_hearing = escape_string(str(td.text).strip().replace("\n", ""))
                    if i == 2:
                        date_of_tribunal_order = escape_string(str(td.text).strip().replace("\n", ""))

            if tr_count == 3:
                i = 0
                for td in td_list:
                    i += 1
                    if i == 1:
                        date_of_last_hearing = escape_string(str(td.text).strip().replace("\n", ""))
                    if i == 2:
                        date_of_pronouncement = escape_string(str(td.text).strip().replace("\n", ""))

            if tr_count == 4:
                i = 0
                for td in td_list:
                    i += 1
                    if i == 1:
                        date_of_next_hearing = escape_string(str(td.text).strip().replace("\n", ""))
                    if i == 2:
                        order_result = escape_string(str(td.text).strip().replace("\n", ""))

            if tr_count == 5:
                i = 0
                for td in td_list:
                    i += 1
                    if i == 1:
                        date_of_final_hearing = escape_string(str(td.text).strip().replace("\n", ""))

        update_query("UPDATE " + court_name + " SET filed_on = '" + str(filed_on) + "', assessment_year = '" +
                     str(assessment_year) + "', bench_allotted = '" + str(bench_allotted) + "', case_status = '" +
                     str(case_status) + "', date_of_first_hearing = '" +
                     str(date_of_first_hearing) + "', date_of_last_hearing = '" + str(date_of_last_hearing) +
                     "', date_of_next_hearing = '" + str(date_of_next_hearing) + "', date_of_final_hearing = '" +
                     str(date_of_final_hearing) + "', date_of_tribunal_order = '" + str(date_of_tribunal_order) +
                     "', date_of_pronouncement = '" + str(date_of_pronouncement) + "', order_result = '" +
                     str(order_result) + "' WHERE appeal_no = '" + str(appeal_no) + "'")

    except Exception as e:
        logging.error("Failed to parse the details html: %s", e)


def parse_html(html_str, court_name):
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
            order_type = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    appeal_no = escape_string(str(td.text).strip().replace("\n", ""))

                if i == 2:
                    filed_by = escape_string(str(td.text).strip().replace('\n', ''))

                if i == 3:
                    appellant = escape_string(str(td.text).strip().replace('\n', ''))

                if i == 4:
                    respondent = escape_string(str(td.text).strip().replace('\n', ''))

                if i == 5:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    details_url = a_tag.get('href')
                    date_of_order, pdf_file, order_type = details_parse(details_url, appeal_no, court_name)

                    if select_count_query_other(str(court_name), 'appeal_no', str(appeal_no), 'date_of_order',
                                                date_of_order):
                        insert_check = True

                        pdf_data = escape_string(str(request_pdf(pdf_file, appeal_no, court_name)).replace("'", ""))

            if appeal_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (appeal_no, appellant, respondent, filed_by, " \
                                                               "bench_code, pdf_filename ) VALUE ('" + appeal_no + \
                            "', '" + appellant + "', '" + respondent + "', '" + filed_by + "', '" + court_name + \
                            "_" + slugify(appeal_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "', date_of_order ='" +
                             date_of_order + "', pdf_file = '" + pdf_file + "', order_type = '" + order_type +
                             "' WHERE appeal_no = '" + str(appeal_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, start_date, end_date_):
    try:
        url = base_url + "/tribunalorders"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }
        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=1)
                        ).strftime("%d/%m/%Y")

            if datetime.datetime.strptime(str(end_date_), "%d/%m/%Y") + datetime.timedelta(days=1) < \
                    datetime.datetime.strptime(str(end_date), "%d/%m/%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "appeal_type=" \
                      "&hearingdate=" \
                      "&pronouncementdate=" \
                      "&orderdate=" + str(start_date) + \
                      "&member=" \
                      "&assesseename="

            response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxy_dict)
            res = response.text

            if res is None:
                logging.error("NO data Found.")
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not parse_html(res, court_name):
                logging.error("Failed to parse data")

            start_date = end_date

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data ")
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("Intellectual_Property_Appellate.py")
    return request_data(court_name, start_date, end_date)
