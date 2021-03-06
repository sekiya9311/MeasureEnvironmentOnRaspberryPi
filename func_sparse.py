import mh_z19
import os
import json
import urllib.request
import time
import datetime

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE_PATH = '{0}/save.txt'.format(CUR_PATH)



def get_prev_data() -> dict:
    if (not os.path.exists(SAVE_FILE_PATH)):
        return {}
    with open(SAVE_FILE_PATH, 'r') as f:
        return json.load(f)



def save_cur_data(data: dict) -> None:
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(data, f)



def put_log(data, is_err: bool, ignore_err: bool = False) -> None:
    try:
        cur_date = datetime.datetime.today()
        log_file_path = '{0}/logs/{1:%Y%m%d}.txt'.format(CUR_PATH, cur_date)
        dump_date = json.dumps(data)
        put_str = '[{0}][{1:%H:%M:%S}]:{2}\n'.format(
            'ERROR' if is_err else 'INFO',
            cur_date,
            dump_date
        )
        with open(log_file_path, 'a') as f:
            f.write(put_str)
        print(put_str)

    except Exception as ex:
        if (ignore_err):
            return
        put_log(ex, True, True)



def post_value(data: dict) -> None:
    put_log(data, False)
    URL = 'https://asia-northeast1-measureenvironments.cloudfunctions.net/addCO2'
    HEADERS = {
        'Content-type': 'application/json'
    }
    post_obj = { 'data': data }

    request = urllib.request.Request(
        URL,
        json.dumps(post_obj).encode(),
        HEADERS
    )
    with urllib.request.urlopen(request) as response:
        unused = response.read()



def interval(prev_data: dict) -> (bool, dict):
    cur_data = mh_z19.read_all()
    if (cur_data == prev_data):
        return (False, cur_data)
    if (cur_data.get('co2') == prev_data.get('co2')):  # use only co2
        return (False, cur_data)

    try:
        post_value(cur_data)
    except Exception as ex:
        put_log(ex, True)
    
    return (True, cur_data)



def main() -> None:
    cur_data = get_prev_data()
    while True:
        res = interval(cur_data)
        if (res[0]):
            cur_data = res[1]
            save_cur_data(cur_data)
        time.sleep(60)



main()
