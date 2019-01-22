import datetime
import json
import os
import requests
import traceback
import logging

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify
from new.utils import logs
from new.utils.bucket import transfer_to_bucket
from new.utils.contants import NO_TRIES, DAYS
from new.utils.extract_text import pdf_to_text_api
from new.utils.my_proxy import proxy_dict
from new.utils.db import select_one_local_query, select_count_query, insert_query, update_query, insert_local_query, \
    select_one_query, update_history_tracker, update_local_query

module_directory = os.path.dirname(__file__)


def request_pdf(url, jud_pdf_name, court_name, bench_id, case_id):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200:
            file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + slugify(jud_pdf_name) + \
                        '.pdf'
            fw = open(file_path, "wb")
            fw.write(response.content)
            update_local_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s and bench=%s",
                               (court_name, bench_id))
            return file_path
        else:
            logging.error("Failed to get text file for: " + str(jud_pdf_name))
            insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                               (court_name, bench_id, case_id, 'Failed to download PDF File.'))
            update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                               (court_name, bench_id))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(jud_pdf_name) + ". Error: %s", e)
        insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                           (court_name, bench_id, case_id, 'Failed to download PDF File.'))
        update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                           (court_name, bench_id))
        return None


def parser(base_url, court_name, bench_id, response):
    pdf_base_path = base_url + 'viewpdf/'

    update_local_query("UPDATE tracker SET total_cases=%s WHERE court_name=%s and bench=%s",
                       (str(len(response)), court_name, bench_id))

    for case in response:
        emergency_exit = select_one_local_query("SELECT emergency_exit FROM tracker WHERE court_name=%s "
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
            pdf_url = pdf_base_path + jud_pdf_name
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

                update_local_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s "
                                   "and bench=%s", (court_name, bench_id))
            else:
                update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                                   (court_name, bench_id))
                insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id,
                                                        'Failed to insert court data in table'))

            if update_query("UPDATE kolkata SET text_data=%s WHERE case_id=%s", (pdf_text_data, case_id)):
                update_local_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s and bench=%s",
                                   (court_name, bench_id))
            else:
                insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to insert text data.'))
                update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                                   (court_name, bench_id))

            if transfer_to_bucket('PDF_Files', pdf_filepath):
                update_local_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 "
                                   "WHERE court_name=%s and bench=%s", (court_name, bench_id))
                os.remove(pdf_filepath)
            else:
                insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to transfer to bucket.'))
                update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                                   (court_name, bench_id))

            if transfer_to_bucket('Text_Files', text_filepath):
                update_local_query("UPDATE tracker SET transferred_text=transferred_text+1 "
                                   "WHERE court_name=%s and bench=%s", (court_name, bench_id))
                os.remove(text_filepath)
            else:
                insert_local_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES "
                                   "(%s, %s, %s, %s)", (court_name, bench_id, case_id, 'Failed to transfer to bucket.'))
                update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                                   (court_name, bench_id))


def request_data(base_url, court_name):
    page_no = None
    try:
        response = None

        emergency_exit = select_one_local_query("SELECT emergency_exit FROM tracker WHERE court_name=%s ", court_name)
        if emergency_exit['emergency_exit'] == 1:
            update_history_tracker(court_name)
            return True

        page_no = select_one_query("SELECT page_no FROM tracker WHERE court_name=%s", court_name)['page_no']

        url = base_url + "?page=" + str(page_no)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, proxies=proxy_dict)

        soup = BeautifulSoup(response.text, "html.parser")

        last_page_li = soup.find_all("li", class_="pager-last last")  # getting last page_ no depends on css so if court
                                                                        # site change this can be a problem

        last_page_li_parser = BeautifulSoup(str(last_page_li), "html.parser")
        last_page_link = last_page_li_parser.find("a")

        last_page_no = int(str(last_page_link['href'])[str(last_page_link['href']).find('=') + 1:])

        while page_no <= last_page_no:
            page_no += 1

        # total_pages =

        # while datetime.datetime.strptime(str(start_date), "%Y-%m-%d") <= today:
        #     emergency_exit = select_one_local_query("SELECT emergency_exit FROM tracker WHERE court_name=%s "
        #                                             "and bench=%s", (court_name, bench_id))
        #     if emergency_exit['emergency_exit'] == 1:
        #         update_history_tracker(court_name, bench_id)
        #         return True
        #
        #     update_local_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s and bench=%s",
        #                        (court_name, bench_id))
        #     no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s and bench=%s",
        #                                 (court_name, bench_id))['no_tries']
        #     while no_tries < NO_TRIES:
        #         payload = "dtfrom=" + start_date + \
        #                   "&dtto=" + start_date
        #
        #         response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
        #         response = json.loads(str(response.text))
        #
        #         if response['error'] == 0 and "data_errors" not in response:
        #             parser(base_url, court_name, bench_id, response['find_data'])
        #             check_cases = select_one_local_query("SELECT total_cases, inserted_cases FROM tracker "
        #                                                  "WHERE court_name=%s AND bench=%s", (court_name, bench_id))
        #
        #             if check_cases['total_cases'] == check_cases['inserted_cases']:
        #                 break
        #
        #         if response['error'] == 1 and response['data_errors'] == 0 and no_tries == NO_TRIES:
        #             update_local_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s and bench=%s",
        #                                (court_name, bench_id))
        #
        #         no_tries += 1
        #         update_local_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s and bench=%s",
        #                            (no_tries, court_name, bench_id))
        #
        #     if no_tries == NO_TRIES:
        #         insert_local_query("INSERT INTO alerts (court_name, bench, start_date, error_message) VALUES "
        #                            "(%s, %s, %s, %s)", (court_name, bench_id, start_date, str(response)))
        #         update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
        #                            (court_name, bench_id))
        #
        #     update_local_query("UPDATE tracker SET end_date=%s WHERE court_name=%s and bench=%s",
        #                        (start_date, court_name, bench_id))
        #     update_history_tracker(court_name, bench_id)
        #     start_date = (datetime.datetime.strptime(str(start_date), "%Y-%m-%d") + datetime.timedelta(days=DAYS)
        #                   ).strftime("%Y-%m-%d")

    except Exception as e:
        traceback.print_exc()
        # logging.error("Failed to request: %s", e)
        # insert_local_query("INSERT INTO alerts (court_name, bench, start_date, error_message) VALUES "
        #                    "(%s, %s, %s, %s)", (court_name, bench_id, start_date, str(e)))
        # update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
        #                    (court_name, bench_id))
        return False


def main(court_name):
    logs.initialize_logger("gst_advance_authority")
    base_url = "http://gstcouncil.gov.in/rulings-by-advance-authority"
    return request_data(base_url, court_name)


main('gst_by_advance_authority')
