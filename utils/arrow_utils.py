# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import arrow


class Arrow:
    @staticmethod
    def get_now():
        return arrow.now().format("YYYY-MM-DD")

    @staticmethod
    def get_timestamp():
        return str(int(arrow.now().timestamp() * 1000))


if __name__ == '__main__':
    a = Arrow()
    print(a.get_now())
