import os
import re

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

court_name = "Arunachal"
base_url = "http://ghcitanagar.gov.in/GHCITA/"


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


def parse_html(html_str, month, year):
    try:
        soup = BeautifulSoup(html_str.replace("</a>", ""), "html.parser")
        soup = BeautifulSoup(str(soup.prettify()), "html.parser")

        table_list = soup.find_all('table', {'class': 'style41'})[0]
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            if tr_count <= 5:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            subject = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td', {'colspan': None})

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    judgment_day = escape_string(str(td.decode_contents()))
                    judgment_date = str(re.findall('\d+', str(judgment_day))[0]) + "/" + str(month) + "/" + str(year)

                if i == 2:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = escape_string(str(base_url + a_tag.get('href')))
                    case_no = escape_string(str(a_tag.text).replace("\n", ""))
                    pdf_data = escape_string(request_pdf(pdf_file, case_no))

                if i == 3:
                    party = str(td.decode_contents()).split("<br/>")
                    petitioner = escape_string(str(party[0]).replace("<strong>", "").replace("</strong>", ""))
                    respondent = escape_string(str(party[2]).replace("<strong>", "").replace("</strong>", ""))

                if i == 4:
                    subject = escape_string(str(td.decode_contents()))

                if i == 5:
                    p_tag = BeautifulSoup(str(td), "html.parser").p
                    if p_tag is not None:
                        judge_name = escape_string(str(p_tag.decode_contents()))
                    else:
                        judge_name = escape_string(str(td.decode_contents()))

            if td_list:
                sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, petitioner, respondent, judgment_date, " \
                                                               "judge_name, subject, pdf_data, pdf_file) VALUE ('" + \
                            case_no + "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + \
                            judge_name + "', '" + subject + "', '" + pdf_data + "', '" + pdf_file + "')"
                insert_query(sql_query)

                sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def request_data():
    try:
        year_list = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
        month_list = ['jan', 'feb', 'mar', 'april', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec']

        headers = {
            'Cache-Control': "no-cache",
        }

        i = 0
        for year in year_list:
            for month in month_list:
                i += 1

                url = base_url + "ghci_" + str(month) + str(year) + ".html"

                sql_query = "UPDATE Tracker SET Start_Date = '" + str(year) + "', End_Date = '" + str(year) + \
                            "' WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

                response = requests.request("GET", url, headers=headers, proxies=proxy_dict)

                res = response.text
                # print(res)

                if "NO ROWS" in res.upper():
                    logging.error("NO data Found for start date: " + str(month) + str(year))

                    sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                                str(court_name) + "'"
                    update_query(sql_query)

                    continue

                fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_" +
                          str(month) + str(year) + "_" + str(i) + ".html", "w")
                fw.write(str(res))

                if not parse_html(res, i, year):
                    logging.error("Failed to parse data from date: " + str(month) + str(year))

        shutil.make_archive(str(court_name) + "_HTML_FILES", 'zip', module_directory + "/../Html_Files")
        shutil.make_archive(str(court_name) + "_TEXT_FILES", 'zip', module_directory + "/../Text_Files")

        sql_query = "UPDATE Tracker SET status = 'IN_SUCCESS' WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)

        return "IN_SUCCESS"

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)

        sql_query = "UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" + \
                    str(court_name) + "'"
        update_query(sql_query)

        return "IN_FAILED"


print(request_data())