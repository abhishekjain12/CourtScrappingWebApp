import logging
import os
import traceback
import pymysql.cursors

module_directory = os.path.dirname(__file__)


def db_connect():
    return pymysql.connect(
        # host="localhost",
        host="35.226.213.76",
        user="root",
        # password="root",
        password="krypton212",
        db="new_courts_data",
        # charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def db_local_connect():
    return pymysql.connect(host="localhost",
                           user="root",
                           password="krypton212",
                           # password="root",
                           db="new_courts_data",
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


def insert_local_query(sql):
    db = db_local_connect()
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


def update_local_query(sql):
    db = db_local_connect()
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


def select_local_query(query):
    db = db_local_connect()
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


def select_one_local_query(query):
    db = db_local_connect()
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
