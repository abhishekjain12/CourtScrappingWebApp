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

# m_sideflg - Court Name
# C         Bombay- Appellate(Civil)
# CR        Bombay- Appellate(Criminal)
# OS        Bombay-Original
# NC        Nagpur-Civil
# NR        Nagpur-Criminal
# AC        Aurangabad-Civil
# AR        Aurangabad-Criminal


module_directory = os.path.dirname(__file__)

base_url = "http://bombayhighcourt.nic.in/"


def request_pdf(url, case_id, court_name):
    try:
        response = requests.request("GET", url)
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


def parse_html(html_str, court_name, m_sideflg):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_soup = BeautifulSoup(str(soup.find_all('form')[0]), "html.parser")
        table_soup = BeautifulSoup(str(table_soup.find_all('table', {"width": "100%"})[0]), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count <= 4 or tr_count % 2 == 0:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            coram = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1

                if i == 1 or i == 6 or str(td.decode_contents()).replace("\n", "").strip() == \
                        '<font color="blue">LBR  : Larger Benches Referred Matter</font>':
                    continue

                if i == 2:
                    coram = escape_string(str(td.decode_contents()))

                if i == 3:
                    data1 = escape_string(str(td.decode_contents()))
                    data1_list = data1.split("<b>")
                    petitioner = data1_list[0]
                    respondent = str(data1_list[1]).split("</b>")[1]

                if i == 4:
                    data2 = escape_string(str(td.decode_contents()))
                    data2_list = data2.split("<br/>")
                    judgment_date = data2_list[0]

                if i == 5:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = base_url + a_tag.get('href')
                    case_no = str(a_tag.text).replace("\n", "")
                    pdf_data = escape_string(request_pdf(pdf_file, case_no, court_name))

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (m_sideflg, case_no, petitioner, respondent, " \
                                                               "judgment_date, coram, pdf_file, pdf_filename) VALUE " \
                                                               "('" + m_sideflg +\
                            "', '" + case_no + "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + \
                            "', '" + coram + "', '" + pdf_file + "', '" + court_name + "_" + slugify(case_no) + ".pdf')"
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


def request_data(court_name, m_sideflg, start_date, end_date_):
    try:
        url = base_url + "ordqryrepact_action.php"
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

            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=180)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime(end_date_, "%d-%m-%Y") + datetime.timedelta(days=180) < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "pageno=1" \
                      "&frmaction=" \
                      "&m_sideflg=" + str(m_sideflg) + \
                      "&actcode=0" \
                      "&frmdate=" + str(start_date) + \
                      "&todate=" + str(end_date)

            response = requests.request("POST", url, data=payload, headers=headers)
            res = response.text

            if "invalid inputs given" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not parse_html(res, court_name, m_sideflg):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, m_sideflg, start_date, end_date):
    logs.initialize_logger("BOMBAY")
    return request_data(court_name, m_sideflg, start_date, end_date)
