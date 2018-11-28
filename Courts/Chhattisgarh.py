import datetime

import requests
import os
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

from Courts import judis
from Utils import logs
from Utils.db import insert_query, update_query, update_history_tracker, select_count_query, \
    select_one_local_query, update_local_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://highcourt.cg.gov.in/Afr/"


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
        ul = soup.find_all('ul')[0]
        ul_soup = BeautifulSoup(str(ul), "html.parser")
        li_list = ul_soup.find_all('li')

        # p_list = ul_soup.find_all('p')
        # p_list = [x for x in p_list if "<p><font" not in str(x)]
        # print(p_list)
        # return

        for li in li_list:
            emergency_exit = select_one_local_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name +
                                                    "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            a = BeautifulSoup(str(li), "html.parser").a
            a_link = a.get('href')

            case_no = str(a_link[a_link.rfind("/")+1:]).replace('.pdf', '')
            judgment_date = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            # insert_check = False

            # if select_count_query(str(court_name), str(case_no), 'judgment_date', judgment_date):
            #     insert_check = True

            judgment_date = escape_string(case_no[-10:].replace('(', '').replace(')', ''))
            pdf_data = escape_string(request_pdf(base_url + a_link, case_no, court_name))
            pdf_file = escape_string(base_url + a_link)

            # if case_no != "NULL" and insert_check:
            if case_no != "NULL":
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, judgment_date, pdf_file, pdf_filename) " \
                                                               "VALUE ('" + case_no + "', '" + judgment_date + "', '" \
                            + pdf_file + "', '" + court_name + "_" + slugify(case_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET text_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_local_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        update_local_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, start_date, end_date_):
    try:
        if int(start_date) < 2012:
            update_local_query("UPDATE Tracker SET status = 'IN_NO_DATA_FOUND', emergency_exit=true WHERE Name = '" +
                               str(court_name) + "'")
            if int(end_date_) < 2012:
                update_history_tracker(court_name)
                return True

        for year_ in range(int(start_date), int(end_date_) + 1):
            emergency_exit = select_one_local_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name +
                                                    "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            if int(year_) == 2018:
                year_ = ''

            url = base_url + "DecisionsHeadline" + str(year_) + ".html"

            update_local_query("UPDATE Tracker SET Start_Date = '" + str(year_) + "', End_Date = '" + str(end_date_) +
                               "' WHERE Name = '" + str(court_name) + "'")

            response = requests.request("GET", url, proxies=proxy_dict)
            res = response.text

            if "file or directory not found" in res.lower():
                logging.error("NO data Found for start date: " + str(year_))

                update_local_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                                   str(court_name) + "'")

                continue

            if not parse_html(res, court_name):
                logging.error("Failed to parse data from date: " + str(year_))

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("Chhattisgarh")

    if int((datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime('%Y')) < 2012:
        return judis.main(court_name, 1, start_date, end_date)
    else:
        start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime('%Y')
        end_date = (datetime.datetime.strptime(str(end_date), "%d/%m/%Y")).strftime('%Y')
        return request_data(court_name, start_date, end_date)


# fw = open("../Data_Files/Html_Files/test.html", "r")
# parse_html(fw.read(), "Chhattisgarh")
