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
from new.utils.contants import NO_TRIES, DAYS
from new.utils.db import insert_query, update_history_tracker, select_one_query, update_query, select_count_query
from new.utils.extract_text import pdf_to_text_api, image_to_text_api
from new.utils.json_utils import create_transfer_json
from new.utils.my_proxy import proxy_dict


module_directory = os.path.dirname(__file__)
base_url = "https://phhc.gov.in"


def request_pdf(url, headers, pdf_name, court_name, case_id):
    try:
        if url is not None:
            no_tries = 0
            while no_tries < NO_TRIES:
                response = requests.get(base_url + '/include/captcha.php', headers=headers, proxies=proxy_dict)
                payload = 'vercode=' + image_to_text_api(response.content, court_name).lower() + '&submit=Submit'

                response = requests.request("POST", url, data=payload, headers=headers, verify=False,
                                            proxies=proxy_dict)
                if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                    file_path = module_directory + "/../data_files/pdf_files/" + court_name + "_" + pdf_name
                    fw = open(file_path, "wb")
                    fw.write(response.content)
                    update_query("UPDATE tracker SET no_pdf=no_pdf+1 WHERE court_name=%s", (court_name))
                    return file_path
                else:
                    no_tries += 1

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


def parser(html_str, court_name, headers):
    soup = BeautifulSoup(html_str, "html.parser")
    table_list = soup.find_all('table', {'id': 'tables11'})
    table_soup = BeautifulSoup(str(table_list), "html.parser")
    tr_list = table_soup.find_all('tr')

    tr_count = 0
    for tr in tr_list:
        emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
        if emergency_exit is not None:
            if emergency_exit['emergency_exit'] == 1:
                break

        tr_count += 1
        if tr_count <= 3:
            continue

        case_id = None
        petitioner = None
        respondent = None
        judgment_date = None
        pdf_url = None

        table_soup = BeautifulSoup(str(tr), "html.parser")
        td_list = table_soup.find_all('td')

        i = 0
        for td in td_list:
            i += 1
            if i == 1:
                continue
            elif i == 2:
                a_tag = BeautifulSoup(str(td), "html.parser").a
                case_id = escape_string(str(a_tag.text))
            elif i == 3:
                party = str(td.decode_contents()).split("Vs")
                petitioner = escape_string(str(party[0]))
                respondent = escape_string(str(party[1]))
            elif i == 4:
                judgment_date = escape_string(str(td.decode_contents()))
            elif i == 5:
                a_link = BeautifulSoup(str(td), "html.parser").a.get('onclick')
                a_formatted = str(str(a_link).replace("window.open('", "")).replace("')", "")
                pdf_url = escape_string(base_url + "/" + a_formatted)

        if select_count_query(str(court_name), str(case_id), 'judgment_date', judgment_date):
            pdf_filename = escape_string(slugify(case_id + '-' + judgment_date)) + '.pdf'
            text_filename = escape_string(slugify(case_id + '-' + judgment_date)) + '.txt'
            pdf_filepath = request_pdf(pdf_url, headers, pdf_filename, court_name, case_id)

            if pdf_filepath is not None:
                pdf_text_data = escape_string(str(pdf_to_text_api(pdf_filepath)))
                text_filepath = module_directory + "/../data_files/text_files/" + court_name + "_" + text_filename
                fw = open(text_filepath, "w")
                fw.write(pdf_text_data)
            else:
                text_filepath = None
                pdf_text_data = None

            if insert_query(
                    "INSERT INTO punjab_haryana (case_id, judgment_date, petitioner, respondent, pdf_url, "
                    "pdf_filename, text_filename) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (case_id, judgment_date, petitioner, respondent, pdf_url, pdf_filename, text_filename)):
                update_query("UPDATE tracker SET inserted_cases=inserted_cases+1 WHERE court_name=%s", (court_name))
            else:
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
                insert_query("INSERT INTO alerts (court_name, case_id, error_message) VALUES (%s, %s, %s)",
                             (court_name, case_id, 'Failed to insert court data in table'))

            if update_query("UPDATE punjab_haryana SET text_data=%s WHERE case_id=%s", (pdf_text_data, case_id)):
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


def request_data(court_name, headers):
    start_date = None
    response = None
    try:
        url = base_url + "/home.php"
        start_date = select_one_query("SELECT end_date FROM tracker WHERE court_name=%s", (court_name))['end_date']
        today = datetime.datetime.now()

        while datetime.datetime.strptime(str(start_date), "%d/%m/%Y") <= today:
            emergency_exit = select_one_query("SELECT emergency_exit FROM tracker WHERE court_name=%s", (court_name))
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            update_query("UPDATE tracker SET no_tries=0, no_alerts=0 WHERE court_name=%s", (court_name))
            no_tries = select_one_query("SELECT no_tries FROM tracker WHERE court_name=%s", (court_name))['no_tries']

            while no_tries < NO_TRIES:
                update_query("UPDATE tracker SET total_cases=0, inserted_cases=0, no_pdf=0, no_text=0, "
                             "transferred_pdf=0, transferred_text=0 WHERE court_name=%s", (court_name))

                querystring = {"search_param": "free_text_search_judgment"}
                payload = "t_case_type=" \
                          "&t_case_year=" \
                          "&submit=Search%20Case" \
                          "&from_date=" + str(start_date) + \
                          "&to_date=" + str(start_date) + \
                          "&pet_name=" \
                          "&res_name=" \
                          "&free_text=JUSTICE"

                response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                            proxies=proxy_dict).text

                if "no case found" in response.lower():
                    update_query("UPDATE tracker SET no_nodata=no_nodata+1 WHERE court_name=%s", (court_name))
                else:
                    parser(response, court_name, headers)
                    check_cases = select_one_query(
                        "SELECT total_cases, inserted_cases FROM tracker WHERE court_name=%s", (court_name))
                    if check_cases['total_cases'] == check_cases['inserted_cases']:
                        break

                no_tries += 1
                update_query("UPDATE tracker SET no_tries=%s WHERE court_name=%s", (no_tries, court_name))

            if no_tries == NO_TRIES:
                insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES (%s, %s, %s)",
                             (court_name, start_date, str(response)))
                update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))

            update_query("UPDATE tracker SET end_date=%s WHERE court_name=%s", (start_date, court_name))
            create_transfer_json(court_name)
            update_history_tracker(court_name)
            start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=DAYS)
                          ).strftime("%d/%m/%Y")
        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to request: %s", e)
        insert_query("INSERT INTO alerts (court_name, start_date, error_message) VALUES (%s, %s, %s)",
                     (court_name, start_date, str(e)))
        update_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s", (court_name))
        return False


def main(court_name):
    logs.initialize_logger("punjab_haryana")
    r = requests.request('GET', base_url, proxies=proxy_dict)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cookie': 'PHPSESSID=' + str(requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']),
        'Cache-Control': "no-cache",
    }
    return request_data(court_name, headers)
