#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import colorlog
import coloredlogs

__author__ = "LoRexxar"

logger = logging.getLogger('BSqlier')


# log
def log(loglevel):
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )
    )
    logger.addHandler(handler)
    logger.setLevel(loglevel)

