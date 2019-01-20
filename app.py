import datetime
import os

from glob import glob
from random import randint

from flask import Flask, render_template, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

import new
from Utils import logs
from Utils.CourtMetaData import metadata
from Utils.court_controller import court_controller
from Utils.db import select_query, select_json_query, get_tables_info, update_history_tracker, \
    download_pdf_to_bucket, select_local_query, update_local_query, select_one_local_query
from common import transfer_to_bucket, pdf_to_text_api, court_pdfname
from new.utils import db as new_db, new_controller, new_metadata

app = Flask(__name__)
module_directory = os.path.dirname(__file__)


@app.route('/')
def index():
    tracker_data = select_local_query("SELECT * FROM Tracker")
    tracker_history = select_query("SELECT * FROM Tracker_History ORDER BY id DESC LIMIT 100")
    tracker_json_history = select_query("SELECT * FROM Tracker_History_JSON ORDER BY id DESC LIMIT 100")
    tables = select_query("SHOW TABLES")
    table_info = get_tables_info()

    new_tracker_data = new_db.select_local_query("SELECT * FROM new_courts_data.tracker")
    new_tables = new_db.select_query("SHOW TABLES")
    new_table_info = new_db.get_tables_info()
    new_tracker_history = new_db.select_query("SELECT * FROM tracker_history ORDER BY id DESC LIMIT 100")

    return render_template("index.html",
                           tracker_data=tracker_data,
                           tables=tables,
                           tracker_history=tracker_history,
                           tracker_json_history=tracker_json_history,
                           table_info=table_info,
                           new_tables=new_tables,
                           new_tracker_data=new_tracker_data,
                           new_table_info=new_table_info,
                           new_tracker_history=new_tracker_history)


@app.route('/get-bench-list/<string:court_name>')
def get_bench_list(court_name):
    for court_data in metadata:
        if court_data['court_name'] == court_name:
            return jsonify(court_data['bench'])

    return 'Internal Server Error.', 500


# ----------------------------------------------------------------------------------------------------------------------


@app.route('/start-scrap', methods=['POST'])
def start_scrap():
    court_name = request.form['court_name']
    bench = request.form['bench']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    update_local_query("UPDATE Tracker SET status='IN_CANCELLED', emergency_exit=true WHERE status='IN_RUNNING'")
    update_local_query("UPDATE Tracker SET status='IN_RUNNING', emergency_exit=false, No_Cases=0, No_Year_NoData=0, "
                       "No_Year_Error=0, No_Error=0, Start_Date='" + start_date + "', End_Date='" + end_date +
                       "', bench='" + str(bench) + "' WHERE Name='" + court_name + "'")

    res = court_controller(court_name, bench, start_date, end_date)
    update_local_query("UPDATE Tracker SET status = 'IN_BUCKET_TRANSFER' WHERE Name = '" + str(court_name) + "'")

    for filename in glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/PDF_Files/" + str(court_name) + "*.pdf"):
        if transfer_to_bucket('PDF_Files', filename):
            os.remove(filename)

    for filename in glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/Text_Files/" + str(court_name) + "*.txt"):
        if transfer_to_bucket('Text_Files', filename):
            os.remove(filename)

    if res:
        update_local_query("UPDATE Tracker SET status = 'IN_SUCCESS', emergency_exit=true WHERE Name = '" +
                           str(court_name) + "'")
    else:
        update_local_query("UPDATE Tracker SET No_Year_Error = No_Year_Error + 1, status = 'IN_FAILED', "
                           "emergency_exit=true WHERE Name = '" + str(court_name) + "'")

    update_history_tracker(court_name)
    return jsonify(res)


@app.route('/current-scrap/<string:court_name>')
def current_scrap(court_name):
    return jsonify(select_one_local_query("SELECT * FROM Tracker WHERE Name = '" + court_name + "'"))


@app.route('/running-scrap')
def running_scrap():
    return jsonify(select_one_local_query("SELECT * FROM Tracker WHERE status = 'IN_RUNNING' LIMIT 1"))


@app.route('/cancel-scrap/<string:court_name>')
def cancel_scrap(court_name):
    return jsonify(update_local_query("UPDATE Tracker SET status='IN_ABORT', emergency_exit=true WHERE Name='" +
                                      court_name + "'"))


# ----------------------------------------------------------------------------------------------------------------------


@app.route('/start-pdf', methods=['POST'])
def start_pdf():
    logs.initialize_logger("PDF")
    court_name = request.form['court_name']
    update_local_query("UPDATE Tracker_pdf SET status='IN_RUNNING', emergency_exit=false, Name='" + court_name +
                       "', No_Files=0 WHERE 1")
    court_pdfname(court_name)
    download_pdf_to_bucket(court_name)
    return '', 200


@app.route('/current-pdf')
def current_pdf():
    return jsonify(select_one_local_query("SELECT Name, No_Files, status FROM Tracker_pdf LIMIT 1"))


