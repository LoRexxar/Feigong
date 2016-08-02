#!/usr/bin/env python
# -*- coding:utf-8 -*-

from urllib import quote
from lib.log import logger

__author__ = "LoRexxar"


class DealPayload:
    def __init__(self, sqlirequest, payload, requestformat, filter):
        """
        payload处理函数初始化，这里将会通过传入的参数，来生成传出的payload
        """
        self.payload = payload
        self.requestformat = requestformat
        self.filter = filter
        self.sqlirequest = sqlirequest

    def construct_request(self, payload):

        # 首先要通过自定义的替换表
        for key in self.filter:
            payload = payload.replace(key, self.filter[key])

        # 如果是get请求,我们需要把payload url编码一下
        if self.sqlirequest == "GET":
            payload = quote(payload)
            return self.requestformat.replace('BSqlier', payload)
        elif self.sqlirequest == "POST":
            for key in self.requestformat:
                if self.requestformat[key] == "BSqlier":
                    self.requestformat[key] = payload
            return self.requestformat
        else:
            logger.error("self.Sqlimethod can not be identified")
            exit(0)

    def construct_normal_payload(self, select=None, source = None, conditions = None, limit = 0):
        payload = self.payload

        # select为select的部分，替换自定义的BSqlier
        if select is not None:
            payload = self.payload.replace('\'BSqlier\'', select)

        # source为from后面的部分，from的位置稳定在select后面，所以可以通过

        return self.construct_request(payload)


