import datetime
import os
import requests
import traceback
import logging

from bs4 import BeautifulSoup
from pymysql import escape_string
from slugify import slugify
from Utils import logs
from Utils.db import insert_query, update_query, select_one_query, update_history_tracker, select_count_query
from Utils.my_proxy import proxy_dict


# Bench_Code - Court Name
#   1	       High Court of Chattisgarh
#   2	       High Court of Hyderabad
#   3	       High Court of Jammu & Kashmir - Jammu Wing
#   4	       High Court of Jammu & Kashmir - Srinagar  Wing
#   5	       High Court of Kerala
#   6	       High Court of Madras
#   7	       High Court of Orissa


module_directory = os.path.dirname(__file__)

base_url = "http://judis.nic.in/HCS/"


def request_text(url, case_id, court_name):
    response = requests.request("POST", url, proxies=proxy_dict)
    if response.status_code == 200:
        res = response.text

        if "no data found" in res.lower():
            logging.error("No data for: " + str(case_id))
            return {'data': "NULL", 'url': url}

        soup = BeautifulSoup(res, "html.parser")
        text_area = soup.find_all('textarea')

        text_data = ""
        for data in text_area:
            text_data += data.decode_contents()

        file_path = module_directory + "/../Data_Files/Text_Files/" + court_name + "_" + slugify(case_id) + ".txt"
        fw = open(file_path, "w")
        fw.write(str(text_data))

        return {'data': text_data, 'url': url}
    else:
        logging.error("Failed to get text file for: " + str(case_id))
        return {'data': "NULL", 'url': url}


def request_pdf(url, case_id, court_name):
    response = requests.request("GET", url, proxies=proxy_dict)
    if response.status_code == 200:
        res = response.text

        if "no data found" in res.lower():
            logging.error("No data for: " + str(case_id))
            return str("NULL")

        file_path = module_directory + "/../Data_Files/PDF_Files/" + court_name + "_" + slugify(case_id) + ".pdf"
        fw = open(file_path, "wb")
        fw.write(response.content)

        return str(file_path)
    else:
        logging.error("Failed to get text file for: " + str(case_id))
        return str("NULL")


def parse_html(html_str, court_name):
    try:
        soup = BeautifulSoup(html_str, "html.parser")
        table_list = soup.find_all('table')

        for table in table_list:
            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit is not None:
                if emergency_exit['emergency_exit'] == 1:
                    break

            case_no = "NULL"
            petitioner = "NULL"
            respondent = "NULL"
            judgment_date = "NULL"
            judge_name = "NULL"
            text = "NULL"
            text_file = "NULL"
            pdf_file = "NULL"
            insert_check = False

            table_soup = BeautifulSoup(str(table), "html.parser")
            td_list = table_soup.find_all('td')

            i = 0
            for td in td_list:
                i += 1
                if i == 1:
                    case_no = escape_string(str(td.decode_contents()))

                if select_count_query(str(court_name), str(case_no)):
                    insert_check = True

                    if i == 2:
                        petitioner = escape_string(str(td.decode_contents()))
                    if i == 4:
                        respondent = escape_string(str(td.decode_contents()))
                    if i == 6:
                        judgment_date = escape_string(str(td.decode_contents()))
                    if i == 7:
                        judge_name = escape_string(str(td.decode_contents()))
                    if i == 8:
                        a_link = BeautifulSoup(str(td), "html.parser").a.get('href')
                        text_dir = request_text(base_url + a_link, case_no, court_name)
                        text = escape_string(text_dir['data'])
                        text_file = escape_string(text_dir['url'])
                    if i == 9:
                        a_link = BeautifulSoup(str(td), "html.parser").a.get('href')
                        pdf_file = escape_string(base_url + a_link)
                        pdf_file = escape_string(request_pdf(base_url + a_link, case_no, court_name))

            if case_no != "NULL" and insert_check and petitioner != 'Judgment Information System':
                sql_query = "INSERT INTO " + str(court_name) + \
                            " (case_no, petitioner, respondent, judgment_date, judge_name, text_data, text_file, " \
                            "pdf_file) VALUE ('" + case_no + "', '" + petitioner + "', '" + respondent + "', '" + \
                            judgment_date + "', '" + judge_name + "', '" + text + "', '" + text_file + "', '" + \
                            pdf_file + "')"
                insert_query(sql_query)

                update_query("UPDATE Tracker SET No_Cases = No_Cases + 1 WHERE Name = '" + str(court_name) + "'")

        return True

    except Exception as e:
        logging.error("Failed to parse the html: %s", e)
        update_query("UPDATE Tracker SET No_Error = No_Error + 1 WHERE Name = '" + str(court_name) + "'")
        return False


def request_data(court_name, bench_code, start_date, end_date_):
    try:
        url = base_url + "textqry_new.asp"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
            }

        i = 0
        while True:
            i += 1

            emergency_exit = select_one_query("SELECT emergency_exit FROM Tracker WHERE Name='" + court_name + "'")
            if emergency_exit['emergency_exit'] == 1:
                update_history_tracker(court_name)
                return True

            end_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y") + datetime.timedelta(days=180)
                        ).strftime("%d/%m/%Y")

            if datetime.datetime.strptime(end_date_, "%d/%m/%Y") + datetime.timedelta(days=180) < \
                    datetime.datetime.strptime(str(end_date), "%d/%m/%Y"):
                logging.error("DONE")
                break

            update_query("UPDATE Tracker SET Start_Date = '" + str(start_date) + "', End_Date = '" + str(end_date) +
                         "' WHERE Name = '" + str(court_name) + "'")

            payload = "action=validate_login" \
                      "&Bench_Code=" + str(bench_code) + \
                      "&party=jus" \
                      "&FromDt=" + str(start_date) + \
                      "&ToDt=" + str(end_date)

            response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy_dict)
            res = response.text

            if "no data found" in res.lower():
                logging.error("NO data Found for start date: " + str(start_date))
                update_query("UPDATE Tracker SET No_Year_NoData = No_Year_NoData + 1 WHERE Name = '" +
                             str(court_name) + "'")

                start_date = end_date
                continue

            if not parse_html(res, court_name):
                logging.error("Failed to parse data from date: " + str(start_date))

            start_date = end_date

        update_query("UPDATE Tracker SET status = 'IN_SUCCESS', emergency_exit=true WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get data from date: " + str(start_date))
        logging.error("Failed to request: %s", e)

        update_query("UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED' WHERE Name = '" +
                     str(court_name) + "'")
        update_history_tracker(court_name)

        return False


def main(court_name, bench_code, start_date, end_date):
    logs.initialize_logger("JUDIS")
    return request_data(court_name, bench_code, start_date, end_date)
