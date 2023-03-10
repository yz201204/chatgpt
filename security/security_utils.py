import requests
import random
import datetime


class Security:
    def __init__(self):
        self.http = requests.session()
        self.headers_sz = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
            "referer": "http://www.szse.cn/market/trend/index.html",
        }
        self.headers_sh = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
            "referer": "http://www.sse.com.cn/",
        }
        self.url_sjs_v5 = 'https://www.szse.cn/api/market/ssjjhq/getTimeData'
        self.url_sjs_pe_pb = "http://www.szse.cn/api/report/ShowReport/data"
        self.url_sjs_sz = 'http://www.szse.cn/api/report/ShowReport/data'
        self.url_sh_fast = "http://query.sse.com.cn/commonQuery.do"
        self.url_sh_v1 = "http://yunhq.sse.com.cn:32041/v1/sh1/snap/"
        self.delta_day = 3

    @staticmethod
    def zdf(percent):
        if percent is not None and percent != "None":
            percent = float(percent)
            if percent >= 0:
                return "\x1b[31m{}\x1b[m".format(percent)
            return "\x1b[32m{}\x1b[m".format(percent)

    def price_search(self, code):
        market = self.market(code)
        if market == 1:
            return self.sz_search(code)
        elif market == 2:
            return self.sh_search(code)

    def sz_search(self, code):
        info = dict()
        params_sjs_v5 = {"marketId": 1, 'code': code, "random": random.random()}
        date = datetime.datetime.now()
        ss = date.replace(hour=15, minute=0).timestamp()
        now = date.timestamp()
        if now > ss:
            txt_date = date.strftime('%Y-%m-%d')
        else:
            txt_date = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        params_pe_pb = {"SHOWTYPE": 'JSON', 'CATALOGID': '1815_stock', "TABKEY": 'tab1', 'txtDMorJC': code,
                        'txtBeginDate': txt_date, 'txtEndDate': txt_date, 'radioClass': '00%2C20%2C30',
                        'txtSite': 'all', 'random': random.random()}
        params_sjs_sz = {"SHOWTYPE": 'JSON', 'CATALOGID': 1110, 'TABKEY': 'tab1', 'txtDMorJC': code,
                         "random": random.random()}
        v5 = requests.get(self.url_sjs_v5, params=params_sjs_v5, headers=self.headers_sz).json()['data']
        pe_pb = requests.get(self.url_sjs_pe_pb, params=params_pe_pb, headers=self.headers_sz).json()[0]
        sz = requests.get(self.url_sjs_sz, params=params_sjs_sz, headers=self.headers_sz).json()
        info['名称'] = v5.get('name')
        info['价格'] = v5.get('now')
        info['最高'] = v5.get('high')
        info['最低'] = v5.get('low')
        info['涨跌幅'] = "{}%".format(v5.get('deltaPercent'))
        info['涨跌额'] = v5.get('delta')
        info['成交量'] = "{}万手".format(round(v5.get('volume') / 10000, 2)) if v5.get('volume') else None
        info['成交额'] = "{}亿".format(round(v5.get('amount') / 100000000, 2)) if v5.get('amount') else None
        try:
            info['市盈率'] = pe_pb.get('data')[0]['syl1']
        except:
            try:
                date = datetime.datetime.now()
                txt_date = (date - datetime.timedelta(days=self.delta_day)).strftime('%Y-%m-%d')
                params_pe_pb = {"SHOWTYPE": 'JSON', 'CATALOGID': '1815_stock', "TABKEY": 'tab1', 'txtDMorJC': code,
                                'txtBeginDate': txt_date, 'txtEndDate': txt_date, 'radioClass': '00%2C20%2C30',
                                'txtSite': 'all', 'random': random.random()}
                pe_pb = requests.get(self.url_sjs_pe_pb, params=params_pe_pb, headers=self.headers_sz).json()[0]
                info['市盈率'] = pe_pb.get('data')[0]['syl1']
            except:
                pass
        try:
            info['市值'] = "{}亿".format(round(float(sz[0]['data'][0]['agzgb']) * float(v5.get('now')), 2))
            info['换手率'] = round((v5.get('volume') * 100 / (float(sz[0]['data'][0]['agltgb']) * 100000000) * 100),
                                1)
            info['总股本'] = float(sz[0]['data'][0]['agzgb'])
            info['流通股本'] = float(sz[0]['data'][0]['agltgb'])
            info['上市时间'] = sz[0]['data'][0]['agssrq']
            info['板块'] = sz[0]['data'][0]['bk']
            info['行业'] = sz[0]['data'][0]['sshymc']
        except:
            pass
        prices = v5.get('sellbuy5')
        info['五档价格'] = []
        if prices:
            for price in prices:
                info['五档价格'].append("{}-{}".format(price.get('price'), price.get('volume')))
        return info

    def sh_search(self, code):
        info = dict()
        date = datetime.datetime.now()
        now = date.timestamp()
        txt_date_p = (date - datetime.timedelta(days=1))
        txt_date = txt_date_p.strftime('%Y-%m-%d')
        txt_date_month = txt_date_p.strftime('%Y-%m')
        txt_date_year = txt_date_p.strftime('%Y')
        params_v1 = {"callback": "",
                     "select": "name,last,chg_rate,change,amount,volume,open,prev_close,ask,bid,high,low,tradephase,turnover_ratio,totalValue,amp_rate,circulating,up_limit,down_limit,hlt_tag,gdr_ratio,gdr_prevpx,gdr_currency",
                     "_": str(int(now))}
        params_pe_pb = {"callback": '', 'FUNDID': '', "inMonth": '', 'inYear': '',
                        'searchDate': '', 'sqlId': 'COMMON_SSE_CP_GPJCTPZ_GPLB_CJGK_MRGK_C', 'SEC_CODE': code,
                        'TX_DATE': txt_date, 'TX_DATE_MON': txt_date_month, 'TX_DATE_YEAR': txt_date_year,
                        "_": str(int(now))}
        try:
            sh_pe = requests.get(self.url_sh_fast, params=params_pe_pb, headers=self.headers_sh).json()['result'][0]
        except:
            try:
                date = datetime.datetime.now()
                now = date.timestamp()
                txt_date_p = (date - datetime.timedelta(days=self.delta_day))
                txt_date = txt_date_p.strftime('%Y-%m-%d')
                txt_date_month = txt_date_p.strftime('%Y-%m')
                txt_date_year = txt_date_p.strftime('%Y')
                params_pe_pb = {"callback": '', 'FUNDID': '', "inMonth": '', 'inYear': '',
                                'searchDate': '', 'sqlId': 'COMMON_SSE_CP_GPJCTPZ_GPLB_CJGK_MRGK_C',
                                'SEC_CODE': code,
                                'TX_DATE': txt_date, 'TX_DATE_MON': txt_date_month, 'TX_DATE_YEAR': txt_date_year,
                                "_": str(int(now))}
                sh_pe = requests.get(self.url_sh_fast, params=params_pe_pb, headers=self.headers_sh).json()['result'][0]
            except:
                sh_pe = dict()
        try:
            sh_v1 = requests.get("{}{}".format(self.url_sh_v1, code), params=params_v1, headers=self.headers_sh).text
            sh_v1 = eval(sh_v1)['snap']
        except:
            sh_v1 = [i for i in range(30)]
        info['名称'] = sh_v1[0]
        info['价格'] = sh_v1[1]
        info['最高'] = sh_v1[10]
        info['最低'] = sh_v1[11]
        info['涨跌幅'] = "{}%".format(sh_v1[2])
        info['涨跌额'] = sh_v1[3]
        info['成交量'] = "{}万手".format(round(sh_v1[5] / 1000000, 2))
        info['成交额'] = "{}亿".format(round(sh_v1[4] / 100000000, 2))
        info['市盈率'] = sh_pe.get('PE_RATE')
        info['市值'] = "{}亿".format(round(sh_v1[14] / 100000000, 2))
        info['五档价格'] = []
        for i in range(5):
            index = 2 * i
            info['五档价格'].append("{}-{}".format(sh_v1[8][index], round(sh_v1[8][index + 1] / 100)))
        for i in range(5):
            index = 2 * i
            info['五档价格'].append("{}-{}".format(sh_v1[9][index], round(sh_v1[9][index + 1] / 100)))
        return info

    @staticmethod
    def market(code):
        if code.startswith("0"):
            return 1
        elif code.startswith("6"):
            return 2
        return 1


if __name__ == '__main__':
    s = Security()
    s.price_search("002864")
    # s.price_search("603995")
