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
from Utils.db import insert_query, update_query, select_one_query, update_history_tracker, select_count_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)

base_url = "http://hcbombayatgoa.nic.in/"


def request_pdf(case_id, court_name, val, headers):
    try:
        payload = 'submit1=Get&txtlist=' + str(int(val))
        response = requests.request("POST", base_url + 'jq_case.asp', data=payload, headers=headers, proxies=proxy_dict)
        if response.status_code == 200:
            # res = response.text

            # if "<b>error occurred - </b>" in res.lower():
            #     logging.error("No data for: " + str(case_id))
            #     return "NULL"

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


def parse_html(html_str, court_name, headers):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        select_soup = BeautifulSoup(str(soup.find_all('select', {'id': 'txtlist'})[0]), "html.parser")
        tr_list = select_soup.find_all('option')

        for tr in tr_list:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            insert_check = False
            pdf_value = tr['value']

            res = BeautifulSoup(str(tr['onmouseover']).replace("return overlib('", "").replace("')", ""), "html.parser")
            [s.extract() for s in res('font')]
            res = str(res).replace('\n', '').strip().split('<br/>')

            petitioner = escape_string(res[0])
            respondent = escape_string(res[1])
            judge = escape_string(res[2])
            judgment_date = escape_string(res[3])
            mix_data = str(res[4]).replace("', CAPTION, '", '')

            reportable = mix_data[0:2]
            case_no = escape_string(mix_data[3:])

            if reportable == 'No':
                continue

            if select_count_query(str(court_name), str(case_no)):
                insert_check = True

            if case_no != "NULL" and insert_check:
                pdf_data = escape_string(request_pdf(case_no, court_name, pdf_value, headers))

                sql_query = "INSERT INTO " + str(court_name) + " (case_no, petitioner, respondent, judgment_date, " \
                                                               "judge, pdf_file, pdf_filename, reportable) VALUE ('" + \
                            case_no + "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + \
                            judge + "', '" + pdf_value + "', '" + court_name + "_" + slugify(case_no) + ".pdf', '" + \
                            reportable + "')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def request_data(court_name, start_date, end_date_):
    try:
        url = base_url + "date_JQ.asp"
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

            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=1)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime(end_date_, "%d-%m-%Y") + datetime.timedelta(days=1) < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "txtday=" + str(start_date[0:2]).lstrip('0') + \
                      "&txtmonth=" + str(start_date[3:5]).lstrip('0') +  \
                      "&txtyear=" + str(start_date[-4:])

            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            if "no judgement found for your search" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not parse_html(res, court_name, headers):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("Goa")
    return request_data(court_name, start_date, end_date)
