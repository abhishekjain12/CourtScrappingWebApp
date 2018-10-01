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
base_url = "http://clb.gov.in/Publication/"


def request_pdf(url, case_id, court_name):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200:
            res = response.text

            if res is None:
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


def parse_html(html_str, court_name, bench, child_url):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        div_soup = BeautifulSoup(str(soup.find_all('div', {'id': 'text'})[0]), 'html.parser')
        tr_list = div_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count == 1:
                continue

            case_no = "NULL"
            date_of_order = "NULL"
            description = "NULL"
            section = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    case_no = escape_string(str(td.text).strip().replace("\n", ""))

                if i == 2:
                    date_of_order = escape_string(str(td.text).strip().replace("\n", ""))

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

                    if i == 3:
                        description = escape_string(str(td.text).strip())
                        a_tag = BeautifulSoup(str(td), "html.parser").font.a
                        pdf_url = base_url + child_url + a_tag.get('href')
                        pdf_file = escape_string(pdf_url)
                        # pdf_data = escape_string(request_pdf(pdf_url, case_no, court_name))

                    if i == 4:
                        section = str(td.text)

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, date_of_order, description, section, " \
                                                               "pdf_file, bench_code, pdf_filename) VALUE ('" + \
                            case_no + "', '" + date_of_order + "', '" + description + "', '" + section + "', '" + \
                            pdf_file + "', '" + str(bench) + "', '" + court_name + "_" + slugify(case_no) + ".pdf')"
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


def request_data(court_name, bench, start_date, end_date_):
    try:
        for year in range(start_date, end_date_ + 1):
            if int(year) < 2010 or int(year) > 2016:
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")
                continue

            section_types = ['111_111_A', '397_398', 'Others']
            for section_type in section_types:

                child_url = str(bench) + '/' + str(year) + '/' + str(section_type) + '/'
                url = base_url + child_url + 'index.html'

                emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
                if emergency_exit['emergency_exit'] == 1:
                    update_history_tracker(court_name)
                    return True

                update_query("UPDATE Tracker SET Start_Date = '" + str(year) + "', End_Date = '" + str(year) +
                             "' WHERE Name = '" + str(court_name) + "'")

                response = requests.request("GET", url, proxies=proxy_dict)
                res = response.text
                fw = open(module_directory + "/../Data_Files/Html_Files/" + court_name + "_" +
                          str(start_date).replace("/", "-") + "_.html", "w")
                fw.write(str(res))

                if res is None:
                    logging.error("NO data Found for year: " + str(year))
                    update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                                 str(court_name) + "'")
                    continue

                if not parse_html(res, court_name, bench, child_url):
                    logging.error("Failed to parse data for year: " + str(year))

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, bench, start_date, end_date):
    logs.initialize_logger("National_Company_Law_Tribunal")
    return request_data(court_name, bench, int(start_date), int(end_date))
