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
base_url = "https://phhc.gov.in/"
vercode = "d02a"


def request_pdf(auth, case_id, court_name, headers):
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


def parse_html(html_str, court_name, headers):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_list = soup.find_all('table', {'id': 'tables11'})
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count <= 3:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

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

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

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
                            str(pdf_file).replace(base_url + "download_file.php?auth=", ""), case_no, court_name,
                            headers))

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, petitioner, respondent, judgment_date, " \
                                                               "pdf_file) VALUE ('" + case_no + "', '" + \
                            petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + pdf_file + "')"
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


def request_data(court_name, headers, start_date, end_date_):
    try:
        url = base_url + "home.php"

        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=1)
                        ).strftime("%d/%m/%Y")

            if datetime.datetime.strptime(end_date_, "%d/%m/%Y") + datetime.timedelta(days=1) < \
                    datetime.datetime.strptime(str(end_date), "%d/%m/%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            querystring = {"search_param": "free_text_search_judgment"}

            payload = "t_case_type=" \
                      "&t_case_year=" \
                      "&submit=Search%20Case" \
                      "&from_date=" + str(start_date) + \
                      "&to_date=" + str(end_date) + \
                      "&pet_name=" \
                      "&res_name=" \
                      "&free_text=JUSTICE"

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                        proxies=proxy_dict)
            res = response.text

            if "no data found" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not parse_html(res, court_name, headers):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        update_query("UPDATE Tracker SET status = 'IN_SUCCESS', emergency_exit=true WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        update_query("UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("PUNJAB_HARYANA")
    r = requests.request('GET', base_url, proxies=proxy_dict)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cookie': 'PHPSESSID=' + str(requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']),
        'Cache-Control': "no-cache",
    }
    return request_data(court_name, headers, start_date, end_date)
