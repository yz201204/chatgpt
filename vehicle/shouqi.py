import time

import requests
from bs4 import BeautifulSoup
import re
import random
from vehicle.chaojiying import Chaojiying_Client
import arrow


class ShouQi:
    def __init__(self):
        self.http = requests.session()
        self.channel = "fbtong"
        self.sqycKey = "WjYuCka5tWw7aamyY"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
        }
        self.car_group_id = {
            "舒适型": 34,
            "商务6座": 35,
            "商务福祉车": 40,
            "畅享型": 43,
            "豪华型": 61,
            "优享型": 283,
        }
        # self.group_id = random.choice(list(self.car_group_id.values()))
        self.group_id = 34
        self.url = "https://test-openapi.01zhuanche.com/touch/process/driver/updateOrderStatus"

    def accepted(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "accepted",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def setout(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "setout",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def arriving(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "arriving",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def in_progress(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "in_progress",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def end_trip(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "end_trip",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def completed(self, order_no):
        data = {
            "orderNo": order_no,
            "orderStatus": "completed",
            "carGroupId": self.group_id,
            "channel": self.channel,
            "sqycKey": self.sqycKey
        }
        res = self.http.post(self.url, data, headers=self.headers)
        print(res.text)
        return res.text

    def run(self, order_no=None):
        self.accepted(order_no)
        time.sleep(1)
        self.setout(order_no)
        time.sleep(1)
        self.arriving(order_no)
        time.sleep(1)
        self.in_progress(order_no)
        time.sleep(1)
        self.end_trip(order_no)
        time.sleep(1)
        self.completed(order_no)


if __name__ == '__main__':
    shouqi = ShouQi()
    shouqi.run("B230112162824931000")
