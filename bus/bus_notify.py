# *_*coding:utf-8 *_*
import requests
from stereo.http_handle import HttpHandle


class BusNotify(HttpHandle):
    def __init__(self):
        super(BusNotify, self).__init__()
        self.head = {"channel": "ctrip", "token": "", "version": "1.0"}
        self.sign = "QH93TCVBYO0HRPPHXQW0PNRWWRHTMC0PMKGWRRYVZIK="

    def pay_notify(self, order_number):
        url = "http://event-fat.fenbeijinfu.com/supplier/route/8/bus_bass/xiecheng/callback/payNotify"
        data = {
            "head": self.head,
            "body": {
                "description": "出票成功",
                "orderNumber": order_number,
                "payStatus": 0,
                "processState": 5,
                "status": "已成交"
            },
            "sign": self.sign
        }
        res = requests.post(url, json=data)
        return res.json()

    def refund_notify(self, order_number):
        """退票退款"""
        url = self.old_host + "/stereo/order/bus/pageList"
        params = {
            "supplierOrderId": order_number
        }
        response = self.get(url, params=params)
        data = {
            "head": self.head,
            "body": {
                "orderNumber": order_number,
                "partnerOrderNumber": "",
                "refundTicketState": "1",
                "refundTicketType": 1,
                "ticketId": "",
                "refundAmount": 0,
                "ticketAmount": 0,
                "passengerName": "",
                "refundTicketTime": "",
                "failMsg": "错误原因",
            },
            "sign": self.sign
        }
        refund_data = {
            "head": self.head,
            "body": {
                "orderNumber": order_number,
                "partnerOrderNumber": "",
                "refundTicketType": 13,
                "ticketId": "1",
                "refundAmount": 0,
                "sourceType": 1
            },
            "sign": self.sign
        }
        for d in response.json()["data"]:
            if d["orderStatus"]["key"] == 101:
                data["body"]["partnerOrderNumber"] = d["orderId"]
                data["body"]["refundAmount"] = d["ticketTotalPrice"]
                data["body"]["ticketAmount"] = d["ticketTotalPrice"]
                data["body"]["passengerName"] = d["passengerName"]
                data["body"]["refundTicketTime"] = d["createTime"]
                refund_data["body"]["partnerOrderNumber"] = d["orderId"]
                refund_data["body"]["refundAmount"] = d["ticketCostPrice"]
            elif d["orderStatus"]["key"] == 91:
                data["body"]["ticketId"] = d["ticketId"]
            else:
                return
        print(data)
        print(refund_data)
        url1 = "http://event-fat.fenbeijinfu.com/supplier/route/8/bus_bass/xiecheng/callback/refundNotify"
        url2 = "http://event-fat.fenbeijinfu.com/supplier/route/8/bus_bass/xiecheng/callback/ticketNotify"
        res1 = requests.post(url1, json=refund_data)
        # res2 = requests.post(url2, json=data)
        # print(res1.json())
        # print(res2.json())
        return res1.json()


if __name__ == '__main__':
    bus = BusNotify()
    # bus.pay_notify("35090472966")
    bus.refund_notify("35090472966")
