# *_*coding:utf-8 *_*
__author__ = 'zhe.yang'

import logging
import datetime
import os
import re
from logging.handlers import TimedRotatingFileHandler
import filepath
from pathlib import Path

rootDir = filepath.fileDir

log_path = rootDir + '/logs/'  # 当前目录
if not Path(log_path).exists():
    Path(log_path).mkdir()

# 第一步，创建一个logger
logger = logging.getLogger()

if os.getenv('LOG_LEVEL') is None:
    logger.setLevel(logging.DEBUG)  # Log等级总开关

elif os.getenv('LOG_LEVEL').lower() == 'error':
    logger.setLevel(logging.ERROR)  # Log等级总开关

elif os.getenv('LOG_LEVEL').lower() == 'warning':
    logger.setLevel(logging.WARNING)  # Log等级总开关

elif os.getenv('LOG_LEVEL').lower() == 'debug':
    logger.setLevel(logging.DEBUG)  # Log等级总开关

elif os.getenv('LOG_LEVEL').lower() == 'info':
    logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
logfile = log_path + "jira.log"
'''
TimedRotatingFileHandler类的参数意义如下:

filename：日志文件名的prefix；
when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
 “S”: Seconds
 “M”: Minutes
 “H”: Hours
 “D”: Days
 “W”: Week day (0=Monday)
 “midnight”: Roll over at midnight
interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件；
backupCount: 表示日志文件的保留个数； 不写则全保存
'''
fh = TimedRotatingFileHandler(filename=logfile, when='midnight', interval=1, backupCount=31, encoding='utf-8')
fh.suffix = "%Y-%m-%d.log"
fh.extMatch = r"^\d{4}-\d{2}-\d{2}.log$"
fh.extMatch = re.compile(fh.extMatch)
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)
