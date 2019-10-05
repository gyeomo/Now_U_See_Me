import requests
import json

class ClientManager:
    def __init__(self):
        self.url = "http://203.252.91.45:3000/event/"

    def post_status_unknown(self, json_result):
        print(json_result)
        url = self.url+'unknown'
        res = requests.post(url, data = json_result)
        return res