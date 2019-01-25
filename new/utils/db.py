import logging
import os
import traceback
import pymysql.cursors

module_directory = os.path.dirname(__file__)


def db_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        # password="root",
        password="krypton212",
        db="new_courts_data",
        # charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def insert_query(sql, data=None):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(sql, data)
        db.commit()
        cursor.close()
        db.close()
        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed insert query: %s", e)
        db.rollback()
        db.close()
        return False


def update_query(sql, data=None):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(sql, data)
        db.commit()
        cursor.close()
        db.close()
        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed update query: %s", e)
        db.rollback()
        db.close()
        return False


def select_query(query, data=None):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(query, data)
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


def select_one_query(query, data=None):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute(query, data)
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


def get_tables_info():
    try:
        queries = select_query("""select concat("select '",table_name,"' as name, count(id) from ",table_name) as 
        `query` from `information_schema`.`tables` WHERE `table_schema` = 'new_courts_data'""")

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


def select_count_query(table_name, case_id, date_col, date_val):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT count(case_id) FROM " + str(table_name) + " WHERE case_id = '" + str(case_id) +
                       "' AND " + str(date_col) + " = '" + str(date_val) + "'")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result[0]['count(case_id)']:
            return True
        else:
            return False

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select count query: %s", e)
        db.close()
        return False


def select_count_query_with_extra_param(table_name, case_id, date_col, date_val,
                                        extra_parameter_name_1, extra_val_1, extra_parameter_name_2, extra_val_2):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT count(case_id) FROM " + str(table_name) + " WHERE case_id = '" + str(case_id) +
                       "' AND " + str(date_col) + " = '" + str(date_val) + "'" + "AND " + str(extra_parameter_name_1)
                       + "= '" + str(extra_val_1) + "'" + "AND " + str(extra_parameter_name_2)
                       + "= '" + str(extra_val_2) + "'")

        result = cursor.fetchall()
        cursor.close()
        db.close()
        if not result[0]['count(case_id)']:
            return True
        else:
            return False

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed select count query: %s", e)
        db.close()
        return False


def update_history_tracker(court_name):
    r = select_one_query("SELECT * FROM tracker WHERE court_name=%s and bench=%s ORDER BY id LIMIT 1", (court_name))
    insert_query("INSERT INTO tracker_history (court_name, bench, start_date, end_date, no_tries, total_cases, "
                 "inserted_cases, no_nodata, no_alerts, no_pdf, no_text, no_json, transferred_pdf, transferred_text, "
                 "transferred_json, emergency_exit, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                 "%s, %s, %s, %s, %s, %s)",
                 (r['court_name'], r['bench'], r['start_date'], r['end_date'], r['no_tries'], r['total_cases'],
                  r['inserted_cases'], r['no_nodata'], r['no_alerts'], r['no_pdf'], r['no_text'], r['no_json'],
                  r['transferred_pdf'], r['transferred_text'], r['transferred_json'], r['emergency_exit'], r['status']))


def update_history_tracker_bench(court_name, bench):
    r = select_one_query("SELECT * FROM tracker WHERE court_name=%s and bench=%s ORDER BY id LIMIT 1",
                         (court_name, bench))

    insert_query("INSERT INTO tracker_history (court_name, bench, start_date, end_date, no_tries, total_cases, "
                 "inserted_cases, no_nodata, no_alerts, no_pdf, no_text, no_json, transferred_pdf, transferred_text, "
                 "transferred_json, emergency_exit, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                 "%s, %s, %s, %s, %s, %s)",
                 (r['court_name'], r['bench'], r['start_date'], r['end_date'], r['no_tries'], r['total_cases'],
                  r['inserted_cases'], r['no_nodata'], r['no_alerts'], r['no_pdf'], r['no_text'], r['no_json'],
                  r['transferred_pdf'], r['transferred_text'], r['transferred_json'], r['emergency_exit'], r['status']))
