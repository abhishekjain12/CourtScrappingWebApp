import json
import logging
import os
import traceback
import pymysql.cursors

from math import floor

import requests

from Utils.my_proxy import proxy_dict
from common import transfer_to_bucket

module_directory = os.path.dirname(__file__)


def db_connect():
    return pymysql.connect(host="localhost",
                           user="root",
                           password="krypton212",
                           db="Courts_Data",
                           # charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def insert_query(sql):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed insert query: %s", e)
        db.rollback()
        db.close()


def update_query(sql):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed update query: %s", e)
        db.rollback()
        db.close()


def update1_query(sql):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed update query: %s", e)
        db.rollback()
        db.close()


def update_history_tracker(table_name):
    result = select_one_query("SELECT * FROM Tracker WHERE Name='" + table_name + "' ORDER BY id LIMIT 1")
    insert_query("INSERT INTO Tracker_History (Name, bench, No_Cases, Start_Date, End_Date, No_Error, No_Year_Error, "
                 "No_Year_NoData, emergency_exit, status) VALUES ('" + str(result['Name']) + "', '" +
                 str(result['bench']) + "', " + str(result['No_Cases']) + ", '" + str(result['Start_Date']) +
                 "', '" + str(result['End_Date']) + "', " + str(result['No_Error']) + ", " +
                 str(result['No_Year_Error']) + ", " + str(result['No_Year_NoData']) + ", true, '" +
                 str(result['status']) + "')")


def update_history_tracker_json(table_name):
    result = select_one_query("SELECT * FROM Tracker_JSON WHERE Name='" + table_name + "' ORDER BY id LIMIT 1")
    insert_query("INSERT INTO Tracker_History_JSON (Name, Start_Date, End_Date, No_Files, emergency_exit, "
                 "status) VALUES ('" + str(result['Name']) + "', '" + str(result['Start_Date']) + "', '" +
                 str(result['End_Date']) + "', " + str(result['No_Files']) + ", true, '" + str(result['status']) + "')")


def select_query(query):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if result:
            return result
        else:
            return None

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select query: %s", e)
        db.close()
        return None


def get_tables_info():
    try:
        queries = select_query("""select concat("select '",table_name,"' as name, count(id) from ",table_name) as `query`
        from `information_schema`.`tables` WHERE `table_schema` = 'Courts_Data'""")

        result = []
        for query in queries:
            res = select_one_query(query['query'])
            result.append(res)

        if result:
            return result
        else:
            return None

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed get_tables_info query: %s", e)
        return None


def select_one_query(query):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return result
        else:
            return None

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select one query: %s", e)
        db.close()
        return None


def select_count_query(table_name, case_no):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT count(case_no) FROM " + str(table_name) + " WHERE case_no = '" + str(case_no) + "'")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result[0]['count(case_no)']:
            return True
        else:
            return False

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select count query: %s", e)
        db.close()
        return False


def select_count_query_other(table_name, col_name, value):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT count(" + str(col_name) + ") FROM " + str(table_name) + " WHERE " + str(col_name) +
                       " = '" + str(value) + "'")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result[0]['count(' + str(col_name) + ')']:
            return True
        else:
            return False

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select count query: %s", e)
        db.close()
        return False


def select_json_query(table_name, start_date, end_date):
    db = db_connect()
    try:
        update_query("UPDATE Tracker_JSON SET Start_Date='" + start_date + "', End_Date='" + end_date +
                     "', No_Files=0, emergency_exit=false, status='IN_RUNNING' WHERE Name='" + table_name + "'")

        cursor = db.cursor()
        cursor.execute("select count(id) as num_rows from " + str(table_name) + " WHERE is_json=0")
        result = cursor.fetchall()
        cursor.close()
        no_rows = result[0]['num_rows']

        no_of_data_per_iteration = 1000
        no_of_iteration = floor(int(no_rows) / no_of_data_per_iteration) + 1

        j_count = select_one_query("SELECT json_count FROM Tracker_JSON WHERE Name='" + table_name + "'")['json_count']

        for i in range(0, no_of_iteration):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM " + str(table_name) + " WHERE is_json=0 LIMIT " +
                           str(no_of_data_per_iteration) + " OFFSET " + str(i * no_of_data_per_iteration))
            result = cursor.fetchall()
            cursor.close()

            file_path = module_directory + "/../Data_Files/JSON_Files/" + str(table_name) + "-" + \
                        str(i + 1 + j_count) + ".json"
            fw = open(file_path, "w")
            fw.write(json.dumps(result))

            for record in result:
                update_query("UPDATE " + table_name + " SET is_json=1 WHERE id='" + str(record['id']) + "'")

            update_query("UPDATE Tracker_JSON SET No_Files=No_Files+1, json_count=json_count+1 WHERE Name='" +
                         table_name + "'")

        update_query("UPDATE Tracker_JSON SET status='IN_SUCCESS', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        update_history_tracker_json(table_name)
        db.close()

        return True

    except Exception as e:
        update_query("UPDATE Tracker_JSON SET status='IN_FAILED', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        traceback.print_exc()
        logging.error("Failed select query: %s", e)
        db.close()
        return False


def download_pdf_to_bucket(table_name):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("select count(id) as num_rows from " + str(table_name) + " WHERE is_pdf=0")
        result = cursor.fetchall()
        cursor.close()
        no_rows = result[0]['num_rows']

        no_of_data_per_iteration = 5000
        no_of_iteration = floor(int(no_rows) / no_of_data_per_iteration) + 1

        for i in range(0, no_of_iteration):
            cursor = db.cursor()
            cursor.execute("SELECT id, case_no, pdf_file, pdf_filename FROM " + str(table_name) +
                           " WHERE is_pdf=0 LIMIT " + str(no_of_data_per_iteration) + " OFFSET " +
                           str(i * no_of_data_per_iteration))
            result = cursor.fetchall()
            cursor.close()

            for record in result:
                if str(record['pdf_file']).upper() != 'NULL' and record['pdf_file'] is not None:
                    filename = "/home/karaa_krypt/CourtScrappingWebApp/Data_Files/PDF_Files/" + \
                               str(record['pdf_filename'])

                    response = requests.request("GET", str(record['pdf_file']), proxies=proxy_dict)
                    if response.status_code == 200:
                        res = response.text
                        if "no data found" in res.lower():
                            logging.error("No data for: " + str(record['pdf_filename']))
                            return str("NULL")
                        fw = open(filename, "wb")
                        fw.write(response.content)

                        if transfer_to_bucket('PDF_Files', filename):
                            os.remove(filename)

                        update_query("UPDATE " + table_name + " SET is_pdf=1 WHERE id='" + str(record['id']) + "'")
                        update_query("UPDATE Tracker_pdf SET No_Files=No_Files+1 WHERE Name='" + table_name + "'")

        update_query("UPDATE Tracker_pdf SET status='IN_SUCCESS', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        db.close()
        return True

    except Exception as e:
        logging.error("Failed download_pdf_to_bucket: %s", e)
        update_query("UPDATE Tracker_pdf SET status='IN_FAILED', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        traceback.print_exc()
        db.close()
        return False
