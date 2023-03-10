# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

from flask import request, jsonify
from flask import Blueprint
from utils.Log import logger
from lib.ding_msg_controller import DingMsgController
from lib.api_handler import ApiHandler
from lib.send_ding_msg import SendDingMsg
import json
import time

jira_ding_api = Blueprint('jira_ding_api', __name__)


@jira_ding_api.route('/', methods=['GET'])
def deploy_check():
    resp = {"code": 0, "status": 200, "msg": "部署成功"}
    return jsonify(resp)


# 处理钉钉机器人outgoing msg
@jira_ding_api.route('/atDingTalk', methods=['POST'])
def atDingTalk():
    if request.method == 'POST':
        post_form = json.loads(request.data)
        sender_id = post_form['senderId']
        content = post_form['text']
        msg = content['content'].strip()
        session_webhook = post_form['sessionWebhook']
        logger.info("sessionWebhook====" + session_webhook)
        logger.info('atDingTalkMsg=====' + msg)
        comment = DingMsgController().main(msg)
        SendDingMsg().send_msg(session_webhook, comment, at_dingtalk_ids=[sender_id])
        return {"code": 0, "status": 200, "msg": comment}
    else:
        return {"code": 9999, "status": 405, "msg": "Method not allowed"}
