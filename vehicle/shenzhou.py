import time

import requests
from bs4 import BeautifulSoup
import re
import random
from vehicle.chaojiying import Chaojiying_Client
import arrow


class ShenZhou:
    def __init__(self):
        self.http = requests.session()
        self.app_id = "19991D7E00001C0A"
        self.csrf = ""
        self.code = ""
        self.cookie = ""

    def get_csrf(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
        }
        url = "http://developer.10101111.com/"
        res = self.http.get(url=url, headers=headers).text
        csrf = re.search('<meta name="csrf-token" content="(.*?)">', res)
        self.csrf = csrf.group(1)
        return self.csrf

    def get_code_png(self, name):
        url = "http://developer.10101111.com/login/checkCode"
        r = random.random()
        res = self.http.get(url + "?{}".format(r)).content
        with open(name, "wb") as fp:
            fp.write(res)

    def get_code(self, name):
        chaojiying = Chaojiying_Client('18612962340', '18612962340', '940341')
        im = open(name, 'rb').read()
        ret = chaojiying.PostPic(im, 1902)
        self.code = ret.get("pic_str")
        return self.code

    def login(self):
        url = "http://developer.10101111.com/login"
        data = {
            "username": "lele.xue@fenbeitong.com",
            "password": "xuelele1988",
            "vcode": self.code,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-Token": self.csrf,
            "Origin": "http://developer.10101111.com",
            "Referer": "http://developer.10101111.com/",
            "Host": "developer.10101111.com",
        }
        res = self.http.post(url=url, data=data, headers=headers)
        print(res.json())
        if res.json().get("message") == "验证码不正确!":
            return False
        cookie = res.headers["Set-Cookie"]
        self.cookie = cookie.split(";")[0]
        return self.cookie

    def orders(self, start_date="", end_date=""):
        if start_date == "" and end_date == "":
            date = arrow.now().format("YYYY-MM-DD")
            start_date = str(int(arrow.Arrow(*map(int, date.split('-'))).timestamp()))
            end_date = str(int(arrow.Arrow(*map(int, date.split('-'))).shift(days=1).timestamp()))
        url = "http://developer.10101111.com/authorization/manager/orders"
        data = {
            "appId": self.app_id,
            "startDate": start_date,
            "endDate": end_date,
            "state": "",
            "pageNo": ""
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "Cookie": "_csrf={}; {}".format(self.csrf, self.cookie),
            "Host": "developer.10101111.com"
        }
        res = self.http.get(url, params=data, headers=headers)
        return res.text

    @staticmethod
    def get_order_id(text):
        soap = BeautifulSoup(text, "html.parser")
        td = soap.find_all("td", class_="al tdcenter")
        if td:
            order_id = td[0].contents[0].strip()
            print(order_id)
            if td[4].contents[0].strip() == "新建":
                return order_id
            else:
                order_id = td[6].contents[0].strip()
                return order_id

    def order_header(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-Token": self.csrf,
            "Origin": "http://developer.10101111.com",
            "Host": "developer.10101111.com",
        }
        return headers

    def dispatch(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "dispatched",
            "driverId": "12345",
            "appId": self.app_id
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def arriving(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "arriving",
            "appId": self.app_id
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def arrived(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "arrived",
            "appId": self.app_id
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def service_started(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "serviceStarted",
            "appId": self.app_id
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def service_finished(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "serviceFinished",
            "appId": self.app_id
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def fee_submitted(self, order_id, fees=None):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        if fees:
            data = {
                "orderId": order_id,
                "state": "feeSubmitted",
                "appId": self.app_id,
                "actualKiloLength": fees[0],
                "highwayAmount": fees[1],
                "airportServiceAmount": fees[2],
                "parkingAmount": fees[3],
                "cleanAmount": fees[4],
                "otherAmount": fees[5],
                "otherAmountRemark": "备注",
            }
        else:
            data = {
                "orderId": order_id,
                "state": "feeSubmitted",
                "appId": self.app_id,
                "actualKiloLength": 1,
                "highwayAmount": 2,
                "airportServiceAmount": 3,
                "parkingAmount": 4,
                "cleanAmount": 5,
                "otherAmount": 6,
                "otherAmountRemark": 7,
            }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def completed(self, order_id):
        url = "http://developer.10101111.com/authorization/manager/orderStateChange"
        headers = self.order_header()
        data = {
            "orderId": order_id,
            "state": "completed",
            "appId": self.app_id,
        }
        res = self.http.post(url, data, headers=headers)
        return res.text

    def order_change(self, order_id, fees=None):
        res = self.dispatch(order_id)
        print(res)
        time.sleep(0.5)
        res = self.arriving(order_id)
        print(res)
        time.sleep(0.5)
        res = self.arrived(order_id)
        print(res)
        time.sleep(0.5)
        res = self.service_started(order_id)
        print(res)
        time.sleep(0.5)
        res = self.service_finished(order_id)
        print(res)
        time.sleep(0.5)
        res = self.fee_submitted(order_id, fees=fees)
        print(res)
        time.sleep(0.5)
        res = self.completed(order_id)
        print(res)
        return res

    def run(self, fees=None, start_date="", end_date=""):
        name = "code.png"
        self.get_csrf()
        self.get_code_png(name)
        self.get_code(name)
        login_status = self.login()
        if not login_status:
            self.get_code_png(name)
            self.get_code(name)
            self.login()
        text = self.orders(start_date, end_date)
        order_id = self.get_order_id(text)
        if order_id:
            self.order_change(order_id, fees=fees)
            return "神州接列表第一单成功"
        return "没查到订单信息"


if __name__ == '__main__':
    shenzhou = ShenZhou()
    shenzhou.run()
