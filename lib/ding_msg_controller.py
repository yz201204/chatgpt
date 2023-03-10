# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import arrow
from utils.Log import logger
from lib.chat_gpt import ChatGPT

# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import re

import arrow
from utils.Log import logger
from stereo.settlement_orders_update import SettlementOrdersUpdate
from stereo.settlement_orders_bill_verify import SettlementOrdersBillVerify
from stereo.settlement_orders_detail_verify import SettlementOrdersDetailVerify
from stereo.settlement_orders_add import SettlementOrdersAdd
from security.security_utils import Security


class DingMsgController(object):
    """接收钉钉消息处理的处理类"""

    def __init__(self):
        self.demo_msg = """测试组机器人目前支持以下功能：\n"""
        self.demo_list = list()
        self.help = '您好，如果想了解我当前的使用方式你可以通过@我 demo获取！'

    def main(self, message):
        """
        钉钉消息主方法
        :param message:
        :return:
        """
        self.demo_list_method()
        self.demo_msg += "\n".join("{}、{}".format(i, j) for i, j in enumerate(self.demo_list, 1))
        logger.info('=' * 10 + '@机器人 原始消息体如下：' + str(message))
        if message == "" or message is None:
            return ""
        elif message == 'demo':
            return self.demo_msg
        elif message.startswith("对账"):
            return self.settlement_verify(message)
        elif message.startswith("账单对账商务"):
            return self.settlement_verify_bill(message)
        elif message.startswith("账单对账分贝"):
            return self.settlement_verify_bill_fb(message)
        elif message.startswith("明细对账商务"):
            return self.settlement_verify_detail(message)
        elif message.startswith("明细对账分贝"):
            return self.settlement_verify_detail_fb(message)
        elif message.startswith("计入商务"):
            return self.settlement_orders_add(message)
        elif message.startswith("计入分贝"):
            return self.settlement_orders_add_fb(message)
        elif message.startswith("账单重新计入商务"):
            return self.settlement_bill_all_orders_add(message)
        elif message.startswith("账单重新计入分贝"):
            return self.settlement_bill_all_orders_add_fb(message)
        elif message.startswith("神州用车"):
            return self.vehicle_shen_zhou(message)
        elif message.startswith("首汽用车"):
            return self.vehicle_shou_qi(message)
        elif message.startswith("账单订单移动"):
            return self.settlement_bill_move(message)
        elif message.startswith("明细订单移动"):
            return self.settlement_detail_move(message)
        elif message.startswith("汽车出票"):
            return self.bus_pay_notify(message)
        elif re.match('[0-9]{6}', message):
            return self.price_search(message)
        else:
            return self.help

    @staticmethod
    def price_search(message):
        return Security().price_search(message)

    @staticmethod
    def settlement_verify(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：对账:订单编号1/明细编号1[,订单编号2/明细编号2]"
        message = message.replace("：", ":")
        ids = message.split(":")[1]
        if not ids:
            return "请输入编号，参考格式：对账:订单编号1/明细编号1[,订单编号2/明细编号2]"
        ids_list = ids.replace("，", " ").replace(",", " ").split()
        return SettlementOrdersBillVerify().batch_verify_status(*ids_list)

    @staticmethod
    def settlement_verify_bill(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：账单对账商务:账单编号/账单id[,场景id]"
        message = message.replace("：", ":")
        bill_info = message.split(":")[1]
        if not bill_info:
            return "请输入账单编号，参考格式：账单对账商务:账单编号/账单id[,场景id]"
        bill = bill_info.replace("，", " ").replace(",", " ").split()
        return SettlementOrdersBillVerify().batch_verify_status_bill(*bill)

    @staticmethod
    def settlement_verify_bill_fb(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：账单对账分贝:账单编号/账单id[,场景id]"
        message = message.replace("：", ":")
        bill_info = message.split(":")[1]
        if not bill_info:
            return "请输入账单编号，参考格式：账单对账分贝:账单编号/账单id[,场景id]"
        bill = bill_info.replace("，", " ").replace(",", " ").split()
        return SettlementOrdersBillVerify().batch_verify_status_bill_fb(*bill)

    @staticmethod
    def settlement_orders_add(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：计入商务:订单id1[,订单id2]"
        message = message.replace("：", ":")
        ids = message.split(":")[1]
        if not ids:
            return "请输入订单id，参考格式：计入商务:订单id1[,订单id2]"
        ids_list = ids.replace("，", " ").replace(",", " ").split()
        return SettlementOrdersUpdate().batch_add(*ids_list)

    @staticmethod
    def settlement_orders_add_fb(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：计入分贝:订单id1[,订单id2]"
        message = message.replace("：", ":")
        ids = message.split(":")[1]
        if not ids:
            return "请输入订单id，参考格式：计入分贝:订单id1[,订单id2]"
        ids_list = ids.replace("，", " ").replace(",", " ").split()
        return SettlementOrdersUpdate().batch_add_fb(*ids_list)

    @staticmethod
    def settlement_bill_all_orders_add(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：账单重新计入商务:账单编号/id"
        message = message.replace("：", ":")
        bill_id = message.split(":")[1]
        if not bill_id:
            return "请输入bill_id，参考格式：账单重新计入商务:账单编号/id"
        settlement = SettlementOrdersUpdate()
        order_ids = settlement.get_bill_order_ids(bill_id)
        settlement.batch_add_thread(*order_ids)

    @staticmethod
    def settlement_bill_all_orders_add_fb(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：账单重新计入分贝:账单编号/id"
        message = message.replace("：", ":")
        bill_id = message.split(":")[1]
        if not bill_id:
            return "请输入bill_id，参考格式：账单重新计入分贝:账单编号/id"
        settlement = SettlementOrdersUpdate()
        order_ids = settlement.get_bill_order_ids_fb(bill_id)
        settlement.batch_add_fb(*order_ids)

    @staticmethod
    def vehicle_shen_zhou(message):
        from vehicle.shenzhou import ShenZhou
        if ":" not in message and "：" not in message:
            return ShenZhou().run()
        message = message.replace("：", ":")
        fees = message.split(":")[1]
        if not fees:
            return "请输入费用，参考格式：神州用车[:1,2,3,4,5,6]"
        fee_list = fees.replace("，", " ").replace(",", " ").split()
        if len(fee_list) != 6:
            return "请输入6个费用，参考格式：神州用车[:1,2,3,4,5,6]"
        return ShenZhou().run(fees=fee_list)

    @staticmethod
    def vehicle_shou_qi(message):
        from vehicle.shouqi import ShouQi
        if ":" not in message and "：" not in message:
            return "请输入单号，参考格式：首汽用车:首汽订单号"
        message = message.replace("：", ":")
        order_no = message.split(":")[1]
        if not order_no:
            return "请输入首汽订单号，参考格式：首汽用车:首汽订单号"
        return ShouQi().run(order_no)

    def settlement_verify_detail(self, message):
        print(message, "开始")
        print("查询条件可修改detail_search")
        settlement = SettlementOrdersDetailVerify()
        settlement.detail_search = self.sw_detail_search()
        return settlement.batch_verify_status()

    def settlement_verify_detail_fb(self, message):
        print(message, "开始")
        print("查询条件可修改detail_search")
        settlement = SettlementOrdersDetailVerify()
        settlement.detail_search = self.fb_detail_search()
        return settlement.batch_verify_status_fb()

    @staticmethod
    def settlement_bill_move(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：账单订单移动::bill_id1/bill_no1,bill_id2/bill_no2"
        message = message.replace("：", ":")
        bill_id = message.split(":")[1]
        if not bill_id:
            return "请输入bill_id，参考格式：账单订单移动::bill_id1/bill_no1,bill_id2/bill_no2"
        settlement = SettlementOrdersAdd()
        bill_ids = bill_id.replace("，", " ").replace(",", " ").split()
        settlement.batch_detail_move_thread(*bill_ids)

    def settlement_detail_move(self, message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：明细订单移动::bill_id/bill_no"
        message = message.replace("：", ":")
        bill_id = message.split(":")[1]
        if not bill_id:
            return "请输入bill_id，参考格式：明细订单移动::bill_id/bill_no"
        settlement = SettlementOrdersAdd()
        settlement.detail_search = self.sw_detail_search_move()
        settlement.batch_add_detail_search(bill_id)

    @staticmethod
    def bus_pay_notify(message):
        if ":" not in message and "：" not in message:
            return "格式有误，参考格式：汽车出票:供应商订单id"
        message = message.replace("：", ":")
        bill_id = message.split(":")[1]
        if not bill_id:
            return "请输入bill_id，参考格式：汽车出票:供应商订单id"
        from bus.bus_notify import BusNotify
        return BusNotify().pay_notify(bill_id)

    @staticmethod
    def sw_detail_search_move():
        return {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "order_create_start_time": "2023-01-02 00:00:00",
            "order_create_end_time": "2023-02-09 23:59:59",
            "company_id": "6319a47986afcc0c8b63b10a"
        }

    @staticmethod
    def sw_detail_search():
        return {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "order_create_start_time": "2023-02-09 00:00:00",
            "order_create_end_time": "2023-02-09 23:59:59",
            "company_id": "635f96159620ee59ebf80707"
        }

    @staticmethod
    def fb_detail_search():
        return {
            "v": int(arrow.now().timestamp() * 1000),
            "pageIndex": 1,
            "pageSize": 20,
            "voucher_use_time_start_time": "2023-02-07 00:00:00",
            "voucher_use_time_end_time": "2023-02-08 23:59:59",
            "to_bill_status": 2
        }

    def demo_list_method(self):
        self.demo_list.append("对账-订单编号/明细编号，参考格式：对账:订单编号1/明细编号1[,订单编号2/明细编号2]")
        self.demo_list.append("对账-账单中入账中的商务，参考格式：账单对账商务:账单编号/账单id[,场景id]")
        self.demo_list.append("对账-账单中入账中的分贝，参考格式：账单对账商务:账单编号/账单id[,场景id]")
        self.demo_list.append("对账-将明细查询到的都对账无差异，参考格式：明细对账商务")
        self.demo_list.append("对账-将明细查询到的都对账无差异，参考格式：明细对账分贝")
        self.demo_list.append("计入商务-重新计入（自动判断票id和是否减免），参考格式：计入商务:订单id1[,订单id2]")
        self.demo_list.append("计入分贝-重新计入（自动判断票id），参考格式：计入分贝:订单id1[,订单id2]")
        self.demo_list.append("账单重新计入商务，参考格式：账单重新计入商务:账单编号/id")
        self.demo_list.append("账单重新计入分贝，参考格式：账单重新计入分贝:账单编号/id")
        self.demo_list.append("神州用车-接第一个单，参考格式：神州用车[:1,2,3,4,5,6]")
        self.demo_list.append("首汽用车，参考格式：首汽用车:首汽订单号")
        self.demo_list.append("将账单A下所有订单移动到账单B下，参考格式：账单订单移动:bill_id1/bill_no1,bill_id2/bill_no2")
        self.demo_list.append("将明细查询到的订单加入账单，参考格式：明细订单移动:bill_id/bill_no")
        self.demo_list.append("汽车出票，参考格式：汽车出票:供应商订单id")


if __name__ == '__main__':
    # msg = "对账:63bf75b78327a7152323e2af"
    msg = "账单对账商务:6406fd41ff364c69207987b8"  # 支持账单编号和账单id
    # msg = "账单对账分贝:6360b59ed2d44746e7d98908"  # 支持账单编号和账单id
    # msg = "计入商务：63e45fe50b8e2b1cd1c4a833,RMS230209105711780794573"
    # msg = "计入分贝：63db5cd0e37c7d7be00bca0d,63e09f18e4b07c5aade8fa37"
    # msg = "账单重新计入商务：63e3a37d9903e42031b35a1a"
    # msg = "账单重新计入分贝：76161565420221201"
    # msg = "神州用车:1,2,3,4,5,6"
    # msg = "首汽用车：B230309114610931000"
    # msg = "明细对账商务"
    # msg = "明细对账分贝"
    # msg = "账单订单移动:63bd3094bf14007dd3e1f811"  # 2中订单移动到1
    # msg = "明细订单移动:76161556020231101"  # 2中订单移动到1
    # msg = "汽车出票:35090531029"
    # msg = "demo"
    msg = "002628"
    # todo, 订单加入账单
    print(DingMsgController().main(msg))


