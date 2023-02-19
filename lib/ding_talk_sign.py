# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import time
import hmac
import hashlib
import base64
import urllib.parse
from utils.arrow_utils import Arrow


class DingTalkSign:
    def __init__(self, timestamp, secret):
        self.timestamp = timestamp
        self.secret = str(secret)

    def sign(self):
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign


if __name__ == '__main__':
    print(DingTalkSign(Arrow.get_timestamp(), 1).sign())
