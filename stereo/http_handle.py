# coding:utf-8
import requests
from copy import deepcopy
from utils.Log import logger


class HttpHandle:
    def __init__(self, env=None):
        if env is None:
            env = "fat"
        self.env = env
        self.http = requests.session()
        self.headers = {'content-type': 'application/json'}
        self.setlement_header = {"Host": "stereo-settlement-web-fat.fenbeijinfu.com", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        if self.env == "fat":
            self.host = "https://stereo-portal-web-fat.fenbeijinfu.com"
            self.old_host = "https://stereo-fat.fenbeijinfu.com"
            self.stereo_host = "stereo-fat.fenbeijinfu.com"
            self.settlement_url = "https://stereo-settlement-web-fat.fenbeijinfu.com"
            self.username = "18612962340"
            self.password = "Fbt20220811"
        elif self.env == "fat2":
            self.host = "https://stereo-portal-web-fat2.fenbeijinfu.com"
            self.old_host = "https://stereo-fat2.fenbeijinfu.com"
            self.stereo_host = "stereo-fat2.fenbeijinfu.com"
            self.settlement_url = "https://stereo-settlement-web-fat2.fenbeijinfu.com"
            self.username = "18612962340"
            self.password = "Fbt20220811"
        self.thread_count = 10
        self.token = None
        self.result = None
        self.login()

    def login(self):
        logger.info("登录系统获取cookie")
        url = self.host + "/api/pl/stereo/portal/sys/login"
        validateCode = "test"  # 测试环境没有验证校验码
        data = {"username": self.username, "password": self.password, "validateCode": validateCode}
        res = self.http.post(url, json=data)
        print(res.text)
        token = res.json()["data"]["token"]
        self.token = token
        self.headers = {"X-Auth-Token": token}
        self.setlement_header.update(self.headers)
        self.http.headers.update(self.headers)
        self.stereo_hearder = deepcopy(self.headers)
        self.stereo_hearder.update({"Cookie": "X-Auth-Token={}".format(token), "Host": self.stereo_host})
        logger.info("更新http请求header： {}".format(self.headers))
        return res.json()

    def get(self, url, params=None, **kwargs):
        if not url.startswith("http"):
            url = self.host + url
        try:
            if "headers" not in kwargs:
                kwargs['headers'] = self.headers
            res = self.http.get(url, params=params, **kwargs)
        except Exception as err:
            logger.error(err)
            assert False
        if res.status_code == 200:
            logger.info('发送get请求: %s 服务器返回: %s' % (res.url, res.status_code))
        elif res.status_code == 301:
            logger.info('发送get请求: %s 服务器返回: %s\n返回内容:\n%s' %
                        (res.url, res.status_code, res.content.decode('utf-8', 'ignore')))
        else:
            logger.error('发送get请求: %s 服务器返回: %s\n返回内容:\n%s' %
                         (res.url, res.status_code, res.content.decode('utf-8', 'ignore')))
            assert False
        return res

    def post(self, url, data=None, form=False, **kwargs):
        if not url.startswith("http"):
            url = self.host + url
        try:
            if "headers" not in kwargs:
                kwargs['headers'] = self.headers
            if form:
                res = self.http.post(url, data=data, **kwargs)
            else:
                res = self.http.post(url, json=data, **kwargs)
        except Exception as err:
            logger.error(err)
            assert False
        if res.status_code == 200:
            logger.info('发送post请求: %s  服务器返回: %s data: %s  ' %
                        (res.url, res.status_code, data))
        else:
            logger.error('发送post请求: %s 请求参数: %s 请求头: %s 服务器返回: %s\n返回内容:\n%s' %
                         (res.url, data, self.headers, res.status_code, res.content.decode('utf-8', 'ignore')))
            assert False
        return res


if __name__ == "__main__":
    http = HttpHandle()
    res = http.login()
    print(res)
