# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

from utils.Log import logger
from dingtalkchatbot.chatbot import DingtalkChatbot
from lib.webhook_utils import WebHook
from utils.arrow_utils import Arrow


class SendDingMsg(object):
    def __init__(self):
        self._headers = {"content-type": "application/json", "Charset": "UTF-8"}

    def send_msg(self, webhook, message, at_dingtalk_ids=[]):
        try:
            ding = DingtalkChatbot(webhook)
            # 发送请求
            info = ding.send_text(message, False, [], at_dingtalk_ids)
            logger.info("send ding msg======")
            logger.info(info)
        except Exception as send_error:
            logger.error("send_msg error: %s", send_error)

    def send_md(self, webhook, title, text):
        '''
        发送markdown消息
        :param webhook:
        :param title:
        :param text:
        :return:
        '''
        try:
            ding = DingtalkChatbot(webhook)
            # 发送请求
            info = ding.send_markdown(title, text)
            logger.info("send ding link======")
            logger.info(info)
        except Exception as send_error:
            logger.error("send_link error: %s", send_error)


if __name__ == '__main__':
    dingtalk_webhook = WebHook("小贝").get_webhook(Arrow.get_timestamp())
    text = "test"
    SendDingMsg().send_msg(dingtalk_webhook, text)
