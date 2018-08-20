import os
import re
from math import ceil

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

court_name = "karnataka"
base_url = "http://judgmenthck.kar.nic.in"

headers = {
    'Cache-Control': "no-cache"
    }


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


def parse_html(html_str):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_tag = soup.find_all('table', {'class': 'miscTable'})[0]

        table_soup = BeautifulSoup(str(table_tag), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            tr_count += 1
            if tr_count == 1:
                continue

            case_no = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            bench = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1

                if i == 1:
                    judgment_date = escape_string(str(td.decode_contents()))

                if i == 2:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    case_no = escape_string(str(a_tag.text).replace("\n", ""))

                    new_url = base_url + a_tag.get('href')
                    response = requests.request('GET', new_url, headers=headers, proxies=proxy_dict)

                    new_soup = BeautifulSoup(str(response.text), "html.parser")
                    new_td_tag = new_soup.find_all('td', {'headers': 't1'})[0]
                    new_a_href = BeautifulSoup(str(new_td_tag), "html.parser").a.get('href')

                    pdf_file = escape_string(base_url + new_a_href)
                    pdf_data = escape_string(request_pdf(base_url + new_a_href, case_no))

                if i == 3:
                    judge_name = escape_string(str(td.text))

                if i == 4:
                    petitioner = escape_string(str(td.text))

                if i == 5:
                    respondent = escape_string(str(td.text))

                if i == 6:
                    bench = escape_string(str(td.text))

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, judgment_date, judge_name, petitioner, " \
                                                           "respondent, bench, pdf_data, pdf_file) VALUE ('" + \
                        case_no + "', '" + judgment_date + "', '" + judge_name + "', '" + petitioner + "', '" + \
                        respondent + "', '" + bench + "', '" + pdf_data + "', '" + pdf_file + "')"
            insert_query(sql_query)

            sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
            update_query(sql_query)

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def offset_link(html_str, url, querystring):
    try:
        if not parse_html(html_str):
            return False

        querystring['sort_by'] = "1"
        querystring['etal'] = "-1"

        soup = BeautifulSoup(html_str, "html.parser")
        div_tag = soup.find_all('div', {'class': 'browse_range'})[0]

        total_records = int(re.findall('\d+', str(div_tag.text))[-1])
        total_calls = ceil(total_records/200)

        next_num = 0
        for page_link in range(0, total_calls):
            next_num += 200

            querystring['offset'] = str(next_num)
            response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)
            res = response.text

            fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_offset_" +
                      str(next_num) + ".html", "w")
            fw.write(str(res))

            if not parse_html(res):
                logging.error("Failed for url: " + str(next_num))
                return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data_old():
    try:
        url = base_url + "/judgments/browse"

        sql_query = "UPDATE Tracker SET Start_Date = '1999', End_Date = '2014' WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)

        querystring = {"type": "reported", "value": "Reportable", "sort_by": "1", "order": "ASC", "rpp": "357",
                       "etal": "0", "submit_browse": "Update"}

        response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)

        res = response.text
        # print(res)

        if "NO ROWS" in res.upper():
            sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                        str(court_name) + "'"
            update_query(sql_query)

        fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_1990" + ".html", "w")
        fw.write(str(res))

        if not parse_html(res):
            logging.error("Failed to parse data old")

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


def request_data():
    try:
        url = base_url + "/judgmentsdsp/browse"

        sql_query = "UPDATE Tracker SET Start_Date = '2014', End_Date = '2018' WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)

        querystring = {"type": "reportable", "order": "ASC", "rpp": "200", "value": "Reportable"}

        response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy_dict)

        res = response.text
        # print(res)

        if "NO ROWS" in res.upper():
            sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                        str(court_name) + "'"
            update_query(sql_query)

        fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_2014" + ".html", "w")
        fw.write(str(res))

        if not offset_link(res, url, querystring):
            logging.error("Failed to parse data")

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


# print(request_data_old())
print(request_data())
