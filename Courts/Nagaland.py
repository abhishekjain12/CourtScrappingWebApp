from datetime import datetime

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
from Utils import logs
from Utils.db import insert_query, update_query, update_history_tracker, select_one_query, select_count_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://kohimahighcourt.gov.in/"


def month_list_(dates):
    start, end = [datetime.strptime(_, "%m%Y") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    m_list = []
    for tot_m in range(total_months(start) - 1, total_months(end)):
        y, m = divmod(tot_m, 12)
        m_list.append(datetime(y, m + 1, 1).strftime("%m%Y"))
    return m_list


def request_pdf(url, case_id, court_name):
    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
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
        div = soup.find_all('div', {'id': 'CPHBody_PanelList'})[0]
        a_list_soup = BeautifulSoup(str(div), "html.parser")
        a_list = a_list_soup.find_all('a')

        a_list_unique = list(set(a_list))
        for a in a_list_unique:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            case_no = escape_string(str(str(a.text)[:-10]).replace("-", ""))
            judgment_date = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            if select_count_query(str(court_name), str(case_no)):
                insert_check = True

                judgment_date = escape_string(str(a.text)[-10:])

                a_link = a.get('href')
                pdf_data = escape_string(request_pdf(base_url + a_link, case_no, court_name))
                pdf_file = escape_string(base_url + a_link)

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, judgment_date, pdf_file) VALUE ('" \
                            + case_no + "', '" + judgment_date + "', '" + pdf_file + "')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, start_date, end_date_):
    try:
        if int(start_date[-4:]) < 2010:
            update_query("UPDATE Tracker SET status = 'IN_NO_DATA_FOUND', emergency_exit=true WHERE Name = '" +
                         str(court_name) + "'")
            if int(end_date_[-4:]) < 2010:
                update_history_tracker(court_name)
                return True

        for month_year in month_list_([str(start_date), str(end_date_)]):
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            data = {'ctl00$CPHBody$DropDownListYear': str(month_year[-4:]),
                    'ctl00$CPHBody$DropDownListMonth': str(month_year[:-4]).replace("0", ""),
                    'ctl00$CPHBody$TextBox1': '',
                    'ctl00$CPHBody$SM1': 'ctl00$CPHBody$SM1|ctl00$CPHBody$DropDownListMonth'
                    }

            with requests.Session() as s:
                page = s.get(base_url + 'judgement.aspx')
                soup = BeautifulSoup(page.content, "html.parser")

                data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
                data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
                data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

                update_query("UPDATE Tracker SET Start_Date = '" + str(month_year) + "' WHERE Name = '" +
                             str(court_name) + "'")

                response = s.post(base_url + 'judgement.aspx', data=data)
                res = response.text

                if "no records were found." in res.lower() or "application error" in res.lower():
                    logging.error("NO data Found for start date: " + str(month_year))
                    update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                                 str(court_name) + "'")
                    continue

                if not parse_html(res, court_name):
                    logging.error("Failed to parse data")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("NAGALAND")
    return request_data(court_name, start_date, end_date)

