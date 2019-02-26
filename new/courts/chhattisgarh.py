import datetime

import requests
import os
import traceback
import logging

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify

from new.utils import logs
from new.utils.bucket import transfer_to_bucket
from new.utils.contants import NO_TRIES
from new.utils.db import insert_query, update_history_tracker, select_one_query, update_query, select_count_query
from new.utils.extract_text import pdf_to_text_api
from new.utils.json_utils import create_transfer_json
from new.utils.my_proxy import proxy_dict

module_directory = os.path.dirname(__file__)
base_url = "http://highcourt.cg.gov.in/Afr/"


def request_pdf(url, pdf_name, court_name, case_id):
    try:
        if url is not None:
            response = requests.request("GET", url, proxies=proxy_dict)
            if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + slugify(pdf_name) + \
                            '.pdf'
                fw = open(file_path, "wb")
                fw.write(response.content)
                update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s", (court_name))
                return file_path
            else:
                logging.error("Failed to get text file for: " + str(pdf_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to download PDF File.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                return None
        else:
            logging.error("Failed to get pdf file for: " + str(pdf_name))
            insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                         (court_name, case_id, 'Failed to download PDF File. No url.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                     (court_name, case_id, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return None


def parser(html_str, court_name, year):
    soup = BeautifulSoup(html_str, "html.parser")
    ul = soup.find_all('ul')[0]
    ul_soup = BeautifulSoup(str(ul), "html.parser")
    li_list = ul_soup.find_all('li')

    update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0, no_pdf=0, no_text=0, transferred_pdf=0,"
                 "transferred_text=0 WHERE court_name=%s", (str(len(li_list)), court_name))

    for li in li_list:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        a = BeautifulSoup(str(li), "html.parser").a
        a_link = a.get('href')
        subject = a.get_text()
        case_id = str(a_link[a_link.rfind("/")+1:]).replace('.pdf', '')

        if len(case_id) >= 10:
            judgment_date = escape_string(case_id[-10:].replace('(', '').replace(')', ''))
            try:
                judgment_date = datetime.datetime.strptime(str(judgment_date), '%d.%m.%y').strftime('%Y-%m-%d')
            except ValueError:
                judgment_date = year
        else:
            judgment_date = year

        if select_count_query(str(court_name), str(case_id), 'judgment_date', judgment_date):
            pdf_url = base_url + a_link
            pdf_filename = escape_string(slugify(case_id + '-' + judgment_date))
            text_filename = escape_string(slugify(case_id + '-' + judgment_date)) + '.txt'
            pdf_filepath = request_pdf(pdf_url, pdf_filename, court_name, case_id)

            if pdf_filepath is not None:
                pdf_text_data = escape_string(str(pdf_to_text_api(pdf_filepath)))
                text_filepath = module_directory + "/../data_files/text_files/" + court_name + "_" + text_filename
                fw = open(text_filepath, "w")
                fw.write(pdf_text_data)
            else:
                text_filepath = None
                pdf_text_data = None

            if insert_query(
                    "INSERT INTO chhattisgarh (case_id, judgment_date, pdf_url, pdf_filename, text_filename, subject) "
                    "VALUES (%s, %s, %s, %s, %s, %s)", (case_id, judgment_date, pdf_url, pdf_filename, text_filename,
                                                        subject)):
                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s", (court_name))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to insert court data in table'))

            if update_query("UPDATE chhattisgarh SET text_data=%s WHERE case_id=%s", (pdf_text_data, case_id)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", (court_name))
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to insert text data.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if transfer_to_bucket('PDF_Files', pdf_filepath):
                update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 WHERE court_name=%s", (court_name))
                os.remove(pdf_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to transfer PDF to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if transfer_to_bucket('Text_Files', text_filepath):
                update_query("UPDATE tracker SET transferred_text=transferred_text+1 WHERE court_name=%s", (court_name))
                os.remove(text_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to transfer text to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

        else:
            update_query("UPDATE tracker SET inserted_cases=inserted_cases+1, no_pdf=no_pdf+1, no_text=no_text+1,"
                         "transferred_pdf=transferred_pdf+1, transferred_text=transferred_text+1 WHERE court_name=%s",
                         (court_name))


def request_data(court_name):
    year = None
    response = None
    try:
        year = int(select_one_query("SELECT end_date FROM tracker WHERE court_name=%s", (court_name))['end_date'])
        while str(year) <= str(datetime.datetime.now().strftime('%Y')):
            if str(year) == str(datetime.datetime.now().strftime('%Y')):
                year = ''

            url = base_url + "DecisionsHeadline" + str(year) + ".html"

            emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s", (court_name))
            no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s", (court_name))['no_tries']

            while no_tries < NO_TRIES:
                update_query("UPDATE tracker SET total_cases=0, inserted_cases=0, no_pdf=0, no_text=0, "
                             "transferred_pdf=0, transferred_text=0 WHERE court_name=%s", (court_name))
                response = str(requests.request("GET", url, proxies=proxy_dict).text)

                if "file or directory not found" in response.lower():
                    update_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s", (court_name))
                else:
                    parser(response, court_name, str(year))
                    check_cases = select_one_query(
                        "SELECT total_cases, inserted_cases FROM tracker WHERE court_name=%s", (court_name))
                    if check_cases['total_cases'] == check_cases['inserted_cases']:
                        break

                no_tries += 1
                update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s", (no_tries, court_name))

            if no_tries == NO_TRIES:
                insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES (%s, %s, %s)",
                             (court_name, str(year), str(response)))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            update_query("UPDATE tracker SET end_date=%s WHERE court_name=%s", (str(year), court_name))
            create_transfer_json(court_name)
            update_history_tracker(court_name)

            if str(year) == '':
                return True
            year += 1

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES (%s, %s, %s)",
                     (court_name, year, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return False


def main(court_name):
    logs.initialize_logger("chhattisgarh")
    return request_data(court_name)
