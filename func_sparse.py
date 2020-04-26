import mh_z19
import os
import json
import urllib.request
import time

SAVE_FILE_NAME = 'save.txt'



def get_prev_data():
    if (not os.path.exists(SAVE_FILE_NAME)):
        return {}
    with open(SAVE_FILE_NAME, 'r') as f:
        return json.load(f)



def save_cur_data(data):
    with open(SAVE_FILE_NAME, 'w') as f:
        json.dump(data, f)



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



def interval(prev_data):
    cur_data = mh_z19.read_all()
    if (cur_data == prev_data):
        return (False, cur_data)
    if (cur_data.get('co2') == prev_data.get('co2')):  # use only co2
        return (False, cur_data)

    post_value(cur_data)
    return (True, cur_data)



def main():
    cur_data = get_prev_data()
    while True:
        res = interval(cur_data)
        if (res[0]):
            cur_data = res[1]
            save_cur_data(cur_data)
        time.sleep(10)



main()

