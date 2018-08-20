import requests
import datetime
import os
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
logs.initialize_logger("SC")

court_name = "SupremeCourt"
base_url = "https://www.supremecourtofindia.nic.in/"


def request_pdf(url, case_id):
    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if "no data found" in res.lower():
                logging.error("No data for: " + str(case_id))
                return "NULL"

            file_path = module_directory + "/../PDF_Files/SC_" + str(court_name) + "_" + str(slugify(case_id)) + ".pdf"
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

            file_path = module_directory + "/../Text_Files/SC_" + str(court_name) + "_" + str(slugify(case_id)) + ".txt"
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
        soup = BeautifulSoup(html_str)
        tr_list = soup.find_all('tr')

        case_no = "NULL"
        diary_number = "NULL"
        petitioner = "NULL"
        respondent = "NULL"
        petitioner_advocate = "NULL"
        respondent_advocate = "NULL"
        judgment_date = "NULL"
        judge_name = "NULL"
        bench = "NULL"
        pdf_data = "NULL"
        pdf_file = "NULL"

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            tr_soup = BeautifulSoup(str(tr))
            td_list = tr_soup.find_all('td')

            if tr_count == 1:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        diary_number = escape_string(str(td.decode_contents()))

            if tr_count == 2:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        case_no = escape_string(str(td.decode_contents()))
                    if td_count == 3:
                        judgment_date = escape_string(str(td.a.string))
                        a_link = BeautifulSoup(str(td)).a.get('href')
                        pdf_data = escape_string(request_pdf(base_url + a_link, case_no))
                        pdf_file = base_url + a_link

            if tr_count == 3:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        petitioner = escape_string(str(td.decode_contents()))

            if tr_count == 4:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        respondent = escape_string(str(td.decode_contents()))

            if tr_count == 5:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        petitioner_advocate = escape_string(str(td.decode_contents()))

            if tr_count == 6:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        respondent_advocate = escape_string(str(td.decode_contents()))

            if tr_count == 7:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        bench = escape_string(str(td.decode_contents()))

            if tr_count == 8:
                td_count = 0
                for td in td_list:
                    td_count += 1
                    if td_count == 2:
                        judge_name = escape_string(str(td.decode_contents()))

                sql_query = "INSERT INTO " + str(court_name) + \
                            " (diary_number, case_no, petitioner, respondent, petitioner_advocate, " \
                            "respondent_advocate, judgment_date, bench, judge_name, pdf_data, pdf_file) VALUE " \
                            "('" + diary_number + "', '" + case_no + "', '" + petitioner + "', '" + respondent + \
                            "', '" + petitioner_advocate + "', '" + respondent_advocate + "', '" + judgment_date + \
                            "', '" + bench + "', '" + judge_name + "', '" + pdf_data + "', '" + pdf_file + "')"
                insert_query(sql_query)

                sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

            if tr_count == 9:
                tr_count = 0
                case_no = "NULL"
                diary_number = "NULL"
                petitioner = "NULL"
                respondent = "NULL"
                petitioner_advocate = "NULL"
                respondent_advocate = "NULL"
                judgment_date = "NULL"
                judge_name = "NULL"
                bench = "NULL"
                pdf_data = "NULL"
                pdf_file = "NULL"

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def request_data():
    start_date = None
    try:
        url = base_url + 'php/getJBJ.php'

        headers = {
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Cache-Control': "no-cache"
        }

        start_date = "22-12-1990"

        i = 0
        while True:
            i += 1
            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=365)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime("31-12-2019", "%d-%m-%Y") < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("END date Exceed.")
                break

            sql_query = "UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) + \
                        "' WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

            payload = "jorrop=J" \
                      "&JBJfrom_date=" + str(start_date) + \
                      "&JBJto_date=" + str(end_date)

            response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxy_dict)

            res = response.text
            # print(res)

            if "no data found" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))

                sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                            str(court_name) + "'"
                update_query(sql_query)

                start_date = end_date
                continue

            fw = open(module_directory + "/../Html_Files/SC_" + str(court_name) + "_" +
                      str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
            fw.write(str(res))

            if not parse_html(res):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        shutil.make_archive(str(court_name) + "_HTML_FILES", 'zip', module_directory + "/../Html_Files")
        shutil.make_archive(str(court_name) + "_TEXT_FILES", 'zip', module_directory + "/../Text_Files")
        shutil.make_archive(str(court_name) + "_PDF_FILES", 'zip', module_directory + "/../PDF_Files")

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
