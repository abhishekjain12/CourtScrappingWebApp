import os
import requests
import traceback
import logging

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify
from new.utils import logs
from new.utils.bucket import transfer_to_bucket
from new.utils.contants import NO_TRIES
from new.utils.extract_text import pdf_to_text_api
from new.utils.my_proxy import proxy_dict
from new.utils.db import select_count_query, insert_query, select_one_query, update_history_tracker, update_query

module_directory = os.path.dirname(__file__)


def request_pdf(url, jud_pdf_name, court_name, case_id):
    try:
        if url is not None:
            response = requests.request("GET", url, proxies=proxy_dict)
            if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + \
                            slugify(jud_pdf_name) + '.pdf'
                fw = open(file_path, "wb")
                fw.write(response.content)
                update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s", (court_name))
                return file_path
            else:
                logging.error("Failed to get pdf file for: " + str(jud_pdf_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to download PDF File.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                return None
        else:
            logging.error("Failed to get pdf file for: " + str(jud_pdf_name))
            insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                         (court_name, case_id, 'Failed to download PDF File. No url.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(jud_pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                     (court_name, case_id, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return None


def parser(base_url, court_name, response):
    table = BeautifulSoup(response, "html.parser").find_all('table', {'class': 'custum-tbl table table-bordered'})[0]
    tbody = BeautifulSoup(str(table), "html.parser").find_all('tbody')[0]
    tr_list = BeautifulSoup(str(tbody), "html.parser").find_all('tr')

    update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0, no_pdf=0, no_text=0, transferred_pdf=0,"
                 "transferred_text=0 WHERE court_name=%s", (str(len(tr_list)), court_name))

    for tr in tr_list:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        state = None
        name_of_appellant = None
        brief_of_order_in_appeal = None
        appeal_order_no = None
        appeal_order_date = None
        pdf_url = None
        aar_order_no = None
        aar_order_date = None
        aar_pdf_url = None

        i = 0
        td_list = BeautifulSoup(str(tr), "html.parser").find_all('td')
        for td in td_list:
            i += 1
            if i == 2:
                state = escape_string(str(td.decode_contents()))
            elif i == 3:
                name_of_appellant = escape_string(str(td.decode_contents()))
            elif i == 4:
                brief_of_order_in_appeal = escape_string(str(td.decode_contents()))
            elif i == 5:
                appeal_order = str(td.decode_contents()).lower()
                if 'dated' in appeal_order:
                    appeal_order = appeal_order.split('dated')
                elif 'dt.' in appeal_order:
                    appeal_order = appeal_order.split('dt.')

                appeal_order_no = escape_string(appeal_order[0])
                appeal_order_date = escape_string(appeal_order[1])

            elif i == 6:
                a_tag = BeautifulSoup(str(td), "html.parser").a
                pdf_url = escape_string(str(base_url + a_tag.get('href')))

            elif i == 7:
                if str(td.decode_contents()) != '-':
                    a_tag = BeautifulSoup(str(td), "html.parser").a
                    aar_pdf_url = escape_string(str(a_tag.get('href')))
                    aar_order = str(a_tag.decode_contents()).lower()
                    if 'dated' in aar_order:
                        aar_order = aar_order.split('dated')
                    elif 'dt.' in aar_order:
                        aar_order = aar_order.split('dt.')
                    elif 'dtd.' in aar_order:
                        aar_order = aar_order.split('dtd.')

                    aar_order_no = escape_string(aar_order[0])
                    aar_order_date = escape_string(aar_order[1])

        if select_count_query(str(court_name), str(appeal_order_no), 'appeal_order_date', appeal_order_date):
            pdf_filename = slugify('appeal-' + appeal_order_no + appeal_order_date) + '.pdf'
            text_filename = slugify('appeal-' + appeal_order_no + appeal_order_date) + '.txt'

            pdf_filepath = request_pdf(pdf_url, pdf_filename, court_name, appeal_order_no)
            if pdf_filepath is not None:
                pdf_text_data = escape_string(str(pdf_to_text_api(pdf_filepath)))

                text_filepath = module_directory + "/../data_files/text_files/" + court_name + '_' + text_filename
                fw = open(text_filepath, "w")
                fw.write(pdf_text_data)
            else:
                text_filepath = None
                pdf_text_data = None

            if aar_order_no is not None:
                aar_pdf_filename = slugify('aar-' + aar_order_no + aar_order_date) + '.pdf'
                aar_text_filename = slugify('aar-' + aar_order_no + aar_order_date) + '.txt'

                aar_pdf_filepath = request_pdf(aar_pdf_url, aar_pdf_filename, court_name, aar_order_no)
                if aar_pdf_filepath is not None:
                    aar_text_data = escape_string(pdf_to_text_api(aar_pdf_filepath))

                    aar_text_filepath = module_directory + "/../data_files/text_files/" \
                                                           "" + court_name + '_' + aar_text_filename
                    fw = open(aar_text_filepath, "w")
                    fw.write(aar_text_data)
                else:
                    aar_text_filepath = None
                    aar_text_data = None
            else:
                aar_pdf_filename = None
                aar_text_filename = None
                aar_text_data = None
                aar_pdf_filepath = None
                aar_text_filepath = None

            if insert_query(
                    "INSERT INTO gst_appellate (case_id, appeal_order_no, appeal_order_date, name_of_appellant, "
                    "brief_of_order_in_appeal, state, aar_order_no, aar_order_date, pdf_url, pdf_filename, "
                    "text_filename, aar_pdf_url, arr_pdf_filename, aar_text_filename) VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (appeal_order_no, appeal_order_no, appeal_order_date, name_of_appellant, brief_of_order_in_appeal,
                     state, aar_order_no, aar_order_date, pdf_url, pdf_filename, text_filename, aar_pdf_url,
                     aar_pdf_filename, aar_text_filename)):

                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s", (court_name))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, appeal_order_no, 'Failed to insert court data in table'))

            if update_query("UPDATE gst_appellate SET text_data=%s WHERE case_id=%s", (pdf_text_data, appeal_order_no)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", (court_name))
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, appeal_order_no, 'Failed to insert text data.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if update_query("UPDATE gst_appellate SET aar_text_data=%s WHERE case_id=%s",
                            (aar_text_data, appeal_order_no)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", (court_name))
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, appeal_order_no, 'Failed to insert aar text data.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if transfer_to_bucket('PDF_Files', pdf_filepath):
                update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 WHERE court_name=%s", (court_name))
                os.remove(pdf_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, appeal_order_no, 'Failed to transfer pdf to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if transfer_to_bucket('Text_Files', text_filepath):
                update_query("UPDATE tracker SET transferred_text=transferred_text+1 WHERE court_name=%s", (court_name))
                os.remove(text_filepath)
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, appeal_order_no, 'Failed to transfer text to bucket.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            if aar_order_no is not None:
                if transfer_to_bucket('PDF_Files', aar_pdf_filepath):
                    update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 WHERE court_name=%s",
                                 (court_name))
                    os.remove(aar_pdf_filepath)
                else:
                    insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                                 (court_name, appeal_order_no, 'Failed to transfer aar pdf to bucket.'))
                    update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

                if transfer_to_bucket('Text_Files', aar_text_filepath):
                    update_query("UPDATE tracker SET transferred_text=transferred_text+1 WHERE court_name=%s",
                                 (court_name))
                    os.remove(aar_text_filepath)
                else:
                    insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                                 (court_name, appeal_order_no, 'Failed to transfer aar text to bucket.'))
                    update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        else:
            update_query("UPDATE tracker SET inserted_cases=inserted_cases+1, no_pdf=no_pdf+1, no_text=no_text+1,"
                         "transferred_pdf=transferred_pdf+1, transferred_text=transferred_text+1 WHERE court_name=%s",
                         (court_name))


def request_data(base_url, court_name):
    try:
        url = base_url + "/orders-appellate-authority-advance-ruling"

        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit['emergency_exit'] == 1:
            update_history_tracker(court_name)
            return True

        update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s", (court_name))
        no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s", (court_name))['no_tries']

        while no_tries < NO_TRIES:
            response = requests.request("GET", url, proxies=proxy_dict)
            if response.status_code == 200:
                parser(base_url, court_name, str(response.text))
                check_cases = select_one_query("SELECT total_cases, inserted_cases FROM tracker WHERE court_name=%s",
                                               (court_name))
                if check_cases['total_cases'] == check_cases['inserted_cases']:
                    break

            elif response.status_code != 200 and no_tries == NO_TRIES:
                update_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s", (court_name))

            no_tries += 1
            update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s", (no_tries, court_name))

        if no_tries == NO_TRIES:
            insert_query("INSERT INTO alerts (court_name, error_message) VALUES (%s, %s)",
                         (court_name, 'Failed to get HTML.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

        update_history_tracker(court_name)
        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, error_message) VALUES (%s, %s)", (court_name, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return False


def main(court_name):
    logs.initialize_logger("gst_appellate")
    base_url = "http://gstcouncil.gov.in"
    return request_data(base_url, court_name)
