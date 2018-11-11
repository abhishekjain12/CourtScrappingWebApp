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


# Court Name -      dc
# 'MEGHALAYA':      '16',
# 'delhi':          '31',
# 'UTTARANCHAL':    '35',
# 'ORISSA':         '19'
# 'J&K -Jammu':     '1'
# 'J&K-Srinagar'"   '2'


module_directory = os.path.dirname(__file__)
base_url = "http://lobis.nic.in"


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


def parse_html(html_str, court_name, dc):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
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
            corrigendum = "NULL"
            pdf_data = "NULL"
            pdf_file = "NULL"
            insert_check = False

            tr_soup = BeautifulSoup(str(tr), "html.parser")
            td_list = tr_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    continue

                if i == 2:
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    pdf_file = base_url + a_tag.get('href')
                    case_no = str(a_tag.text).replace("\n", "")
                    pdf_data = escape_string(request_pdf(pdf_file, case_no, court_name))

                if i == 3:
                    span_tag = BeautifulSoup(str(td), "html.parser").span
                    judgment_date = escape_string(str(span_tag.decode_contents()))

                if select_count_query(str(court_name), str(case_no), 'judgment_date', judgment_date):
                    insert_check = True

                    if i == 5:
                        span_tag = BeautifulSoup(str(td), "html.parser").span
                        corrigendum = escape_string(str(span_tag.decode_contents()))

                    if i == 4:
                        td_soup = BeautifulSoup(str(td), "html.parser")
                        span_list = td_soup.find_all('span')

                        j = 0
                        for span in span_list:
                            j += 1

                            if j == 1:
                                petitioner = escape_string(str(span.decode_contents()))
                            if j == 3:
                                respondent = escape_string(str(span.decode_contents()))

            if case_no != "NULL" and insert_check:
                sql_query = "INSERT INTO " + str(court_name) + " (case_no, petitioner, respondent, judgment_date, " \
                                                               "corrigendum, pdf_file, bench_code, pdf_filename) VALUE"\
                                                               " ('" + case_no + "', '" + petitioner + "', '" + \
                            respondent + "', '" + judgment_date + "', '" + corrigendum + "', '" + pdf_file + "', " + \
                            str(dc) + ", '" + court_name + "_" + slugify(case_no) + ".pdf')"
                insert_query(sql_query)

                update_query("UPDATE " + court_name + " SET pdf_data = '" + str(pdf_data) + "' WHERE case_no = '" +
                             str(case_no) + "'")
                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def offset_link(html_str, headers, court_name, dc):
    try:
        if not parse_html(html_str, court_name, dc):
            return False

        soup = BeautifulSoup(html_str, "html.parser")
        p_tag = soup.find_all('p', {'class': 'style2'})[1]
        p_soup = BeautifulSoup(str(p_tag), "html.parser")
        a_tags = p_soup.find_all('a')
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

            if page_link != "http://lobis.nic.in/juddt1.php?offset=0":
                response = requests.request("POST", page_link, headers=headers, proxies=proxy_dict)
                res = response.text

                if not parse_html(res, court_name, dc):
                    logging.error("Failed for url: " + page_link)
                    return False

        return True
    except Exception as e:
        logging.error("Error in offset_link. %s", e)
        return False


def request_data(court_name, dc, headers, start_date, end_date_):
    try:
        url = base_url + "/juddt1.php"

        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=1)
                        ).strftime("%d/%m/%Y")

            if datetime.datetime.strptime(str(end_date_), "%d/%m/%Y") + datetime.timedelta(days=1) < \
                    datetime.datetime.strptime(str(end_date), "%d/%m/%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            querystring = {"dc": str(dc), "fflag": "1"}
            payload = "juddt=" + str(start_date) + "&Submit=Submit"

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                        proxies=proxy_dict)
            res = response.text

            if "NO ROWS" in res.upper():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not offset_link(res, headers, court_name, dc):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)
        return False


def main(court_name, dc, start_date, end_date):
    logs.initialize_logger("LOBIS")
    r = requests.request('GET', base_url + '/juddt.php', proxies=proxy_dict)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Cookie': 'PHPSESSID=' + str(requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']),
    }

    payload = "rb=1&selhc=" + str(dc) + "&Submit=Submit"
    requests.request("POST", base_url, data=payload, headers=headers, proxies=proxy_dict)

    return request_data(court_name, dc, headers, start_date, end_date)
