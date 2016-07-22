#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
from urllib import quote
from lib.log import logger
from config import BaseConfig

__author__ = "LoRexxar"


class DataProcess(BaseConfig):
    # 获取返回数据
    def __init__(self):
        BaseConfig.__init__(self)

    def GetLen(self, payload):
        data = quote(payload)
        r = self.s.get(self.url+"?"+data)
        lens = len(r.text.encode('utf-8'))
        return lens

    def GetData(self, payload):
        data = payload
        r = self.s.get(self.url + "?" + data)
        return r.text.encode('utf-8')

    def GetBuildData(self, payload, llen):
        data = payload
        r = self.s.get(self.url + "?" + data)
        lens = len(r.text.encode('utf-8'))
        # print r.text.encode('utf-8')
        # print payload
        if lens == llen:
            return 1
        else:
            return 0

    def GetTimeData(self, payload, dtime):
        data = payload
        ptime = time.time()
        r = self.s.get(self.url + "?" + data)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime-ptime > dtime:
            return 1
        else:
            return 0

    def PostLen(self, payload):
        data = payload
        r = self.s.post(self.url, data=data)
        return len(r.text.encode('utf-8'))

    def PostData(self, payload):
        data = payload
        r = self.s.post(self.url, data=data)
        return r.text.encode('utf-8')

    def PostBuildData(self, payload, llen):
        data = payload
        r = self.s.post(self.url, data=data)
        lens = len(r.text.encode('utf-8'))
        # print r.text.encode('utf-8')
        if lens == llen:
            return 1
        else:
            return 0

    def PostTimeData(self, payload, dtime):
        data = payload
        ptime = time.time()
        r = self.s.post(self.url, data=data)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime - ptime > dtime:
            return 1
        else:
            return 0

