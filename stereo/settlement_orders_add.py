# coding:utf-8
import arrow
from queue import Queue
import threading
from stereo.settlement_common import SettlementCommon


class SettlementOrdersAdd(SettlementCommon):
    """
    加入账单
    """

    def __init__(self):
        super(SettlementOrdersAdd, self).__init__()
        self.error_list = list()
        self.q = Queue()
        self.detail_search = {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "order_create_start_time": "2023-01-02 00:00:00",
            "order_create_end_time": "2023-02-09 23:59:59",
            "company_id": "6319a47986afcc0c8b63b10a"
        }

    def batch_detail_add(self, bill_id_in, bill_id_out):
        """将账单bill_id_out中的订单批量加入账单bill_id_in"""
        order_ids = self.get_bill_order_ids(bill_id_out)
        for order_id in order_ids:
            bill_detail_ids = self.get_bill_detail_ids(order_id)
            for bill_detail_id in bill_detail_ids:
                self.detail_add(bill_id_in, bill_detail_id)

    def batch_detail_add_thread(self, bill_id_in, bill_in_out):
        """将账单bill_id_out中的订单批量加入账单bill_id_in多线程模式"""
        order_ids = self.get_bill_order_ids(bill_in_out)
        for order_id in order_ids:
            self.q.put(order_id)
        tasks = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.detail_add_thread, args=(bill_id_in,))
            tasks.append(t)
            t.start()
        for task in tasks:
            task.join()

    def batch_detail_move_thread(self, *bill_id):
        """账单间的订单移动"""
        if len(bill_id) == 2:
            bill_id_in, bill_id_out = bill_id
        elif len(bill_id) == 1:
            bill_id_out = bill_id[0]
            if self.judgment_bill(bill_id_out):
                bill_id_in = bill_id_out[:-8] + "00000000"
            else:
                from config.db_config import StereoSettlementDb
                from utils.DbHandle import DBHandle
                sql = DBHandle(StereoSettlementDb)
                bill_id_in = sql.query("select * from bill_summary where id = '6333c5292caeca35c7152ef6'")[0]["BILL_NO"]
        else:
            raise ValueError("账单间移动订单请输入1个或两个账单号, 为一个时默认移动到未出账单")
        bill_id_in = self.get_bill_id(bill_id_in) if self.judgment_bill(bill_id_in) else bill_id_in
        bill_id_out = self.get_bill_id(bill_id_out) if self.judgment_bill(bill_id_out) else bill_id_out
        print(bill_id_in, bill_id_out)
        self.batch_detail_add_thread(bill_id_in, bill_id_out)

    def detail_add_thread(self, bill_id):
        """从队列中获取订单号加入账单bill_id中"""
        try:
            while True:
                order_id = self.q.get(timeout=1)
                bill_detail_ids = self.get_bill_detail_ids(order_id)
                for bill_detail_id in bill_detail_ids:
                    self.detail_add(bill_id, bill_detail_id)
        except Exception as e:
            print(e)

    def get_bill_detail_ids(self, order_id):
        """通过订单id获取明细id列表"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/listV2"
        params = {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "order_id": order_id
        }
        res = self.get(url, params=params)
        detail_ids = []
        for d in res.json()["data"]:
            detail_id = d["detailBaseInfoBean"]["id"]
            detail_ids.append(detail_id)
        return detail_ids

    def get_detail_ids_search(self):
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/listV2"
        params = self.detail_search
        res = self.get(url, params=params)
        detail_ids = []
        can_add_status = {1, 5}  # 已出账单和未出账单可加入账单
        for d in res.json()["data"]:
            if d["detailBillInfoBean"]["state"]["key"] in can_add_status:
                detail_id = d["detailBaseInfoBean"]["id"]
                detail_ids.append(detail_id)
        return detail_ids

    def batch_add_detail_search(self, bill_id):
        detail_ids = self.get_detail_ids_search()
        bill_id = self.get_bill_id(bill_id) if self.judgment_bill(bill_id) else bill_id
        for detail_id in detail_ids:
            self.detail_add(bill_id, detail_id)


if __name__ == '__main__':
    s = SettlementOrdersAdd()
    # a = s.get_bill_order_ids("63d732d746b22546c2f5c06e")
    # a = s.detail_add("635f6f8496424a7e6e71c52e", "6361022574766e127824e52d")
    # a = s.get_bill_detail_ids("637f6cc471eade56b6c10d85")
    # a = s.batch_detail_add_thread("635f6f8496424a7e6e71c52e", "63e3a97e9903e42031b35c1b")
    # a = s.batch_detail_add_thread("638099a448176461d8a917e5", "63e458385520cc5071a3ba22")
    # a = s.batch_detail_add_thread("635f965296424a7e6e71c94c", "63e45e939903e42031b38f66")
    a = s.get_detail_ids_search()
    print(a)
