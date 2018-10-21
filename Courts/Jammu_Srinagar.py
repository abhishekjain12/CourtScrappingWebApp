from Courts import judis, lobis


def main(court_name, bench_code, start_date, end_date):
    if int(bench_code) == 3 or int(bench_code) == 4:
        return judis.main(court_name, bench_code, start_date, end_date)
    else:
        return lobis.main(court_name, bench_code, start_date, end_date)
