import requests
import datetime
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


# ----------------------------------------------------------------------------------------------------------------------
# IND - Indore
# JBP - Jabalpur
# GWL - Gwailor

court_name = "Madhya_Pradesh"
# ----------------------------------------------------------------------------------------------------------------------


module_directory = os.path.dirname(__file__)
logs.initialize_logger("HCS")

base_url = "https://mphc.gov.in"


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


def parse_html(html_str, bench):
    try:
        soup = BeautifulSoup(html_str.replace("<b>", "").replace("</b>", "").replace("</br>", "").replace("<b", ""),
                             "html.parser")
        tr_list = soup.find_all('tr')
        del tr_list[0:7]

        case_no = "NULL"
        petitioner = "NULL"
        respondent = "NULL"
        petitioner_advocate = "NULL"
        respondent_advocate = "NULL"
        judgment_date = "NULL"
        disposal_date = "NULL"
        judge_name = "NULL"
        pdf_data = "NULL"
        pdf_file = "NULL"

        tr_count = 0
        for tr in tr_list:
            tr_count += 1

            if tr_count == 1:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        case_no = escape_string(str(td.text).strip())

                    if td_count == 4:
                        td_text = str(td.text)
                        if td_text.find("NA") == -1:
                            a_tag = BeautifulSoup(str(td), "html.parser").a
                            if a_tag:
                                a_link = a_tag.get('href')
                                pdf_data = escape_string(request_pdf(base_url + a_link, case_no))
                                pdf_file = base_url + a_link

                        judgment_date = escape_string(td_text.replace("Judgement", "")
                                                             .replace("(AFR)", "").replace("NA", "").strip())

            if tr_count == 2:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        petitioner = escape_string(str(td.text).strip())

            if tr_count == 3:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        respondent = escape_string(str(td.text).strip())

            if tr_count == 4:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        petitioner_advocate = escape_string(str(td.text).strip())

            if tr_count == 5:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        respondent_advocate = escape_string(str(td.text).strip())

            if tr_count == 6:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        judge_name = escape_string(str(td.text).strip())

            if tr_count == 7:
                td_count = 0
                tr_soup = BeautifulSoup(str(tr), "html.parser")
                td_list = tr_soup.find_all('td')
                for td in td_list:
                    td_count += 1
                    if td_count == 3:
                        disposal_date = escape_string(str(td.text).strip())

                sql_query = "INSERT INTO " + str(court_name) + \
                            "_HC (case_no, petitioner, respondent, petitioner_advocate, respondent_advocate, " \
                            "judgment_date, disposal_date, bench, judge_name, pdf_data, pdf_file)" \
                            " VALUE ('" + case_no + "', '" + petitioner + "', '" + respondent + "', '" + \
                            petitioner_advocate + "', '" + respondent_advocate + "', '" + judgment_date + "', '" + \
                            disposal_date + "', '" + bench + "', '" + judge_name + "', '" + pdf_data + "', '" + \
                            pdf_file + "')"
                insert_query(sql_query)

                sql_query = "UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

            if tr_count == 9:
                tr_count = 0
                case_no = "NULL"
                petitioner = "NULL"
                respondent = "NULL"
                petitioner_advocate = "NULL"
                respondent_advocate = "NULL"
                judgment_date = "NULL"
                judge_name = "NULL"
                pdf_data = "NULL"
                pdf_file = "NULL"

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        sql_query = "UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'"
        update_query(sql_query)
        return False


def request_data():
    start_date = None
    try:
        url = base_url + '/php/hc/judgement/judgement_pro_all.php'

        headers = {
            'Cookie': "SSESS8c45314aadff2a84e50fe1a5f9b552c7=yac4IPhMVtTR6dUaZ0dFZ2QNuiKeggEgIwZhjC7oHwc; "
                      "PHPSESSID=n2sl8vof12ci8u6logji67jn34; has_js=1",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        start_date = "01-01-1950"

        benches = ['IND', 'JBP', 'GWL']
        for bench in benches:

            i = 0
            while True:
                i += 1
                end_date = (datetime.datetime.strptime(str(start_date), "%d-%m-%Y") + datetime.timedelta(days=365)
                            ).strftime("%d-%m-%Y")

                if datetime.datetime.strptime("31-12-2019", "%d-%m-%Y") < \
                        datetime.datetime.strptime(str(end_date), "%d-%m-%Y"):
                    logging.error("END date Exceed.")
                    break

                sql_query = "UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + \
                            str(end_date) + "' WHERE Name = '" + str(court_name) + "'"
                update_query(sql_query)

                payload = "lst_judge=0" \
                          "&lst_pet=" \
                          "&txtparty=" \
                          "&lst_counsel=" \
                          "&txtcounsel=" \
                          "&date1=" + str(start_date) + \
                          "&date2=" + str(end_date) + \
                          "&onlyafr=Y" \
                          "&court=" + str(bench) + \
                          "&lst_judge1=0" \
                          "&lst_judge2=0" \
                          "&btn_search=is" \
                          "&bench=" \
                          "&sort=jo" \
                          "&ad=DESC"

                response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)

                res = response.text
                # print(res)

                if "no jugdement or order found that you want to search" in res.lower():
                    logging.error("NO data Found for start date: " + str(start_date))

                    sql_query = "UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" + \
                                str(court_name) + "'"
                    update_query(sql_query)

                    start_date = end_date
                    continue

                fw = open(module_directory + "/../Html_Files/HCS_" + str(court_name) + "_" +
                          str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
                fw.write(str(res))

                if not parse_html(res, bench):
                    logging.error("Failed to parse data from date: " + str(start_date))

                start_date = end_date

        shutil.make_archive(str(court_name) + "_HTML_FILES", 'zip', module_directory + "/../Html_Files")
        shutil.make_archive(str(court_name) + "_TEXT_FILES", 'zip', module_directory + "/../Text_Files")
        shutil.make_archive(str(court_name) + "_PDF_FILES", 'zip', module_directory + "/../PDF_Files")

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
