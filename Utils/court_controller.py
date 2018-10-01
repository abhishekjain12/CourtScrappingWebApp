import datetime

from Courts import Manipur, judis, lobis, Bombay, Calcutta, Karnataka, Arunachal_Pradesh, Himachal_Pradesh, \
    Madhya_Pradesh, Mizoram, Nagaland, Punjab_Haryana, Sikkim, Supreme_Court, Goa, Gauhati
from Tribunals import Income_Tax_Appellate, Customs_Excise_And_Service_Tax_Appellate_Tribunal, \
    National_Company_Law_Tribunal
from Utils.CourtMetaData import metadata


def court_controller(court_name, bench, start_date, end_date):
    code_file = None
    court_id = None
    bench_list = None
    for data in metadata:
        if data['court_name'] == court_name:
            start_date = (datetime.datetime.strptime(str(start_date), "%d/%m/%Y")).strftime(data['date_format'])
            end_date = (datetime.datetime.strptime(str(end_date), "%d/%m/%Y")).strftime(data['date_format'])
            code_file = data['file_name']
            court_id = data['court_id']
            bench_list = data['bench']
            break

    if code_file is not None:
        if str(code_file) == 'Manipur':
            return Manipur.main(start_date, end_date)

        if str(code_file) == 'judis':
            if court_id != 555 and court_id is not None:
                return judis.main(court_name, court_id, start_date, end_date)

            else:
                if bench_list is not None:
                    for bench_ in bench_list:
                        if int(bench_['id']) == int(bench):
                            return judis.main(court_name, bench, start_date, end_date)

        if str(code_file) == 'lobis':
            if court_id is not None:
                return lobis.main(court_name, court_id, start_date, end_date)

        if str(code_file) == 'Bombay':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return Bombay.main(court_name, bench, start_date, end_date)

        if str(code_file) == 'Calcutta':
            if bench_list is not None:
                for bench_ in bench_list:
                    if int(bench_['id']) == int(bench):
                        return Calcutta.main(court_name, bench, start_date, end_date)

        if str(code_file) == 'Karnataka':
            return Karnataka.main(court_name, start_date, end_date)

        if str(code_file) == 'Arunachal_Pradesh':
            return Arunachal_Pradesh.main(court_name, start_date, end_date)

        if str(code_file) == 'Himachal_Pradesh':
            return Himachal_Pradesh.main(court_name, start_date, end_date)

        if str(code_file) == 'Madhya_Pradesh':
            return Madhya_Pradesh.main(court_name, start_date, end_date)

        if str(code_file) == 'Mizoram':
            return Mizoram.main(court_name, start_date, end_date)

        if str(code_file) == 'Nagaland':
            return Nagaland.main(court_name, start_date, end_date)

        if str(code_file) == 'Punjab_Haryana':
            return Punjab_Haryana.main(court_name, start_date, end_date)

        if str(code_file) == 'Sikkim':
            return Sikkim.main(court_name, start_date, end_date)

        if str(code_file) == 'Supreme_Court':
            return Supreme_Court.main(court_name, start_date, end_date)

        if str(code_file) == 'Goa':
            return Goa.main(court_name, start_date, end_date)

        if str(code_file) == 'Gauhati':
            return Gauhati.main(court_name, start_date, end_date)

        # ----------------------------------------------------------------TRIBUNALS

        if str(code_file) == 'Income_Tax_Appellate':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == int(bench):
                        return Income_Tax_Appellate.main(court_name, bench, start_date, end_date)

        if str(code_file) == 'Customs_Excise_And_Service_Tax_Appellate_Tribunal':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return Customs_Excise_And_Service_Tax_Appellate_Tribunal.main(court_name, bench,
                                                                                      start_date, end_date)

        if str(code_file) == 'National_Company_Law_Tribunal':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return National_Company_Law_Tribunal.main(court_name, bench, start_date, end_date)

    else:
        return False
