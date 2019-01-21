import datetime
import json
import os
import requests
import traceback
import logging

from pymysql import escape_string
from slugify import slugify
from new.utils import logs
from new.utils.bucket import transfer_to_bucket
from new.utils.contants import NO_TRIES, DAYS
from new.utils.extract_text import pdf_to_text_api
from new.utils.my_proxy import proxy_dict
from new.utils.db import select_one_query, select_count_query, insert_query, update_query, insert_query, \
    select_one_query, update_history_tracker, update_query

module_directory = os.path.dirname(__file__)


def request_pdf(url, jud_pdf_name, court_name, bench_id, case_id):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200:
            file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + slugify(jud_pdf_name) + \
                        '.pdf'
            fw = open(file_path, "wb")
            fw.write(response.content)
            update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s and bench=%s",
                         (court_name, bench_id))
            return file_path
        else:
            logging.error("Failed to get text file for: " + str(jud_pdf_name))
            insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                         (court_name, bench_id, case_id, 'Failed to download PDF File.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                         (court_name, bench_id))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(jud_pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                     (court_name, bench_id, case_id, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                     (court_name, bench_id))
        return None


def parser(base_url, court_name, response):
    update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0 WHERE court_name=%s",
                 (str(len(response)), court_name))

    for case in response:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s "
                                                "and bench=%s", (court_name, bench_id))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        case_type = case['CaseType']
        case_no = case['CaseNo']
        case_yr = case['CaseYr']
        jud_dt = case['Jud_Dt']
        jud_pdf_name = case['Jud_Pdf_Name']

        case_id = case_type + ' ' + case_no + ' OF ' + case_yr

        if select_count_query(str(court_name), str(case_id), 'judgment_date', jud_dt):
            pdf_url = base_url + jud_pdf_name
            pdf_filename = str(jud_pdf_name).replace('.pdf', '')

            pdf_filepath = request_pdf(pdf_url, pdf_filename, court_name, bench_id, case_id)
            pdf_text_data = escape_string(pdf_to_text_api(pdf_filepath))

            text_filepath = module_directory + "/../data_files/text_files/" + court_name + "_" + slugify(
                pdf_filename) + '.txt'
            fw = open(text_filepath, "w")
            fw.write(pdf_text_data)

            if insert_query(
                    "INSERT INTO kolkata (case_id, judgment_date, pdf_url, pdf_filename, text_filename, case_type, "
                    "case_no, case_year, bench) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (case_id, jud_dt, pdf_url, jud_pdf_name, jud_pdf_name, case_type, case_no, case_yr, bench_id)):

                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s "
                                   "and bench=%s", (court_name, bench_id))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id,
                                                        'Failed to insert court data in table'))

            if update_query("UPDATE kolkata SET text_data=%s WHERE case_id=%s", (pdf_text_data, case_id)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to insert text data.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))

            if transfer_to_bucket('PDF_Files', pdf_filepath):
                update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 "
                                   "WHERE court_name=%s and bench=%s", (court_name, bench_id))
                os.remove(pdf_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to transfer to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))

            if transfer_to_bucket('Text_Files', text_filepath):
                update_query("UPDATE tracker SET transferred_text=transferred_text+1 "
                                   "WHERE court_name=%s and bench=%s", (court_name, bench_id))
                os.remove(text_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to transfer to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))
        else:
            update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s "
                               "and bench=%s", (court_name, bench_id))


def request_data(base_url, court_name):
    start_date = None
    try:
        url = base_url + "/orders-appellate-authority-advance-ruling"

        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit['emergency_exit'] == 1:
            update_history_tracker(court_name, None)
            return True

        update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s", (court_name))
        no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s", (court_name))['no_tries']

        while no_tries < NO_TRIES:
            response = requests.request("GET", url, proxies=proxy_dict)
            if response.status_code == 200:
                parser(base_url, court_name, str(response.text))
                check_cases = select_one_query("SELECT total_cases, inserted_cases FROM tracker "
                                                     "WHERE court_name=%s", (court_name))

                if check_cases['total_cases'] == check_cases['inserted_cases']:
                    break

            elif response.status_code != 200 and no_tries == NO_TRIES:
                update_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s", (court_name))

            no_tries += 1
            update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s", (no_tries, court_name))

        if no_tries == NO_TRIES:
            insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES "
                               "(%s, %s, %s)", (court_name, start_date, 'Failed to get HTML.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

        update_query("UPDATE tracker SET end_date=%s WHERE court_name=%s", (start_date, court_name))
        update_history_tracker(court_name, None)
        start_date = (datetime.datetime.strptime(str(start_date), "%Y-%m-%d") + datetime.timedelta(days=DAYS)
                      ).strftime("%Y-%m-%d")

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES "
                           "(%s, %s, %s)", (court_name, start_date, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return False


def main(court_name):
    logs.initialize_logger("gst_appellate")
    base_url = "http://gstcouncil.gov.in"
    return request_data(base_url, court_name)
