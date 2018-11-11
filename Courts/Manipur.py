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
from Utils.db import insert_query, update_query, select_count_query, update_history_tracker, select_one_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)

court_name = "Manipur"
base_url = "http://hcmjudgment.man.nic.in"


def request_pdf(url, case_id):
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


def parse_html(html_str):
    try:
        soup = BeautifulSoup(str(html_str), "html.parser")

        table_soup = BeautifulSoup(str(soup.find_all('table', {"width": "100%"})[0]), "html.parser")
        tr_list = table_soup.select('tr')

        tr_count = 0
        for tr in tr_list:

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count <= 2:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.select('td')

            i = 0
            for td in td_list:
                i += 1

                if i == 1:
                    continue

                if i == 2 and td.get('align') is None:
                    font_tag = BeautifulSoup(str(td), "html.parser").font
                    case_no = escape_string(str(font_tag.text))

                if select_count_query(str(court_name), str(case_no), 'judgment_date', judgment_date):
                    insert_check = True

                    if i == 3 and td.get('align') is None:
                        font_tag = BeautifulSoup(str(td), "html.parser").font
                        respondent = escape_string(str(font_tag.text))

                    if i == 4 and td.get('align') is None:
                        font_tag = BeautifulSoup(str(td), "html.parser").font
                        petitioner = escape_string(str(font_tag.text))

                    if i == 5 and td.get('align') is None:
                        font_tag = BeautifulSoup(str(td), "html.parser").font
                        judgment_date = escape_string(str(font_tag.text))

                    if td.get('align') == 'left':
                        td_soup1 = BeautifulSoup(str(td), "html.parser")
                        judge_name = escape_string(str(td_soup1.text))

                    if td.get('align') == 'center':
                        font_tag = BeautifulSoup(str(td), "html.parser").font
                        a_tag = BeautifulSoup(str(font_tag), "html.parser").a
                        pdf_file = escape_string(base_url + "/" + a_tag.get('href'))
                        pdf_data = escape_string(bytes(str(request_pdf(base_url + "/" + a_tag.get('href'), case_no)),
                                                       'utf-8').decode("utf-8", 'ignore'))

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, petitioner, respondent, judgment_date, " \
                                                               "judge_name, pdf_file, pdf_filename) VALUE ('" + \
                            case_no + "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + \
                            judge_name + "', '" + pdf_file + "', '" + court_name + "_" + slugify(case_no) + ".pdf')"
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


def offset_link(html_str, headers):
    try:
        if not parse_html(html_str):
            return False

        soup = BeautifulSoup(html_str, "html.parser")
        td_tag = soup.find_all('td', {'height': '172', 'align': 'center', 'valign': 'top'})[0]
        td_soup = BeautifulSoup(str(td_tag), "html.parser")
        for table in td_soup.find_all("table"):
            table.decompose()

        a_tags = td_soup.find_all('a')
        a_link_list = []

        for a_tag in a_tags:
            a_link = base_url + a_tag.get('href')
            a_link_list.append(a_link)

        a_link_list_unique = list(set(a_link_list))
        i = 0
        for page_link in a_link_list_unique:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                break

            if page_link != 'http://hcmjudgment.man.nic.in/ByDate.php?page=1':
                response = requests.request("POST", page_link, headers=headers, proxies=proxy_dict)
                res = response.text

                if not parse_html(res):
                    logging.error("Failed for url: " + page_link)
                    return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data(headers, start_date, end_date_):
    try:
        url = base_url + "/ByDate.php"

        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=180)
                        ).strftime("%d-%m-%Y")

            if datetime.datetime.strptime(str(end_date_), "%d-%m-%Y") + datetime.timedelta(days=180) < \
                    datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "date_day=" + str(start_date[0:2]).replace("0", "") + \
                      "&date_month=" + str(start_date[3:5]).replace("0", "") + \
                      "&date_year=" + str(start_date[6:]) + \
                      "&date_day1=" + str(end_date[0:2]).replace("0", "") + \
                      "&date_month1=" + str(end_date[3:5]).replace("0", "") + \
                      "&date_year1=" + str(end_date[6:]) + \
                      "&submit=Submit"

            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            if "invalid inputs given" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not offset_link(res, headers):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(start_date, end_date):
    logs.initialize_logger("Manipur")
    r = requests.request('GET', base_url + "/ByDate.php", proxies=proxy_dict)

    headers = {
        'Content-Type': "text/html",
        'Cookie': 'PHPSESSID=' + str(requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']),
        'Cache-Control': "no-cache",
    }
    return request_data(headers, start_date, end_date)
