import datetime

from Courts import Manipur
from Utils.CourtMetaData import metadata


def court_controller(court_name, bench, start_date, end_date):
    code_file = None
    for data in metadata:
        if data['court_name'] == court_name:
            start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime(data['date_format'])
            end_date = (datetime.datetime.strptime(str(end_date), "%d/%m/%Y")).strftime(data['date_format'])
            code_file = data['file_name']
            break

    if str(code_file) == 'Manipur':
        return Manipur.main(start_date, end_date)
