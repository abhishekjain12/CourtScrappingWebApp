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
from new.utils.json_utils import create_transfer_json
from new.utils.my_proxy import proxy_dict
from new.utils.db import insert_query, update_query, select_one_query, update_history_tracker, \
    select_count_query_with_extra_param, select_count_query

module_directory = os.path.dirname(__file__)


def request_pdf(url, jud_pdf_name, court_name, case_id, page_no):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
            file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + \
                        "_" + slugify(jud_pdf_name) + '.pdf'
            fw = open(file_path, "wb")
            fw.write(response.content)
            update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s", (court_name))
            return file_path
        else:
            logging.error("Failed to get pdf file for: " + str(jud_pdf_name))
            insert_query("INSERT INTO alerts (court_name, case_id, page_no, error_message) VALUES (%s, %s, %s, %s)",
                         (court_name, case_id, page_no, 'Failed to download PDF File.'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
            return None

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(jud_pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, case_id, page_no, error_message) VALUES (%s, %s, %s, %s)",
                     (court_name, case_id, page_no, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", court_name)
        return None


def parser(court_name, page_no, response):
    try:
        table_data = None
        soup = BeautifulSoup(response, "html.parser")
        tables = soup.find_all("table")
        i = 0
        for table in tables:
            i += 1
            if i == 5:
                table_data = table
                break
        table_data = BeautifulSoup(str(table_data), "html.parser")
        table_rows = table_data.find_all("tr")
        i = 0
        for table_row in table_rows:
            update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0, no_pdf=0, no_text=0, transferred_pdf=0,"
                         "transferred_text=0 WHERE court_name=%s", ((len(table_rows) - 1), court_name))
            if i == 0:
                i += 1
                continue
            else:
                emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s",
                                                  court_name)
                if emergency_exit is not None:
                    if emergency_exit['emergency_exit'] == 1:
                        break
                s_no = None
                country = None
                applicant = None
                case_id = None
                pdf_url = None
                ruling_date = None
                itr_taxman_ctr = None

                row = BeautifulSoup(str(table_row), "html.parser")
                total_td = row.find_all("td")
                j = 0
                for td in total_td:
                    td_soup = BeautifulSoup(str(td), "html.parser")
                    strong_text = td_soup.find('strong')
                    if j == 0:
                        if strong_text is not None:
                            s_no = escape_string(str(strong_text.decode_contents()))
                    elif j == 1:
                        if strong_text is not None:
                            case_id = escape_string(str(strong_text.decode_contents()))
                    elif j == 2:
                        if strong_text is not None:
                            ruling_date = escape_string(str(strong_text.decode_contents()))
                    elif j == 3:
                        if strong_text is not None:
                            applicant = escape_string(str(strong_text.decode_contents()))
                    elif j == 4:
                        if strong_text is not None:
                            country = escape_string(str(strong_text.decode_contents()))
                    elif j == 5:
                        if strong_text is not None:
                            itr_taxman_ctr = escape_string(str(strong_text.decode_contents()))
                    elif j == 6:
                        td_soup = BeautifulSoup(str(td), "html.parser")
                        if td_soup.a is not None:
                            a = td_soup.a
                            index_of_first_comma = str(a['href']).index("'")
                            index_of_last_comma = str(a['href']).rindex("'")
                            pdf_url = str(a['href'])[index_of_first_comma + 1: index_of_last_comma]
                    j += 1

                if select_count_query(str(court_name), str(escape_string(case_id)), 'date', ruling_date):
                    pdf_filepath = None
                    text_filename = None
                    pdf_final_url = None
                    pdf_filename = None
                    if pdf_url is not None:
                        pdf_filename = slugify('aar-rulings' + str(escape_string(case_id)) + str(ruling_date)) + '.pdf'
                        text_filename = slugify('aar-rulings-' + str(escape_string(case_id)) + str(ruling_date)) + '.txt'
                        pdf_final_url = 'http://aarrulings.in/it-rulings/uploads/pdf/' + pdf_url
                        pdf_filepath = request_pdf(pdf_final_url, pdf_filename, court_name, case_id, page_no)

                    if pdf_filepath is not None:
                        pdf_text_data = escape_string(str(pdf_to_text_api(pdf_filepath)))
                        text_filepath = module_directory + "/../data_files/text_files/" + court_name + '_' + text_filename
                        fw = open(text_filepath, "w")
                        fw.write(pdf_text_data)
                    else:
                        text_filepath = None
                        pdf_text_data = None
                        pdf_filename = None
                        text_filename = None

                    if insert_query("INSERT INTO aar_rulings (sl_no, case_id, date, country, "
                                    "itr_taxman_ctr, pdf_url, pdf_filename, text_filename) "
                                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (s_no, str(escape_string(case_id)), ruling_date, country,
                                     itr_taxman_ctr, pdf_final_url,
                                     pdf_filename, text_filename)):
                        update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s",
                                     court_name)
                    else:
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and page_no",
                                     (court_name, page_no))
                        insert_query("INSERT INTO alerts (court_name, case_id, page_no,error_message) VALUES "
                                     "(%s, %s, %s, %s)", (court_name, case_id, page_no,
                                                          'Failed to insert court data in table'))
                    if update_query("UPDATE aar_rulings SET name_of_applicant=%s WHERE case_id=%s",
                                    (applicant, case_id)):
                        update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", court_name)
                    else:
                        insert_query(
                            "INSERT INTO alerts (court_name, case_id, page_no,error_message) VALUES (%s, %s, %s,"
                            " %s)", (court_name, case_id, page_no, 'Failed to insert applicant name in table'))
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and page_no",
                                     (court_name, page_no))

                    if update_query("UPDATE aar_rulings SET text_data=%s WHERE case_id=%s",
                                    (pdf_text_data, case_id)):
                        update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", court_name)
                    else:
                        insert_query(
                            "INSERT INTO alerts (court_name, case_id, page_no,error_message) VALUES (%s, %s, %s,"
                            " %s)", (court_name, case_id, page_no, 'Failed to insert text data in table'))
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and page_no",
                                     (court_name, page_no))

                    if transfer_to_bucket('PDF_Files', pdf_filepath):
                        update_query("UPDATE tracker SET transferred_pdf=transferred_pdf+1 WHERE court_name=%s",
                                     court_name)
                        os.remove(pdf_filepath)
                    else:
                        insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                                     (court_name, case_id, 'Failed to transfer pdf to bucket.'))
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

                    if transfer_to_bucket('Text_Files', text_filepath):
                        update_query("UPDATE tracker SET transferred_text=transferred_text+1 WHERE court_name=%s",
                                     (court_name))
                        os.remove(text_filepath)
                    else:
                        insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                                     (court_name, case_id, 'Failed to transfer text to bucket.'))
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                else:
                    update_query(
                        "UPDATE tracker SET inserted_cases=inserted_cases+1, no_pdf=no_pdf+1, no_text=no_text+1, "
                        "transferred_pdf=transferred_pdf+1, transferred_text=transferred_text+1 WHERE "
                        "court_name=%s", court_name)

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES (%s, %s, %s)",
                     (court_name, page_no, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", court_name)
        return False


def request_data(base_url, court_name):
    page_no = 0
    try:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s ", court_name)
        if emergency_exit['emergency_exit'] == 1:
            update_history_tracker(court_name)
            return True

        page_no = select_one_query("SELECT page_no FROM tracker WHERE court_name=%s", court_name)['page_no']

        url = base_url + str(page_no)

        response = requests.request("GET", url)
        response = response.text
        if response.lower().__contains__("access denied"):
            print('Problem')
            insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES (%s, %s, %s)",
                         (court_name, page_no, 'IP has been Blacklisted'))
            update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", court_name)
            return False
        else:
            parser(court_name, page_no, response)
            soup = BeautifulSoup(response, "html.parser")
            last_page_a_tag = soup.find("a", string="Last ›")
            if last_page_a_tag is not None:
                last_page_link = str(last_page_a_tag['href'])
                last_page_no = int(last_page_link[int(last_page_link.rindex("/") + 1):])
            else:
                return True

            while page_no <= last_page_no:
                update_query("UPDATE tracker SET page_no=%s WHERE court_name=%s", (page_no, court_name))
                update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s", court_name)
                no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s", court_name)['no_tries']

                url = base_url + str(page_no)
                response = requests.request("GET", url, proxies=proxy_dict)
                response = response.text

                while no_tries < NO_TRIES:
                    update_query("UPDATE tracker SET total_cases=0, inserted_cases=0, no_pdf=0, no_text=0, "
                                 "transferred_pdf=0, transferred_text=0 WHERE court_name=%s", (court_name))
                    parser(court_name, page_no, response)
                    check_cases = select_one_query("SELECT total_cases, inserted_cases FROM tracker WHERE court_name=%s",
                                                   court_name)
                    if check_cases['total_cases'] == check_cases['inserted_cases']:
                        break

                    no_tries += 1
                    update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s", (no_tries, court_name))

                    if no_tries == NO_TRIES:
                        insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES (%s, %s, %s)",
                                    (court_name, page_no, 'Tries Exceeded'))
                        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", court_name)

                create_transfer_json(court_name)
                update_history_tracker(court_name)
                page_no += 20
        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES (%s, %s, %s)",
                     (court_name, page_no, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", court_name)
        return False


def main(court_name):
    logs.initialize_logger("aar_rulings")
    base_url = "http://aarrulings.in/it-rulings/ruling/display/"
    return request_data(base_url, court_name)

