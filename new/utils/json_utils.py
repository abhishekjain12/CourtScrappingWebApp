import json
import logging
import os
import traceback
from math import floor

from new.utils.bucket import transfer_to_bucket
from new.utils.db import db_connect, select_one_query, update_query, update_local_query, insert_local_query

module_directory = os.path.dirname(__file__)


def create_transfer_json(court_name, bench):
    db = db_connect()
    try:
        cursor = db.cursor()
        cursor.execute("select count(id) as num_rows from " + str(court_name) + " WHERE is_json=0")
        result = cursor.fetchall()
        cursor.close()
        no_rows = result[0]['num_rows']

        no_of_data_per_iteration = 1000
        no_of_iteration = floor(int(no_rows) / no_of_data_per_iteration) + 1

        j_count = select_one_query("SELECT no_json FROM tracker WHERE court_name=%s and bench=%s",
                                   (court_name, bench))['no_json']

        for i in range(0, no_of_iteration):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM " + str(court_name) + " WHERE is_json=0 LIMIT " +
                           str(no_of_data_per_iteration) + " OFFSET " + str(i * no_of_data_per_iteration))
            result = cursor.fetchall()
            cursor.close()

            if result:
                file_path = module_directory + "/../data_files/json_files/new-" + str(
                    court_name) + "-" + str(bench) + "-" + str(i + 1 + j_count) + ".json"
                fw = open(file_path, "w")
                fw.write(json.dumps(result))

                if transfer_to_bucket('JSON_Files', file_path):
                    for record in result:
                        update_query("UPDATE " + court_name + " SET is_json=1 WHERE id='" + str(record['id']) + "'")

                    update_local_query("UPDATE tracker SET no_json=no_json+1 WHERE court_name=%s", (court_name))
                    update_local_query("UPDATE tracker SET transferred_json=transferred_json+1 "
                                       "WHERE court_name=%s and bench=%s", (court_name, bench))
                    os.remove(file_path)
                else:
                    insert_local_query("INSERT INTO alerts (court_name, bench, error_message) VALUES (%s, %s, %s)",
                                       (court_name, bench, 'JSON Failed to transfer to bucket.'))
                    update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                                       (court_name, bench))

        db.close()
        return True

    except Exception as e:
        insert_local_query("INSERT INTO alerts (court_name, bench, error_message) VALUES (%s, %s, %s)",
                           (court_name, bench, 'JSON Error'))
        update_local_query("UPDATE tracker SET no_alerts=no_alerts+1 WHERE court_name=%s and bench=%s",
                           (court_name, bench))
        traceback.print_exc()
        logging.error("Failed select query: %s", e)
        db.close()
        return False
