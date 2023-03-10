# coding:utf-8
import arrow
import re
from utils.json_utils import get_json_value
from stereo.http_handle import HttpHandle


class SettlementCommon(HttpHandle):
    def __init__(self):
        super(SettlementCommon, self).__init__()

    def detail_add(self, bill_id, bill_detail_id, reason="python脚本加入账单"):
        """将订单bill_detail_id移到账单bill_id中"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/add"
        params = {
            "version": 2,
        }
        data = {
            "bill_id": bill_id,
            "bill_detail_id": bill_detail_id,
            "reason": reason
        }
        res = self.post(url, params=params, data=data)
        print(res.json())
        return res.json()

    def get_list_count(self, bill_id, order_category=None):
        """商务账单bill_id下的所有订单数量"""
        url = self.settlement_url + "/api/settlement/settlement/bill/manage/detail/orders/new"
        params = {
            "bill_id": bill_id,
            "pageIndex": 1,
            "pageSize": 30
        }
        if order_category:
            params.update({"order_category": order_category})
        res = self.get(url, params=params)
        count = res.json().get("count")
        return count

    def get_bill_order_ids(self, bill_id, order_category=None):
        """账单bill_id下的所有订单"""
        if self.judgment_bill(bill_id):
            bill_id = self.get_bill_id(bill_id)
        url = self.settlement_url + "/api/settlement/settlement/bill/manage/detail/orders/new"
        count = self.get_list_count(bill_id, order_category)
        if count is None:
            raise ValueError("列表数量获取失败了")
        size = 30
        order_ids = set()
        for i in range(1, int(count / size) + 2):
            params = {
                "bill_id": bill_id,
                "pageIndex": i,
                "pageSize": size
            }
            if order_category:
                params.update({"order_category": order_category})
            res = self.get(url, params=params)
            for d in res.json()["data"]:
                order_ids.add(d["orderId"])
        return list(order_ids)

    def get_list_count_fb(self, bill_id, order_category=None):
        """个人账单bill_id下的所有订单数量"""
        url = self.settlement_url + "/api/settlement/settlement/bill/manage/detail/voucher/orders/new"
        params = {
            "bill_id": bill_id,
            "pageIndex": 1,
            "pageSize": 1
        }
        if order_category:
            params.update({"order_category": order_category})
        res = self.get(url, params=params)
        count = res.json().get("count")
        return count

    def get_bill_order_ids_fb(self, bill_id, order_category=None):
        """个人账单bill_id下的所有订单"""
        if self.judgment_bill(bill_id):
            bill_id = self.get_bill_id(bill_id)
        url = "https://stereo-settlement-web-fat.fenbeijinfu.com/api/settlement/settlement/bill/manage/detail/voucher/orders/new"
        count = self.get_list_count_fb(bill_id, order_category)
        if count is None:
            raise ValueError("列表数量获取失败了")
        size = 30
        order_ids = set()
        for i in range(1, int(count / size) + 2):
            params = {
                "bill_id": bill_id,
                "pageIndex": i,
                "pageSize": size
            }
            res = self.get(url, params=params)
            for d in res.json()["data"]:
                order_ids.add(d["orderId"])
        return list(order_ids)

    def verify_status(self, bill_detail_id, verify_status="3", reason="python脚本对账"):
        """
        对账
        Args:
            bill_detail_id: 明细编号
            verify_status: 3-对账中 4-对账无差异 5-对账有差异
            reason:

        Returns:

        """
        url = self.settlement_url + "/api/settlement/settlement/bill/verify/new/status"
        data = {
            "billDetailId": bill_detail_id,
            "verifyStatus": verify_status
        }
        if verify_status in {"4", "5"}:
            data.update({"reason": reason})
        params = {
            "v": int(arrow.now().timestamp() * 1000),
        }
        res = self.post(url, params=params, data=data, form=True)
        return res.json()

    def get_list(self, order_id):
        """获取订单详情"""
        url = self.settlement_url + "/api/settlement/settlement/bill/all/detail/listV2"
        params = {
            "v": int(arrow.now().timestamp() * 1000),
            "order_id": order_id,
            "pageIndex": 1,
            "pageSize": 20
        }
        res = self.get(url, params=params)
        if res.json()["data"] and len(res.json()["data"]) > 0:
            return res.json()["data"]

    def get_bill_id(self, bill_no):
        """获取bill_id"""
        url = self.settlement_url + "/api/settlement/settlement/bill/manage"
        params = {
            "v": int(arrow.now().timestamp() * 1000),
            "bill_no": bill_no,
            "pageIndex": 1,
            "pageSize": 20
        }
        res = self.get(url, params=params)
        return get_json_value(res.json(), "@bill_id[bill_no={}]".format(bill_no))

    @staticmethod
    def judgment_bill(bill):
        if re.match("[0-9]{8,}", bill):
            return True

if __name__ == "__main__":
    common = SettlementCommon()
    # res = common.get_bill_order_ids_fb("63bd3094bf14007dd3e1f811")
    res = common.get_bill_id("76161556020231101")
    print(res)