@app.route('/cancel-pdf')
def cancel_pdf():
    return jsonify(update_local_query("UPDATE Tracker_pdf SET status='IN_ABORT', emergency_exit=true WHERE 1"))


# ----------------------------------------------------------------------------------------------------------------------


@app.route('/start-json', methods=['POST'])
def start_json():
    court_name = request.form['court_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    for data in metadata:
        if data['court_name'] == court_name:
            start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime(data['o_date_format'])
            end_date = (datetime.datetime.strptime(str(end_date), "%d/%m/%Y")).strftime(data['o_date_format'])
            break

    update_local_query("UPDATE Tracker_JSON SET status='IN_CANCELLED', emergency_exit=true WHERE status='IN_RUNNING'")
    if select_json_query(court_name, start_date, end_date):

        for filename in glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/JSON_Files/*.json"):
            if transfer_to_bucket('JSON_Files', filename):
                os.remove(filename)

        return '', 200
    else:
        return '', 500


@app.route('/current-json/<string:court_name>')
def current_json(court_name):
    return jsonify(select_one_local_query("SELECT * FROM Tracker_JSON WHERE Name = '" + court_name + "' ORDER BY id "
                                                                                                     "DESC LIMIT 1"))


@app.route('/running-json')
def running_json():
    return jsonify(select_one_local_query("SELECT * FROM Tracker_JSON WHERE status = 'IN_RUNNING' ORDER BY id "
                                          "DESC LIMIT 1"))


@app.route('/cancel-json/<string:court_name>')
def cancel_json(court_name):
    return jsonify(update_local_query("UPDATE Tracker_JSON SET status='IN_ABORT', emergency_exit=true WHERE Name='" +
                                      court_name + "'"))


@app.route('/get-json/<string:court_name>')
def get_json(court_name):
    res = {'Name': []}

    for file_ in glob(module_directory + "/Data_Files/JSON_Files/" + court_name + "*.json"):
        res['Name'].append(file_[file_.rfind("/")+1:])

    return jsonify(res)


@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory(directory=module_directory + "/Data_Files/JSON_Files", filename=filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in list(['pdf'])


@app.route('/pdf-to-text', methods=['POST'])
def pdf_to_text_api_route():
    app.config['UPLOAD_FOLDER'] = module_directory + "/Data_Files/input_files"
    if 'file' not in request.files:
        return jsonify({'data': 'FAILED! No file Found.'})

    else:
        f = request.files['file']
        if f.filename == '':
            return jsonify({'data': 'FAILED! No File Received.'})

        elif f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filename = str(randint(0, 1000)) + "_" + filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            res = {'data': pdf_to_text_api(module_directory + "/Data_Files/input_files/" + filename)}
            os.remove(module_directory + "/Data_Files/input_files/" + filename)
            return jsonify(res)

        else:
            return jsonify({'data': 'FAILED! Invalid File Type.'})


# ---------------------------------------------------------------NEW----------------------------------------------------
@app.route('/new/start-scrap', methods=['POST'])
def new_start_scrap():
    court_name = request.form['court_name']
    bench = request.form['bench']

    new_db.update_local_query("UPDATE tracker SET status='IN_CANCELLED', emergency_exit=true WHERE status='IN_RUNNING'")
    new_db.update_local_query("UPDATE tracker SET status='IN_RUNNING', emergency_exit=false, no_alerts=0, no_tries=0 "
                              "WHERE court_name=%s and bench=%s", (court_name, bench))

    res = new_controller.court_controller(court_name, bench)

    if res:
        new_db.update_local_query("UPDATE tracker SET status = 'IN_SUCCESS', emergency_exit=true "
                                  "WHERE court_name=%s and bench=%s", (court_name, bench))
    else:
        new_db.update_local_query("UPDATE tracker SET status = 'IN_FAILED', emergency_exit=true "
                                  "WHERE court_name=%s and bench=%s", (court_name, bench))

    return 'Done'


@app.route('/new/current-scrap/<string:court_name>/<string:bench>')
def new_current_scrap(court_name, bench):
    return jsonify(new_db.select_one_local_query("SELECT * FROM tracker "
                                                 "WHERE court_name=%s and bench=%s", (court_name, bench)))


@app.route('/new/running-scrap')
def new_running_scrap():
    return jsonify(new_db.select_one_local_query("SELECT * FROM tracker WHERE status = 'IN_RUNNING' LIMIT 1"))


@app.route('/new/cancel-scrap/<string:court_name>/<string:bench>')
def new_cancel_scrap(court_name, bench):
    return jsonify(new_db.update_local_query("UPDATE tracker SET status='IN_ABORT', emergency_exit=true "
                                             "WHERE court_name=%s and bench=%s", (court_name, bench)))


@app.route('/new/get-bench-list/<string:court_name>')
def new_get_bench_list(court_name):
    for court_data in new_metadata.metadata:
        if court_data['court_name'] == court_name:
            return jsonify(court_data['bench'])

    return 'Internal Server Error.', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
