import datetime
import os
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


# ----------------------------------------------------------------------------------------------------------------------
# m_sideflg - Court Name
# C         Bombay- Appellate(Civil)
# CR        Bombay- Appellate(Criminal)
# OS        Bombay-Original
# NC        Nagpur-Civil
# NR        Nagpur-Criminal
# AC        Aurangabad-Civil
# AR        Aurangabad-Criminal

court_name = "Bombay"
m_sideflg = "C"
# ----------------------------------------------------------------------------------------------------------------------


module_directory = os.path.dirname(__file__)
logs.initialize_logger("HCS")

base_url = "http://bombayhighcourt.nic.in/"


def request_pdf(url, case_id):
    try:
        response = requests.request("GET", url)
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
        table_soup = BeautifulSoup(str(soup.find_all('form')[0]), "html.parser")
        table_soup = BeautifulSoup(str(table_soup.find_all('table', {"width": "100%"})[0]), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
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
                    pdf_data = escape_string(request_pdf(pdf_file, case_no))

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, petitioner, respondent, judgment_date, " \
                                                           "coram, pdf_data, pdf_file) VALUE ('" + case_no + "', '" + \
                        petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + coram + "', '" + \
                        pdf_data + "', '" + pdf_file + "')"
            insert_query(sql_query)

            sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def request_data():
    start_date = None
    try:
        url = base_url + "ordqryrepact_action.php"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        start_date = "01-01-1950"

        i = 0
        while True:
            i += 1
            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=365)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime("31-12-2019", "%d-%m-%Y") < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            sql_query = "UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) + \
                        "' WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

            payload = "pageno=1" \
                      "&frmaction=" \
                      "&m_sideflg=" + str(m_sideflg) + \
                      "&actcode=0" \
                      "&frmdate=" + str(start_date) + \
                      "&todate=" + str(end_date)

            response = requests.request("POST", url, data=payload, headers=headers)

            res = response.text
            # print(res)

            if "invalid inputs given" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))

                sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                            str(court_name) + "'"
                update_query(sql_query)

                start_date = end_date
                continue

            fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_" +
                      str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
            fw.write(str(res))

            if not parse_html(res):
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
