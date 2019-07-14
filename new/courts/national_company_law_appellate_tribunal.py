import datetime
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
from new.utils.json_utils import create_transfer_json_bench
from new.utils.my_proxy import proxy_dict
from new.utils.db import select_count_query, insert_query, select_one_query, update_query, update_history_tracker_bench

module_directory = os.path.dirname(__file__)


def request_pdf(url, pdf_name, court_name, bench_id, case_id):
    try:
        if url is not None:
            response = requests.request("GET", url, proxies=proxy_dict)
            if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + pdf_name
                fw = open(file_path, "wb")
                fw.write(response.content)
                update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))
                return file_path
            else:
                logging.error("Failed to get text file for: " + str(pdf_name))
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, bench_id, case_id, 'Failed to download PDF File.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))
                return None
        else:
            logging.error("Failed to get pdf file for: " + str(pdf_name))
            insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                         (court_name, case_id, 'Failed to download PDF File. No url.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s AND bench=%s",
                         (court_name, bench_id))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                     (court_name, bench_id, case_id, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                     (court_name, bench_id))
        return None


def parser(court_name, bench_id, response):
    tbody = BeautifulSoup(str(response), "html.parser").find_all('tbody')[0]
    tr_list = BeautifulSoup(str(tbody), "html.parser").find_all('tr')

    update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0, no_pdf=0, no_text=0, transferred_pdf=0,"
                 "transferred_text=0 WHERE court_name=%s AND bench=%s", (str(len(tr_list)), court_name, bench_id))

    for tr in tr_list:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s AND bench=%s",
                                          (court_name, bench_id))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        case_id = None
        judgment_date = None
        party = None
        section = None
        court_name_ = None
        order_passed_by = None
        pdf_url = None

        i = 0
        td_list = BeautifulSoup(str(tr), "html.parser").find_all('td')
        for td in td_list:
            i += 1
            if i == 1:
                case_id = escape_string(str(td.decode_contents()))
            elif i == 2:
                judgment_date = escape_string(str(td.decode_contents()))
            elif i == 3:
                party = escape_string(str(td.decode_contents()))
            elif i == 4:
                section = escape_string(str(td.decode_contents()))
            elif i == 5:
                court_name_ = escape_string(str(td.decode_contents()))
            elif i == 6:
                order_passed_by = escape_string(str(td.decode_contents()))
            elif i == 7:
                a_tag = BeautifulSoup(str(td), "html.parser").a
                if a_tag:
                    pdf_url = escape_string(str(a_tag.get('href')))
                else:
                    pdf_url = None

        if select_count_query(str(court_name), str(case_id), 'judgment_date', judgment_date):
            pdf_filename = slugify(court_name + '-' + case_id + '-' + judgment_date) + '.pdf'
            text_filename = slugify(court_name + '-' + case_id + '-' + judgment_date) + '.txt'

            pdf_filepath = request_pdf(pdf_url, pdf_filename, court_name, bench_id, case_id)
            if pdf_filepath is not None:

                pdf_text_data = escape_string(str(pdf_to_text_api(pdf_filepath)))
                if pdf_text_data is not None:
                    text_filepath = module_directory + "/../data_files/text_files/" + court_name + '_' + text_filename
                    fw = open(text_filepath, "w")
                    fw.write(pdf_text_data)
                else:
                    text_filepath = None
                    text_filename = None
            else:
                text_filepath = None
                pdf_text_data = None
                pdf_filename = None

            if insert_query(
                    "INSERT INTO national_company_law_appellate_tribunal (case_id, judgment_date, party, section, "
                    "court_name, order_passed_by, pdf_url, pdf_filename, text_filename, bench) VALUES (%s, %s, %s, %s, "
                    "%s, %s, %s, %s, %s, %s)", (case_id, judgment_date, party, section, court_name_, order_passed_by,
                                                pdf_url, pdf_filename, text_filename, bench_id)):

                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, bench_id, case_id, 'Failed to insert court data in table'))

            if update_query("UPDATE national_company_law_appellate_tribunal SET text_data=%s WHERE case_id=%s",
                            (pdf_text_data, case_id)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, bench_id, case_id, 'Failed to insert text data.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))

            if transfer_to_bucket('PDF_Files', pdf_filepath):
                update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))
                os.remove(pdf_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, bench_id, case_id, 'Failed to transfer pdf to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))

            if transfer_to_bucket('Text_Files', text_filepath):
                update_query("UPDATE tracker SET transferred_text=transferred_text+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))
                os.remove(text_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, bench, case_id, error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, bench_id, case_id, 'Failed to transfer text to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s AND bench=%s",
                             (court_name, bench_id))

        else:
            update_query("UPDATE tracker SET inserted_cases=inserted_cases+1, no_pdf=no_pdf+1, no_text=no_text+1,"
                         "transferred_pdf=transferred_pdf+1, transferred_text=transferred_text+1 WHERE court_name=%s "
                         "AND bench=%s", (court_name, bench_id))


def request_data(base_url, headers, court_name, bench_id):
    start_date = None
    try:
        response = None
        querystring = {"page_id": "225"}

        start_date = select_one_query("SELECT end_date FROM tracker WHERE court_name=%s and bench=%s",
                                      (court_name, bench_id))['end_date']

        today = datetime.datetime.now()

        while datetime.datetime.strptime(str(start_date), "%m/%d/%Y") <= today:
            emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s and bench=%s",
                                              (court_name, bench_id))
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker_bench(court_name, bench_id)
                return True

            update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s and bench=%s",
                         (court_name, bench_id))
            no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s and bench=%s",
                                        (court_name, bench_id))['no_tries']
            while no_tries < NO_TRIES:
                update_query("UPDATE tracker SET total_cases=0, inserted_cases=0, no_pdf=0, no_text=0, "
                             "transferred_pdf=0, transferred_text=0 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))

                payload = "from_date=" + start_date + \
                          "&to_date=" + start_date + \
                          "&court=" + str(bench_id) + \
                          "&fifth=fifth"

                response = requests.request("POST", base_url, data=payload, params=querystring, headers=headers,
                                            proxies=proxy_dict).text

                if "no record found" in response.lower():
                    update_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s and bench=%s",
                                 (court_name, bench_id))
                else:
                    parser(court_name, bench_id, response)
                    check_cases = select_one_query("SELECT total_cases, inserted_cases FROM tracker "
                                                   "WHERE court_name=%s AND bench=%s", (court_name, bench_id))

                    if check_cases['total_cases'] == check_cases['inserted_cases']:
                        break

                no_tries += 1
                update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s and bench=%s",
                             (no_tries, court_name, bench_id))

            if no_tries == NO_TRIES:
                insert_query("INSERT INTO alerts (court_name, bench, start_date, error_message) VALUES "
                             "(%s, %s, %s, %s)", (court_name, bench_id, start_date, str(response)))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                             (court_name, bench_id))

            update_query("UPDATE tracker SET end_date=%s WHERE court_name=%s and bench=%s",
                         (start_date, court_name, bench_id))
            create_transfer_json_bench(court_name, bench_id)
            update_history_tracker_bench(court_name, bench_id)
            start_date = (datetime.datetime.strptime(str(start_date), "%m/%d/%Y") + datetime.timedelta(days=DAYS)
                          ).strftime("%m/%d/%Y")

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, bench, start_date, error_message) VALUES (%s, %s, %s, %s)",
                     (court_name, bench_id, start_date, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                     (court_name, bench_id))
        return False


def main(court_name, bench):
    logs.initialize_logger("national_company_law_appellate_tribunal")
    base_url = "https://nclat.nic.in/"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Cache-Control': "no-cache",
    }
    return request_data(base_url, headers, court_name, bench)
