# coding:utf-8
import pymysql
import sqlite3
from retrying import retry
from utils.Log import logger


class DBHandle:
    def __init__(self, which_db, auto_close=True):
        self.DB = which_db
        self.auto_close = auto_close
        self.connection = None

    @retry(stop_max_attempt_number=10)
    def __connect(self):
        try:
            if self.DB['TYPE'].lower() == 'mysql':
                self.conn = pymysql.connect(**self.DB['DBINFO'])
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            elif self.DB['TYPE'].lower() == 'sqlite':
                self.conn = sqlite3.connect(self.DB['DBINFO'])
                self.cur = self.conn.cursor()
            else:
                logger.info('%s is Unsupported Type' % self.DB['TYPE'])
        except Exception as err:
            logger.error('数据库接连出错, 错误信息:\n%s' % err)
            assert False

    def query(self, sql, fetchone=False):
        """
        execute custom sql query
        """
        if not self.connection:
            self.__connect()
        with self.cur as cursor:
            if not sql:
                return
            cursor.execute(sql)
            self.conn.commit()  # not auto commit
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    def close(self):
        if self.connection:
            self.cur.close()
            self.conn.close()

    def __del__(self):
        """close mysql database connection"""
        self.close()


if __name__ == '__main__':
    from config.db_config import StereoSettlementDb
    sql = DBHandle(StereoSettlementDb)
    print(sql.query("select * from bill_summary where id = '6333c5292caeca35c7152ef6'")[0]["BILL_NO"])