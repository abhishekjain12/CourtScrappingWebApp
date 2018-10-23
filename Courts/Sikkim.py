import json
import os
from datetime import datetime

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
from Utils.db import insert_query, update_query, select_one_query, select_count_query, update_history_tracker
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://highcourtofsikkim.nic.in"


def month_list_(dates):
    start, end = [datetime.strptime(_, "%m%y") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    m_list = []
    for tot_m in range(total_months(start) - 1, total_months(end)):
        y, m = divmod(tot_m, 12)
        m_list.append(datetime(y, m + 1, 1).strftime("%m%y").lower())
    return m_list


def request_pdf(url, case_id, court_name):
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


def parse_html(html_str, court_name):
    try:
        soup = BeautifulSoup(str(html_str).replace('&', ' '), "html.parser")
        tr_list = soup.find_all('tr')

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
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    judgment_date = escape_string(str(td.decode_contents()))

                if i == 2:
                    judge_name = escape_string(str(td.decode_contents()))

                if i == 3:
                    case_no = escape_string(str(td.text))

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

                    if i == 4:
                        party = str(td.decode_contents()).split("v/s")
                        petitioner = escape_string(str(party[0]))
                        respondent = escape_string(str(party[1]))

                    if i == 5:
                        a_tag = BeautifulSoup(str(td), "html.parser").a
                        pdf_file = escape_string(str(base_url + a_tag.get('href')))
                        pdf_data = escape_string(request_pdf(base_url + a_tag.get('href'), case_no, court_name))

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
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, start_date, end_date_):
    try:
        url = base_url + "/hcs/hcourt/hg_judgement_search"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "application/json",
            'Cache-Control': "no-cache"
        }

        if int(start_date[-2:]) < 11:
            update_query("UPDATE Tracker SET status = 'IN_NO_DATA_FOUND', emergency_exit=true WHERE Name = '" +
                         str(court_name) + "'")
            if int(end_date_[-2:]) < 11:
                update_history_tracker(court_name)
                return True

        for month_year in month_list_([str(start_date), str(end_date_)]):
            year = int(month_year[-2:]) - 10

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            update_query("UPDATE Tracker SET Start_Date = '" + str(month_year) + "', End_Date = '" + str(end_date_) +
                         "' WHERE Name = '" + str(court_name) + "'")

            querystring = {"ajax_form": "1", "_wrapper_format": "drupal_ajax"}

            payload = "form_build_id=form-BS37MKVfuGmv9fgHWUqr3U9nFCjolonq-Nnenj3Ks24" \
                      "&form_id=ajax_example_form" \
                      "&ordermonth=" + str(month_year[:-2]).lstrip("0") + \
                      "&orderyear=" + str(year) + \
                      "&_triggering_element_name=op" \
                      "&_triggering_element_value=Search" \
                      "&_drupal_ajax=1" \
                      "&ajax_page_state%5Btheme%5D=mytheme" \
                      "&ajax_page_state%5Btheme_token%5D=%20" \
                      "&ajax_page_state%5Blibraries%5D=asset_injector%2Fcss%2Fanimation_accordin%2Casset_injector" \
                      "%2Fcss%2Fside_bar%2Casset_injector%2Fcss%2Ftable%2Casset_injector%2Fjs%2Fseperate_tab_%2C" \
                      "core%2Fdrupal.ajax%2Ccore%2Fhtml5shiv%2Ccore%2Fjquery.form%2Cmytheme%2Fmylibrarynew%2C" \
                      "system%2Fbase%2Cviews%2Fviews.module"

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                        proxies=proxy_dict)

            json_res = json.loads(response.text)
            res = None
            for json_r in json_res:
                if "data" in json_r:
                    res = BeautifulSoup(str(json_r['data']), "html.parser")
                    break

            if res is None:
                logging.error("NO data Found for start date: " + str(month_year))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")
                continue

            if not parse_html(res, court_name):
                logging.error("Failed to parse data from date: " + str(month_year))

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("SIKKIM")
    return request_data(court_name, start_date, end_date)
