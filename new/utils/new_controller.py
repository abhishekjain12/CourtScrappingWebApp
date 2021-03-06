from new.courts import kolkata, gst_appellate, gst_advance_authority, chhattisgarh, punjab_haryana, aar_rulings, \
    national_company_law_appellate_tribunal, competition_appellate_tribunal

from new.utils.new_metadata import metadata


def court_controller(court_name, bench):
    code_file = None
    bench_list = None
    for data in metadata:
        if data['court_name'] == court_name:
            code_file = data['file_name']
            bench_list = data['bench']
            break

    if code_file is not None:
        if str(code_file) == 'kolkata':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return kolkata.main(court_name, bench)

        if str(code_file) == 'competition_appellate_tribunal':
            if bench_list is not None:
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return competition_appellate_tribunal.main(court_name, bench)

        if str(code_file) == 'national_company_law_appellate_tribunal':
            if bench_list is not None:
                bench = str(bench).replace(' ', '+')
                for bench_ in bench_list:
                    if bench_['id'] == bench:
                        return national_company_law_appellate_tribunal.main(court_name, bench)

        if str(code_file) == 'gst_appellate':
            return gst_appellate.main(court_name)

        if str(code_file) == 'gst_advance_authority':
            return gst_advance_authority.main(court_name)

        if str(code_file) == 'chhattisgarh':
            return chhattisgarh.main(court_name)

        if str(code_file) == 'punjab_haryana':
            return punjab_haryana.main(court_name)

        if str(code_file) == 'aar_rulings':
            return aar_rulings.main(court_name)
