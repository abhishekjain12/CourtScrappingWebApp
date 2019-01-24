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
from new.utils.db import select_count_query, insert_query, update_query, \
    select_one_query, update_history_tracker

module_directory = os.path.dirname(__file__)


def request_pdf(url, jud_pdf_name, court_name, case_id):
    try:
        response = requests.request("GET", url, proxies=proxy_dict)
        print(response.__dict__)
        if response.status_code == 200:
            if response.url == "http://gstcouncil.gov.in/":
                logging.error("Failed to get pdf file for: " + str(jud_pdf_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to download PDF File.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                return None
            else:
                file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + slugify(jud_pdf_name) + \
                            '.pdf'
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

    except Exception as e:
        logging.error("Failed to get pdf file for: " + str(jud_pdf_name) + ". Error: %s", e)
        insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                     (court_name, case_id, 'Failed to download PDF File.'))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return None


def parser(court_name, page_no, response):

    soup = BeautifulSoup(response, "html.parser")

    div_of_table = BeautifulSoup(str(soup.find(id="block-system-main")), "html.parser")

    table_body = BeautifulSoup(str(div_of_table.find("tbody")), "html.parser")

    table_last_row = BeautifulSoup(str(table_body.find("tr", class_="views-row-last")), "html.parser")

    table_last_td_sr = BeautifulSoup(str(table_last_row.find("td", class_="views-field-counter")), "html.parser")

    total_cases = int(table_last_td_sr.get_text())

    update_query("UPDATE tracker SET total_cases=%s, inserted_cases=0 WHERE court_name=%s",
                 (total_cases, court_name))

    table_rows = table_body.find_all("tr")
    for row in table_rows:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        s_no = None
        state = None
        applicant = None
        question = None
        case_id = None
        pdf_url = None
        category_sgst = None
        order_and_date = None
        order_date = None
        pdf_text_data = None

        row = BeautifulSoup(str(row), "html.parser")
        total_td = row.find_all("td")
        for td in total_td:
            td_soup = BeautifulSoup(str(td), "html.parser")
            if str(td['class'][1]) == "views-field-counter":
                s_no = escape_string(str(td.decode_contents()))
            if str(td['class'][1]) == "views-field-field-state-ut":
                state = escape_string(str(td.decode_contents()))
            if str(td['class'][1]) == "views-field-field-name-of-applicant":
                applicant = escape_string(str(td.decode_contents()))
            if str(td['class'][1]) == "views-field-field-question-s-on-which-advanc":
                p = td_soup.find('p')
                p_soup = BeautifulSoup(str(p), "html.parser")
                question = escape_string(str(p_soup.get_text()))
            if str(td['class'][1]) == "views-field-field-order-no-date":
                text = escape_string(str(td.decode_contents()))
                if 'dated' in text:
                    order_and_date = text.split('dated')
                if 'Dated' in text:
                    order_and_date = text.split('Dated')
                if 'dt' in text:
                    order_and_date = text.split('dt')
                if 'Dt' in text:
                    order_and_date = text.split('Dt')
                if 'dtd' in text:
                    order_and_date = text.split('dtd')
                if 'Dtd' in text:
                    order_and_date = text.split('Dtd')

                case_id = order_and_date[0]
                print(case_id)
                order_date = order_and_date[1]

                # if ':' in order_date:
                #     print(order_date)
                #     order_date = order_date[order_date.index(":"):]
                # if '.' in order_date:
                #     order_date = order_date[order_date.index("."):]

            elif str(td['class'][1]) == "views-field-php":
                a = td_soup.find('a')
                pdf_url = a['href']

            elif str(td['class'][1]) == "views-field-field-category-as-per-section-97":
                category_sgst = escape_string(str(td.decode_contents()))

        if select_count_query(str(court_name), str(case_id), 'date', order_date):
            pdf_filename = slugify('advance-authority-' + case_id + order_date) + '.pdf'
            text_filename = slugify('advance-authority-' + case_id + order_date) + '.txt'
            pdf_filepath = request_pdf(pdf_url, pdf_filename, court_name, case_id)
            if pdf_filepath is None:
                logging.error("Failed to convert text file for: " + str(case_id))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to download PDF File.'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
            else:
                pdf_text_data = escape_string(pdf_to_text_api(pdf_filepath))
                text_filepath = module_directory + "/../data_files/text_files/" + court_name + '_' + text_filename

                fw = open(text_filepath, "w")
                fw.write(pdf_text_data)

            if insert_query("INSERT INTO gst_advance_authority (s_no, state_ut,"
                            " name_of_applicant, questions, case_id, date, category_as_per_sgst_act, "
                            "pdf_url, pdf_filename, text_filename, text_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            , (s_no, state, applicant, question, case_id, order_date, category_sgst, pdf_url,
                               pdf_filename, text_filename, pdf_text_data)):
                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s", (court_name))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and page_no", (court_name,
                                                                                                          page_no))
                insert_query("INSERT INTO alerts (court_name, case_id, page_no,error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, case_id, page_no, 'Failed to insert court data in table'))
            if update_query("UPDATE gst_advance_authority SET text_data=%s WHERE case_id=%s", (pdf_text_data, case_id)):
                update_query("UPDATE tracker SET no_text=no_text+1 WHERE court_name=%s", (court_name))
            else:
                insert_query("INSERT INTO alerts (court_name, case_id, page_no,error_message) VALUES (%s, %s, %s, %s)",
                             (court_name, case_id, page_no, 'Failed to insert court data in table'))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and page_no", (court_name,
                                                                                                          page_no))
        else:
            update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s", (court_name))


def request_data(base_url, court_name):
    page_no = None
    try:
        response = None

        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s ", court_name)
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
        response = response.text
        parser(court_name, page_no, response)
        # soup = BeautifulSoup(response, "html.parser")
        #
        # last_page_li = soup.find_all("li", class_="pager-last last")  # getting last page_ no depends on css so if court
        #                                                                 # site change this can be a problem
        #
        # last_page_li_parser = BeautifulSoup(str(last_page_li), "html.parser")
        # last_page_link = last_page_li_parser.find("a")
        #
        # last_page_no = int(str(last_page_link['href'])[str(last_page_link['href']).find('=') + 1:])
        #
        # while page_no <= last_page_no:
        #     update_query("UPDATE tracker SET page_no=%s WHERE court_name=%s", (page_no, court_name))
        #     no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s",
        #                                 court_name)['no_tries']
        #
        #     url = base_url + "?page=" + str(page_no)
        #     response = requests.request("GET", url, headers=headers, proxies=proxy_dict)
        #     response = response.text
        #
        #     while no_tries < NO_TRIES:
        #         parser(base_url, court_name, page_no, response)
        #         check_cases = select_one_query("SELECT total_cases, inserted_cases FROM tracker "
        #                                        "WHERE court_name=%s", court_name)
        #         if check_cases['total_cases'] == check_cases['inserted_cases']:
        #             break
        #
        #         no_tries += 1
        #         update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s",
        #                      (no_tries, court_name))
        #
        #         if no_tries == NO_TRIES:
        #             insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES "
        #                          "(%s, %s, %s, %s)", (court_name, page_no, 'Tries Exceeded'))
        #             update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s",
        #                          court_name)
        #
        #     page_no += 1

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, page_no, error_message) VALUES (%s, %s, %s)",
                     (court_name, page_no, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s",
                     court_name)
        return False


def main(court_name):
    logs.initialize_logger("ruling_by_advance_authority")
    base_url = "http://gstcouncil.gov.in/rulings-by-advance-authority"
    return request_data(base_url, court_name)


main('gst_advance_authority')
