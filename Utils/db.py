import json
import logging
import os
import traceback
import pymysql.cursors

from math import floor

module_directory = os.path.dirname(__file__)


def db_connect():
    return pymysql.connect(host="localhost",
                           user="root",
                           # password="root",
                           password="Future@4",
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


def select_json_query(table_name, start_date, end_date):
    db = db_connect()
    try:
        update_query("DELETE FROM Tracker_JSON WHERE Name = '" + table_name + "'")
        insert_query("INSERT INTO Tracker_JSON (Name, Start_Date, End_Date, No_Files, emergency_exit, "
                     "status) VALUES ('" + table_name + "', '" + start_date + "', '" + end_date + "', 0, false, "
                                                                                                  "'IN_RUNNING')")

        cursor = db.cursor()
        cursor.execute("select count(id) as num_rows from " + str(table_name))
        result = cursor.fetchall()
        cursor.close()
        no_rows = result[0]['num_rows']

        no_of_data_per_iteration = 1000
        no_of_iteration = floor(int(no_rows) / no_of_data_per_iteration) + 1

        for i in range(0, no_of_iteration):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM " + str(table_name) + " LIMIT " + str(no_of_data_per_iteration) +
                           " OFFSET " + str(i * no_of_data_per_iteration))
            result = cursor.fetchall()
            cursor.close()

            file_path = module_directory + "/../Data_Files/JSON_Files/" + str(table_name) + "_" + str(i) + ".json"
            fw = open(file_path, "w")
            fw.write(json.dumps(result))

            update_query("UPDATE Tracker_JSON SET No_Files=No_Files+1 WHERE Name='" + table_name + "'")

        update_query("UPDATE Tracker_JSON SET status='IN_SUCCESS', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        db.close()

        return True

    except Exception as e:
        update_query("UPDATE Tracker_JSON SET status='IN_FAILED', emergency_exit=true WHERE Name='" +
                     table_name + "'")
        traceback.print_exc()
        logging.error("Failed select query: %s", e)
        db.close()
        return False
