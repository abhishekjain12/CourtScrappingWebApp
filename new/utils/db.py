import os
import pymysql.cursors

module_directory = os.path.dirname(__file__)


def db_connect():
    return pymysql.connect(host="35.226.213.76",
                           user="root",
                           password="krypton212",
                           db="Courts_Data",
                           # charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def db_local_connect():
    return pymysql.connect(host="localhost",
                           user="root",
                           password="krypton212",
                           db="Courts_Data",
                           # charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
