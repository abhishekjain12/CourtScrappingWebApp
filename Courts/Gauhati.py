import os
import re

import requests
import traceback
import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify

from Utils import logs
from Utils.db import insert_query, update_history_tracker, select_one_query, update_query
from Utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://ghconline.gov.in/"


def month_list_(dates):
    start, end = [datetime.strptime(_, "%b%y") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    m_list = []
    for tot_m in range(total_months(start) - 1, total_months(end)):
        y, m = divmod(tot_m, 12)
        m_list.append(datetime(y, m + 1, 1).strftime("%b%y"))
    return m_list


def date_fix(month_year):
    if str(month_year[:-2]) == 'Jul':
        month_year = 'July' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Apr':
        if str(month_year[-2:]) == '10':
            month_year = 'Appr' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Jun':
        if str(month_year[-2:]) == '11' or str(month_year[-2:]) == '12' or str(month_year[-2:]) == '13' or \
                str(month_year[-2:]) == '16' or str(month_year[-2:]) == '17':
            month_year = 'June' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Aug':
        if str(month_year[-2:]) == '11' or str(month_year[-2:]) == '10':
            month_year = 'August' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Sep':
        if str(month_year[-2:]) == '12' or str(month_year[-2:]) == '14' or str(month_year[-2:]) == '15' or \
                str(month_year[-2:]) == '16' or str(month_year[-2:]) == '17':
            month_year = 'Sept' + str(month_year[-2:])
        if str(month_year[-2:]) == '10':
            month_year = 'September' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Oct':
        if str(month_year[-2:]) == '11' or str(month_year[-2:]) == '10':
            month_year = 'October' + str(month_year[-2:])

    if str(month_year[:-2]) == 'Nov':
        if str(month_year[-2:]) == '11' or str(month_year[-2:]) == '10':
            month_year = 'November' + str(month_year[-2:])

    return month_year


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


def parse_html(html_str, court_name, flag):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        soup = BeautifulSoup(str(soup.prettify()), "html.parser")

        date_h4 = soup.find_all('h4', {'align': 'center'})[0]
        month_year = str(date_h4.text).replace('JUDGMENTS FOR THE MONTH OF', '').strip()

        table_list = soup.find_all('table', {'class': 'DISCOVERY3'})[0]
        table_soup = BeautifulSoup(str(table_list), "html.parser")
        tr_list = table_soup.find_all('tr')

        tr_count = 0
        for tr in tr_list:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            tr_count += 1
            if tr_count <= 1:
                continue

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            subject = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            # insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            if flag:
                i = 1
            else:
                i = 0
            for td in td_list:
                i += 1
                if i == 2:
                    judgment_day = escape_string(str(td.decode_contents()))
                    judgment_date = str(re.findall('\d+', str(judgment_day))[0]) + ", " + month_year.replace(
                        'JUDGEMENTS FOR THE MONTH OF', '')

                if i == 3:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = escape_string(str(base_url + a_tag.get('href')))
                    case_no = escape_string(str(a_tag.text).replace("\n", "").strip())

                    # if select_count_query(str(court_name), str(case_no), 'judgment_date', judgment_date):
                    #     insert_check = True
                    pdf_data = escape_string(request_pdf(str(base_url + a_tag.get('href')), case_no, court_name))

                if i == 4:
                    font_tag = BeautifulSoup(str(td), "html.parser").font
                    if font_tag is not None:
                        span_tag = font_tag.span
                    else:
                        span_tag = BeautifulSoup(str(td), "html.parser").span
                        if span_tag is None:
                            span_tag = BeautifulSoup(str(td), "html.parser")

                    party = str(span_tag.decode_contents()).split("<br/>")
                    petitioner = escape_string(
                        str(party[0]).replace('<td align="center" bgcolor="#FFFFFF" valign="middle" width="30%">',
                                              '').strip())
                    petitioner = re.sub(r'(\\x(.){2})', '', petitioner)

                    respondent = escape_string(str(party[2]).replace('</td>', '').strip())
                    respondent = re.sub(r'(\\x(.){2})', '', respondent)

                if i == 5:
                    subject = escape_string(str(td.decode_contents()).strip())

                if i == 6:
                    judge_name = escape_string(str(td.text).replace(r'\x', '').replace('\\xC2\\x92BLE', '').strip())
                    judge_name = re.sub(r'(\\x(.){2})', '', judge_name)
                    judge_name = re.sub(r'', '', judge_name, re.U)

            # if case_no != "NULL" and insert_check and td_list:
            if case_no != "NULL" and td_list:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, petitioner, respondent, judgment_date, " \
                                                               "subject, pdf_file, pdf_filename) VALUE ('" + case_no + \
                            "', '" + petitioner + "', '" + respondent + "', '" + judgment_date + "', '" + subject + \
                            "', '" + pdf_file + "', '" + court_name + "_" + slugify(case_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET judge_name = '" + str(judge_name) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, start_date, end_date_):
    try:
        headers = {
            'Cache-Control': "no-cache",
        }

        if int(start_date[-2:]) < 10:
            update_query("UPDATE Tracker SET status = 'IN_NO_DATA_FOUND', emergency_exit=true WHERE Name = '" +
                         str(court_name) + "'")
            if int(end_date_[-2:]) < 10:
                update_history_tracker(court_name)
                return True

        for month_year in month_list_([str(start_date), str(end_date_)]):
            month_year = date_fix(month_year)

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            url = base_url + "JDMT" + str(month_year) + ".html"

            update_query("UPDATE Tracker SET Start_Date = '" + str(month_year) + "', End_Date = '" +
                         str(end_date_) + "' WHERE Name = '" + str(court_name) + "'")

            response = requests.request("GET", url, headers=headers, proxies=proxy_dict)
            res = response.text

            if "file or directory not found" in res.upper():
                logging.error("NO data Found for start date: " + str(month_year))

                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                continue

            if str(month_year[-2:]) == '10' or str(month_year) == 'Jan11':
                if not parse_html(res, court_name, True):
                    logging.error("Failed to parse data from date: " + str(month_year))
            else:
                if not parse_html(res, court_name, False):
                    logging.error("Failed to parse data from date: " + str(month_year))

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        return False


def main(court_name, start_date, end_date):
    logs.initialize_logger("Gauhati")
    return request_data(court_name, start_date, end_date)
