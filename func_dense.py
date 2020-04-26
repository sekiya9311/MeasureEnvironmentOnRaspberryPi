import mh_z19
import json
import urllib.request
import time


def post_value(data):
    URL = 'https://us-central1-measureenvironments.cloudfunctions.net/addCO2'
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

