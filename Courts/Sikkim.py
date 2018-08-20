import json
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
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
logs.initialize_logger("HCS")

court_name = "sikkim"
base_url = "http://highcourtofsikkim.nic.in"


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
        soup = BeautifulSoup(str(html_str), "html.parser")
        tr_list = soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
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

                if i == 4:
                    party = str(td.decode_contents()).split("v/s")
                    petitioner = escape_string(str(party[0]))
                    respondent = escape_string(str(party[1]))

                if i == 5:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = escape_string(str(base_url + a_tag.get('href')))
                    pdf_data = escape_string(request_pdf(base_url + a_tag.get('href'), case_no))

            sql_query = "INSERT INTO " + str(court_name) + "_HC (case_no, petitioner, respondent, judgment_date, " \
                                                           "judge_name, pdf_data, pdf_file) VALUE ('" + \
                        case_no + "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + \
                        judge_name + "', '" + pdf_data + "', '" + pdf_file + "')"
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
        year_list = ['1', '2', '3', '4', '5', '6', '7', '8']
        month_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        url = base_url + "/hcs/hcourt/hg_judgement_search"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "application/json",
            'Cache-Control': "no-cache"
        }

        i = 0
        for year in year_list:
            for month in month_list:
                i += 1

                sql_query = "UPDATE Tracker SET Start_Date = '" + str(year) + "', End_Date = '" + str(year) + \
                            "' WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

                querystring = {"ajax_form": "1", "_wrapper_format": "drupal_ajax"}

                payload = "form_build_id=form-BS37MKVfuGmv9fgHWUqr3U9nFCjolonq-Nnenj3Ks24" \
                          "&form_id=ajax_example_form" \
                          "&ordermonth=" + str(month) + \
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

                res = BeautifulSoup(str(json.loads(response.content)[1]['data']), "html.parser")
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

                if not parse_html(res):
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
