import requests
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
logs.initialize_logger("HCS")

court_name = "nagaland"
base_url = "http://kohimahighcourt.gov.in/"


def request_pdf(url, case_id):
    try:
        response = requests.request("GET", url, verify=False, proxies=proxy_dict)
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

            file_path = module_directory + "/../Text_Files/HCS_" + str(court_name) + "_" + str(slugify(case_id)) + \
                        ".txt"
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
        div = soup.find_all('div', {'id': 'CPHBody_PanelList'})[0]
        a_list_soup = BeautifulSoup(str(div), "html.parser")
        a_list = a_list_soup.find_all('a')

        a_list_unique = list(set(a_list))
        for a in a_list_unique:
            case_no = escape_string(str(str(a.text)[:-10]).replace("-", ""))
            judgment_date = escape_string(str(a.text)[-10:])

            a_link = a.get('href')
            pdf_data = escape_string(request_pdf(base_url + a_link, case_no))
            pdf_file = base_url + a_link

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, judgment_date, pdf_data, pdf_file) VALUE ('" \
                        + case_no + "', '" + judgment_date + "', '" + pdf_data + "', '" + pdf_file + "')"
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

        year_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
        month_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        i = 0
        for year in year_list:
            for month in month_list:
                i += 1

                data = {'ctl00$CPHBody$DropDownListYear': str(year),
                        'ctl00$CPHBody$DropDownListMonth': str(month),
                        'ctl00$CPHBody$TextBox1': '',
                        'ctl00$CPHBody$SM1': 'ctl00$CPHBody$SM1|ctl00$CPHBody$DropDownListMonth'
                        }

                with requests.Session() as s:
                    page = s.get(base_url + 'judgement.aspx')
                    soup = BeautifulSoup(page.content, "html.parser")

                    data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
                    data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
                    data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

                    response = s.post(base_url + 'judgement.aspx', data=data)

                    sql_query = "UPDATE Tracker SET Start_Date = '" + str(year) + "' WHERE Name = '" + \
                                str(court_name) + "'"
                    update_query(sql_query)

                    res = response.text
                    # print(res)

                    if "no jugdement or order found that you want to search" in res.lower():
                        logging.error("NO data Found for start date: " + str(year))

                        sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                                    str(court_name) + "'"
                        update_query(sql_query)

                        continue

                    fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_" +
                              str(year) + "_" + str(month) + "_" + str(i) + ".html", "w")
                    fw.write(str(res))

                    if not parse_html(res):
                        logging.error("Failed to parse data")

        shutil.make_archive(str(court_name) + "_HTML_FILES", 'zip', module_directory + "/../Html_Files")
        shutil.make_archive(str(court_name) + "_TEXT_FILES", 'zip', module_directory + "/../Text_Files")
        shutil.make_archive(str(court_name) + "_PDF_FILES", 'zip', module_directory + "/../PDF_Files")

        sql_query = "UPDATE Tracker SET status = 'IN_SUCCESS' WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)

        return "IN_SUCCESS"

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data ")
        logging.error("Failed to request: %s", e)

        sql_query = "UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" + \
                    str(court_name) + "'"
        update_query(sql_query)

        return "IN_FAILED"


print(request_data())
