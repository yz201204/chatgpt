# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import arrow
from utils.Log import logger
from lib.chat_gpt import ChatGPT


class DingMsgController(object):
    """接收钉钉消息处理的处理类"""

    def __init__(self):
        self.demo_msg = """欢迎使用chatGPT接口，网页版可登陆https://chat.openai.com\n账号：yangzhe2012001@hotmail.com\n密码：yangzhe2012\n"""

    def main(self, message):
        """
        钉钉消息主方法
        :param message:
        :return:
        """
        logger.info('=' * 10 + '@机器人 原始消息体如下：' + message)
        if message == "" or message is None:
            return
        elif message == 'demo':
            return self.demo_msg
        else:
            return ChatGPT().chat(message)


if __name__ == '__main__':
    msg = "你好"
    print(DingMsgController().main(msg))
