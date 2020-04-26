import mh_z19
import json
import urllib.request
import time
import datetime

def put_log(data):
    cur_date = datetime.datetime.today()
    dump_date = json.dumps(data)
    put_str = '[{0:%H:%M:%S}]:{1}\n'.format(cur_date, dump_date)

    with open('logs/{0:%Y%m%d}.txt'.format(cur_date), 'a') as f:
        f.write(put_str)
    print(put_str)



def post_value(data):
    put_log(data)
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
    post_value(cur_data)



def main():
    while True:
        interval()
        time.sleep(10)



main()
