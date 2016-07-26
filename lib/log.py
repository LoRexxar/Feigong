#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import sys
import coloredlogs

__author__ = "LoRexxar"


# log
def log(loglevel):
    # f = open("./log/" + name + ".log", 'a+')
    # Log_Handle = logging.StreamHandler(f)
    # Log_Handle = logging.StreamHandler(sys.stdout)
    # FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] [%(thread)d] %(message)s", "%H:%M:%S")
    # Log_Handle.setFormatter(FORMATTER)
    # logger.addHandler(Log_Handle)
    logger.setLevel(loglevel)

# 自定义颜色log
FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='green', bold=coloredlogs.CAN_USE_BOLD_FONT),
    filename=dict(color='magenta'),
    name=dict(color='blue'),
    threadName=dict(color='green')
)

LEVEL_STYLES = dict(
    debug=dict(color='green'),
    info=dict(color='cyan'),
    verbose=dict(color='blue'),
    warning=dict(color='yellow'),
    error=dict(color='red'),
    critical=dict(color='red', bold=coloredlogs.CAN_USE_BOLD_FONT)
)

coloredlogs.install(
    level="DEBUG",
    fmt="[%(levelname)s] [(%(threadName)s)] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
    level_styles=LEVEL_STYLES,
    field_styles=FIELD_STYLES,
)

logger = logging.getLogger('BSqlier')
