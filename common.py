# fw = open(module_directory + "/../Data_Files/Html_Files/" + court_name + "_" +
#           str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
# fw.write(str(res))
import logging
import traceback
import pymysql.cursors

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from slugify import slugify


def transfer_to_bucket(folder_name, filename):
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('storage', 'v1', credentials=credentials)

        bucket = 'ecl-original'

        body = {'name': str(folder_name) + '/' + str(filename[filename.rfind("/")+1:])}
        req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
        resp = req.execute()

        return True

    except Exception as e:
        logging.error("Failed to transfer! %s", e)
        return False


def pdf_to_text_api(file_path):
    try:
        text_data = ""

        pdf_manager = PDFResourceManager()
        string_io = StringIO()
        pdf_to_text = TextConverter(pdf_manager, string_io, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(pdf_manager, pdf_to_text)
        for page in PDFPage.get_pages(open(file_path, 'rb')):
            interpreter.process_page(page)
            text_data = string_io.getvalue()

        return str(text_data).strip().replace('\n', '').replace('\f', '')

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        return "FAILED"


def court_pdfname(court_name):
    try:
        db = pymysql.connect(host="localhost", user="root", password="root", db="Courts_Data",
                             cursorclass=pymysql.cursors.DictCursor)
        while True:
            cursor = db.cursor()
            cursor.execute("SELECT case_no FROM " + court_name + " WHERE pdf_filename IS NULL LIMIT 1")
            result = cursor.fetchone()

            if result is None:
                cursor.close()
                db.close()
                return 'Done'
            else:
                sql = "UPDATE " + court_name + " SET pdf_filename = '" + court_name + "_" + \
                      slugify(result['case_no']) + ".pdf' WHERE case_no = '" + str(result['case_no']) + "'"
                cursor = db.cursor()
                cursor.execute(sql)
                db.commit()

    except Exception as e:
        print(e)
        return False
