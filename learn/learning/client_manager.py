import requests
import json

class ClientManager:
    def __init__(self):
        self.url = 'http://203.252.91.45:3000/event/'#'http://127.0.0.1:3000/event/'

    def post_status_update(self, json_result):
        print(json_result)
        url = self.url + 'unknown'
        res = requests.post(url, data = json_result)
        # with requests.Session() as s:
        #     res = s.post(url, data = json_result)
        #     # html source 가져오기
        #     html = res.text
        #     # http header 가져오기
        #     header = res.headers
        #     # http status 가져오기
        #     status = res.status_code
        #     is_ok = res.ok

        return res
