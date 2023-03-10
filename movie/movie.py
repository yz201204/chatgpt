# *_*coding:utf-8 *_*
import requests


class Movie:
    def __init__(self):
        pass

    @staticmethod
    def ticket(order_id):
        url = "http://noc-fat.fenbeijinfu.com/ordedr/ticket/isready"
        params = {
            "supplierOrderId": order_id,
            "result": 1
        }
        res = requests.get(url, params=params)
        return res.text


if __name__ == '__main__':
    m = Movie()
    a = m.ticket("40777")
    print(a)
