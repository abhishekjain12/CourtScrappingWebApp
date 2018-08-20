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


module_directory = os.path.dirname(__file__)
logs.initialize_logger("HCS")

court_name = "haryana"
base_url = "https://phhc.gov.in/"
vercode = "d02a"

headers = {
    'Cookie': "PHPSESSID=8r4ehq1isscl101k7sv7ufoj02",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
    }


def request_pdf(auth, case_id):
    url = base_url + "download_file.php"
    querystring = {"auth": auth}
    payload = "vercode=" + str(vercode) + \
              "&submit=Submit"

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, proxies=proxy_dict)

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


def parse_html(html_str):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_list = soup.find_all('table', {'id': 'tables11'})
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            if tr_count <= 3:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"

            table_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = table_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    continue

                if i == 2:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    case_no = escape_string(str(a_tag.text))

                if i == 3:
                    party = str(td.decode_contents()).split("Vs")
                    petitioner = escape_string(str(party[0]))
                    respondent = escape_string(str(party[1]))

                if i == 4:
                    judgment_date = escape_string(str(td.decode_contents()))

                if i == 5:
                    a_link = BeautifulSoup(str(td), "html.parser").a.get('onclick')
                    a_formatted = str(str(a_link).replace("window.open('", "")).replace("')", "")
                    pdf_file = escape_string(base_url + a_formatted)

                    pdf_data = escape_string(request_pdf(
                        str(pdf_file).replace(base_url + "download_file.php?auth=", ""), case_no))

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, petitioner, respondent, judgment_date, " \
                                                           "pdf_data, pdf_file) VALUE ('" + case_no + "', '" + \
                        petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + pdf_data + "', '" + \
                        pdf_file + "')"
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
    start_date = None
    try:
        url = base_url + "home.php"
        start_date = datetime.datetime.strptime("01/01/1950", "%d/%m/%Y").strftime("%d/%m/%Y")

        i = 0
        while True:
            i += 1
            end_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=365)
                        ).strftime("%d/%m/%Y")

            if datetime.datetime.strptime("31/12/2019", "%d/%m/%Y") < \
                    datetime.datetime.strptime(str(end_date), "%d/%m/%Y"):
                logging.error("DONE")
                break

            sql_query = "UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) + \
                        "' WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

            querystring = {"search_param": "free_text_search_judgment"}

            payload = "t_case_type=" \
                      "&t_case_year=" \
                      "&submit=Search%20Case" \
                      "&from_date=" + str(start_date) + \
                      "&to_date=" + str(end_date) + \
                      "&pet_name=" \
                      "&res_name=" \
                      "&free_text=Jus"

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                        proxies=proxy_dict)

            res = response.text
            # print(res)

            if "no data found" in res.lower():
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
