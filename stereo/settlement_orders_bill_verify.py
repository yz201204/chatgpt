# coding:utf-8
import arrow
import time
import re
import threading
import queue
from stereo.settlement_common import SettlementCommon


class SettlementOrdersBillVerify(SettlementCommon):
    """
    对账
    """

    def __init__(self):
        super(SettlementOrdersBillVerify, self).__init__()
        self.error_list = list()
        self.q = queue.Queue()

    def batch_verify_status(self, *bill_detail_ids):
        """批量对账"""
        if isinstance(bill_detail_ids, str):
            bill_detail_ids = [bill_detail_ids]
        for bill_detail_id in bill_detail_ids:
            res = self.verify_status(bill_detail_id, verify_status="3")
            time.sleep(0.1)
            if res.get("code") == 600:
                self.verify_status_order_id(bill_detail_id)
                continue
            res = self.verify_status(bill_detail_id, verify_status="4", reason="自动对账")
            if res.get("code") != 0:
                self.error_list.append(bill_detail_id)
        if self.error_list:
            return self.error_list
        else:
            return True

    def verify_status_order_id(self, order_id):
        """订单获取detail_id后对账"""
        bill_detail_ids = self.get_list(order_id)
        for bill_detail_id in bill_detail_ids:
            res = self.verify_status(bill_detail_id, verify_status="3")
            if res.get("code") != 0:
                self.error_list.append(bill_detail_id)
                return
            time.sleep(0.1)
            self.verify_status(bill_detail_id, verify_status="4", reason="自动对账")

    def get_bill_order_ids(self, bill_id, order_category=None):
        """获取入账中的id"""
        url = self.settlement_url + "/api/settlement/settlement/bill/manage/detail/orders/new"
        count = self.get_list_count(bill_id, order_category)
        if count is None:
            raise ValueError("没获取到任何数据，请检查单号")
        order_ids = self.get_all_order_ids(url, bill_id, count)
        return order_ids

    def get_bill_order_ids_fb(self, bill_id, order_category=None):
        """个人账单bill_id下的所有订单"""
        url = "https://stereo-settlement-web-fat.fenbeijinfu.com/api/settlement/settlement/bill/manage/detail/voucher/orders/new"
        count = self.get_list_count_fb(bill_id, order_category)
        if count is None:
            raise ValueError("列表数量获取失败了")
        order_ids = self.get_all_order_ids(url, bill_id, count)
        return order_ids

    def get_all_order_ids(self, url, bill_id, count, size=30):
        order_ids = set()
        for i in range(1, int(count / size) + 2):
            params = {
                "bill_id": bill_id,
                "pageIndex": i,
                "pageSize": size
            }
            res = self.get(url, params=params)
            for d in res.json()["data"]:
                if d["entryStatusDTO"]["key"] == 2:
                    order_ids.add(d["orderId"])
        return list(order_ids)

    def verify_status_order_id_thread(self):
        while True:
            try:
                order_id = self.q.get(timeout=0.1)
                self.verify_status_order_id(order_id)
            except Exception as e:
                print(e)
                break

    def batch_verify_status_bill_id(self, bill_id, order_category=None):
        """账单入账中的都对账"""
        order_ids = self.get_bill_order_ids(bill_id, order_category)
        self.batch_verify_status_order_ids_thread(order_ids)

    def batch_verify_status_bill_id_fb(self, bill_id, order_category=None):
        """账单入账中的都对账-分贝"""
        order_ids = self.get_bill_order_ids_fb(bill_id, order_category)
        self.batch_verify_status_order_ids_thread(order_ids)

    def batch_verify_status_order_ids_thread(self, order_ids):
        for order_id in order_ids:
            self.q.put(order_id)
        tasks = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.verify_status_order_id_thread)
            tasks.append(t)
            t.start()
        for task in tasks:
            task.join()

    def batch_verify_status_bill_no(self, bill_no, order_category=None):
        """账单入账中的都对账"""
        bill_id = self.get_bill_id(bill_no)
        self.batch_verify_status_bill_id(bill_id, order_category)

    def batch_verify_status_bill_no_fb(self, bill_no, order_category=None):
        """账单入账中的都对账"""
        bill_id = self.get_bill_id(bill_no)
        self.batch_verify_status_bill_id_fb(bill_id, order_category)

    def batch_verify_status_bill(self, bill, order_category=None):
        """账单入账中的都对账,自动判断是id还是bill_no"""
        if self.judgment_bill(bill):
            self.batch_verify_status_bill_no(bill, order_category)
        else:
            self.batch_verify_status_bill_id(bill, order_category)

    def batch_verify_status_bill_fb(self, bill, order_category=None):
        """账单入账中的都对账,自动判断是id还是bill_no"""
        if self.judgment_bill(bill):
            self.batch_verify_status_bill_no_fb(bill, order_category)
        else:
            self.batch_verify_status_bill_id_fb(bill, order_category)

    def get_list(self, order_id):
        """对账那获取详情"""
        url = self.settlement_url + "/api/settlement/settlement/bill/verify/new/list"
        params = {
            "v": int(arrow.now().timestamp() * 1000),
            "order_id": order_id,
        }
        res = self.get(url, params=params)
        if len(res.json()["data"]) > 0:
            return [d["id"] for d in res.json()["data"]]


if __name__ == '__main__':
    s = SettlementOrdersBillVerify()
    # s.batch_verify_status_bill_id("63e0b18efa9121347e80f04d")
    # s.verify_status_order_id("ORL221123221918650596069")
    # s.batch_verify_status_bill_id("63e3a97e9903e42031b35c1b")
    # s.batch_verify_status_bill_id("63e458385520cc5071a3ba22")
    # s.batch_verify_status_bill_id("63e45e939903e42031b38f66")
    a = s.judgment_bill("a42020220101")
    print(a)
    print(s.error_list)
