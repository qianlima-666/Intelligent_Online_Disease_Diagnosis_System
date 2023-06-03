# -*- coding=utf-8 -*-
# ======日志记录器======
import os
import sys
from loguru import logger

"""
@logger.catch  # 异常追溯 在 logger 里可以直接使用它提供的装饰器就可以直接进行异常捕获，而且得到的日志是无比详细的
logger.debug('')  # 排查故障时使用的低级别系统信息，通常开发时使用（蓝色）
logger.info('')  # 一般的系统信息，并不算问题（黑色）
logger.warning('')  # 描述系统发生小问题的信息，但通常不影响功能（黄色）
logger.error('')  # 描述系统发生大问题的信息，可能会导致功能不正常（红色）
logger.success('')  # （绿色）
logger.critical('')  # 描述系统发生严重问题的信息，应用程序有崩溃的风险（红色底纹）
"""

# 日志文件地址
def path_log():
    log = os.path.dirname(os.path.realpath(sys.argv[0])) + '/log'
    if not os.path.isdir(log):
        os.mkdir(log)
    # return log + "/{time:YYYY-MM-DD_HH-mm-ss}.log"
    return log + "/{time:YYYY-MM-DD}.log"


logger.add(
    path_log(),
    format="[{time:YYYY-MM-DD HH:mm:ss.SSS}] | {level: ^8} | {module}:{line} -- {message}",
    # enqueue=False
)


# 配置 控制台 日志输出格式
logger.remove(0)
logger.add(
    sink=sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: ^8}</level> | <cyan>{module}:{line}</cyan> -- <level>{message}</level>"
)
