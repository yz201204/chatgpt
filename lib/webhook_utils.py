# coding=utf-8
__author__ = 'zhe.yang'

from utils.arrow_utils import Arrow
import filepath
from pathlib import Path
import json
from lib.ding_talk_sign import DingTalkSign
from utils.arrow_utils import Arrow


class WebHook:
    def __init__(self, robot):
        self.robot = robot
        ding_info = str(Path(filepath.fileDir) / "config" / "ding_info.json")
        with open(ding_info, encoding="utf-8") as f:
            self.ding = json.load(f)

    def get_sign(self):
        return self.ding.get(self.robot).get("secret")

    def get_token(self):
        return self.ding.get(self.robot).get("token")

    def get_webhook(self, timestamp):
        if self.get_sign() is None:
            return "https://oapi.dingtalk.com/robot/send?access_token={}".format(self.get_token())
        sign = DingTalkSign(timestamp, self.get_sign()).sign()
        return "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(self.get_token(), timestamp, sign)


if __name__ == '__main__':
    w = WebHook("小贝")
    print(w.get_webhook(Arrow.get_timestamp()))
