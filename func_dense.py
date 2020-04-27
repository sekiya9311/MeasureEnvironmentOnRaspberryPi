import mh_z19
import json
import urllib.request
import time
import datetime
import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

def put_log(data, is_err):
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



def post_value(data):
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



def interval():
    cur_data = mh_z19.read_all()
    try:
        post_value(cur_data)
    except Exception as ex:
        put_log(ex, True)



def main():
    while True:
        interval()
        time.sleep(10)



main()
