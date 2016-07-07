#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

__author__ = "LoRexxar"

logger = logging.getLogger('Sqlier')


def log(name, loglevel):

    f = open("./log/" + name + ".log", 'a+')
    Log_Handle = logging.StreamHandler(f)
    # Log_Handle = logging.StreamHandler(sys.stdout)
    FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] [%(thread)d] %(message)s", "%H:%M:%S")
    Log_Handle.setFormatter(FORMATTER)
    logger.addHandler(Log_Handle)
    logger.setLevel(loglevel)