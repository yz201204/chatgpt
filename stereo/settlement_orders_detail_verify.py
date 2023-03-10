# coding:utf-8
import time
import arrow
from stereo.settlement_common import SettlementCommon


class SettlementOrdersDetailVerify(SettlementCommon):
    """
    对账
    """

    def __init__(self):
        super(SettlementOrdersDetailVerify, self).__init__()
        self.error_list = list()
        self.detail_search = {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "order_create_start_time": "2023-02-09 00:00:00",
            "order_create_end_time": "2023-02-09 23:59:59",
            "company_id": "635f96159620ee59ebf80707"
        }

    def batch_detail_add(self, bill_id):
        """批量将明细数据中的订单加入到账单bill_id中"""
        bill_detail_ids = self.get_detail_list_detail_ids()
        for bill_detail_id in bill_detail_ids:
            self.detail_add(bill_id, bill_detail_id)

    def get_detail_list_detail_ids(self):
        """获取明细数据的detail_ids，查询条件修改self.detail_search即可"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/listV2"
        params = self.detail_search
        res = self.get(url, params=params)
        detail_ids = []
        for d in res.json()["data"]:
            detail_id = d["detailBaseInfoBean"]["id"]
            detail_ids.append(detail_id)
        return detail_ids

    def get_detail_list_detail_ids_fb(self):
        """获取明细数据的detail_ids，查询条件修改self.detail_search即可"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/voucher/listV2"
        params = self.detail_search
        res = self.post(url, params=params)
        order_ids = []
        if res.json().get("data") is None:
            raise ValueError("没查询到任何数据")
        for d in res.json()["data"]:
            if d["voucherBaseInfoBean"]["verifyStatusDTO"]["key"] == 0:
                continue
            order_id = d["voucherOrderInfoBean"]["orderId"]
            order_ids.append(order_id)
        detail_ids = self.get_detail_ids_by_order_ids(order_ids)
        return detail_ids

    def get_detail_ids_by_order_ids(self, order_ids):
        url = self.settlement_url + "/api/settlement/settlement/bill/verify/new/list"
        detail_ids = []
        for order_id in order_ids:
            data = {"order_id": order_id}
            res = self.get(url, params=data)
            for d in res.json()["data"]:
                detail_ids.append(d["id"])
        return detail_ids

    def batch_verify_status(self):
        """将明细查询的结果都核对无差异"""
        bill_detail_ids = self.get_detail_list_detail_ids()
        self.batch_verify_detail_ids(bill_detail_ids)

    def batch_verify_status_fb(self):
        """将明细查询的结果都核对无差异"""
        bill_detail_ids = self.get_detail_list_detail_ids_fb()
        self.batch_verify_detail_ids(bill_detail_ids)

    def batch_verify_detail_ids(self, bill_detail_ids):
        for bill_detail_id in bill_detail_ids:
            res = self.verify_status(bill_detail_id, verify_status="3")
            time.sleep(0.1)
            print(res)
            res = self.verify_status(bill_detail_id, verify_status="4")
            print(res)

    def get_detail_list_order_ids(self):
        """获取明细数据的order_ids，查询条件修改self.detail_search即可"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/listV2"
        params = self.detail_search
        res = self.get(url, params=params)
        order_ids = []
        for d in res.json()["data"]:
            order_id = d["detailBaseInfoBean"]["orderId"]
            order_ids.append(order_id)
        return order_ids

    def train_batch_toll(self, order_ids: list, train_service_fee="5", voucher_type="2"):
        """批量代打 voucher_type 2-全量代打 5-部分代打 """
        url = self.old_host + "/stereo/order/train/batchToll"
        data = {
            "orderIds": order_ids,
            "trainVoucherModifyData": {
                "voucherType": voucher_type,
                "trainServiceFee": train_service_fee
            }
        }
        res = self.post(url, data=data)
        return res.json()

    def batch_train_batch_toll(self):
        """将明细查询的结果都批量代打"""
        order_ids = self.get_detail_list_order_ids()
        for order_id in order_ids:
            res = self.train_batch_toll([order_id])
            print(res)


if __name__ == '__main__':
    s = SettlementOrdersDetailVerify()
    # a = s.get_detail_list_detail_ids()
    # a = s.verify_status("63da0722f96f4928be6d9cf8", "5")
    # a = s.batch_detail_add("63d732d746b22546c2f5c06e")
    # a = s.batch_verify_status()
    # a = s.train_batch_toll(["63da3f3acc79b24c3889cc56"])
    # a = s.get_detail_list_order_ids()
    # a = s.batch_train_batch_toll()
    a = s.verify_status("63e36354ad4aa13c7d7c525b")
    print(a)
