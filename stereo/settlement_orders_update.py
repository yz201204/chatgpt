# coding:utf-8
import threading
from queue import Queue
from stereo.settlement_common import SettlementCommon


class SettlementOrdersUpdate(SettlementCommon):
    """
    计入
    """

    def __init__(self):
        super(SettlementOrdersUpdate, self).__init__()
        self.error_list = list()
        self.q = Queue()

    def get_ticket_id(self, order_id):
        """获取票id"""
        order_list = self.get_list(order_id)
        if order_list:
            return [d["detailBaseInfoBean"]["productId"] for d in order_list]

    def order_add(self, order_id, order_category=None):
        """重新计入"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/orders/add"
        params = {
            "version": "2",
        }
        relief = "1" if order_id.startswith("ORL") else "0"  # 是否减免
        if order_category is None:
            order_category = self.get_category_type(order_id)
        data = {
            "order_category": order_category,
            "is_relief": relief,
        }
        if str(order_category) in {"3", "7", "15"}:
            ticket_id_list = self.get_ticket_id(order_id)
            for ticket_id in ticket_id_list:
                data.update({"order_id_list": [ticket_id]})
                print("票id:", ticket_id, "订单id:", order_id)
                res = self.post(url, params=params, data=data)
                print(res.text)
                yield res.json()
        else:
            data.update({"order_id_list": [order_id]})
            res = self.post(url, params=params, data=data)
            print(res.text)
            yield res.json()

    def batch_add(self, *order_ids):
        """批量重新计入"""
        if isinstance(order_ids, str):
            order_ids = [order_ids]
        for order_id in order_ids:
            responses = self.order_add(order_id)
            for res in responses:
                if res.get("code") != 0:
                    self.error_list.append(order_id)
        if self.error_list:
            return self.error_list
        else:
            return True

    def order_add_thread(self):
        """重新计入thread"""
        try:
            while True:
                order_id = self.q.get(timeout=0.5)
                responses = self.order_add(order_id)
                for res in responses:
                    if res.get("code") != 0:
                        self.error_list.append(order_id)
        except Exception as e:
            print(e)

    def batch_add_thread(self, *order_ids):
        """批量重新计入thread"""
        if isinstance(order_ids, str):
            order_ids = [order_ids]
        for order_id in order_ids:
            self.q.put(order_id)
        tasks = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.order_add_thread, )
            tasks.append(t)
            t.start()
        for task in tasks:
            task.join()
        if self.error_list:
            return self.error_list
        else:
            return True

    def get_category_type(self, order_id):
        """获取订单的类型"""
        order_list = self.get_list(order_id)
        try:
            return order_list[0]["detailBaseInfoBean"]["categoryDTO"]["key"]
        except Exception as e:
            print(e)

    def bill_update_sw(self, bill_id, order_category=None):
        """账单重新计入"""
        order_ids = self.get_bill_order_ids(bill_id, order_category)
        self.batch_add_thread(*order_ids)

    def get_list_fb(self, order_id):
        """获取个人订单详情"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/voucher/listV2"
        data = {
            "order_id": order_id,
            "pageIndex": 1,
            "pageSize": 20
        }
        res = self.post(url, data=data, form=True)
        if res.json()["data"] and len(res.json()["data"]) > 0:
            return res.json()["data"]

    def get_ticket_id_fb(self, order_id):
        """获取个人票id"""
        order_list = self.get_list_fb(order_id)
        if order_list:
            return [d["voucherOrderInfoBean"]["productId"] for d in order_list]

    def get_category_type_fb(self, order_id):
        """获取个人消费场景"""
        order_list = self.get_list_fb(order_id)
        try:
            return order_list[0]["voucherBaseInfoBean"]["orderCategoryDTO"]["key"]
        except Exception as e:
            print(e)

    def order_add_fb(self, order_id, order_category=None):
        """个人重新计入"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/orders/addPersonal"
        params = {
            "version": "2",
        }
        if order_category is None:
            order_category = self.get_category_type_fb(order_id)
        data = {"order_category": order_category}
        if str(order_category) in {"7"}:
            ticket_id_list = set(self.get_ticket_id_fb(order_id))
            for ticket_id in ticket_id_list:
                data.update({"order_id_list": [ticket_id]})
                print("票id:", ticket_id, "订单id:", order_id)
                res = self.post(url, params=params, data=data)
                print(res.text)
                yield res.json()
        else:
            data.update({"order_id_list": [order_id]})
            res = self.post(url, params=params, data=data)
            print(res.text)
            yield res.json()

    def batch_add_fb(self, *order_ids):
        """个人批量重新计入"""
        if isinstance(order_ids, str):
            order_ids = [order_ids]
        for order_id in order_ids:
            responses = self.order_add_fb(order_id)
            for res in responses:
                if res.get("code") != 0:
                    self.error_list.append(order_id)
        if self.error_list:
            return self.error_list
        else:
            return True

    def bill_update_fb(self, bill_id, order_category=None):
        """账单重新计入"""
        order_ids = self.get_bill_order_ids_fb(bill_id, order_category)
        self.batch_add_fb(*order_ids)


if __name__ == '__main__':
    s = SettlementOrdersUpdate()
    ids = ['63ba89c9e4b0525701b68a1e']
    a = s.batch_add(*ids)
    # a = s.order_add("63ba89c9e4b0525701b68a1e")
    # a = s.bill_update_sw("63e1ecd8e86cf30c236bd7c4")
    # a = s.order_add_fb("63e23010e4b0171cc68dba35")
    # a = s.get_list_count_fb("63e1ecd8e86cf30c236bd7c4")
    # a = s.get_bill_order_ids_fb("63e1ecd8e86cf30c236bd7c4")
    # s.bill_update_fb("63e1ecd8e86cf30c236bd7c4")
    # print(s.error_list)
    print(a)
