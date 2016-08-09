#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from urllib import quote
from config import BaseConfig
from lib.log import logger

__author__ = "LoRexxar"


class DataProcess(BaseConfig):
    # 获取返回数据
    def __init__(self):
        BaseConfig.__init__(self)

    def GetLen(self, payload):
        data = quote(payload)
        try:
            r = self.s.get(self.url + "?" + data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        lens = len(r.text.encode('utf-8'))
        return lens

    def GetData(self, payload):
        data = payload
        try:
            r = self.s.get(self.url + "?" + data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        return r.text.encode('utf-8')

    def GetBuildData(self, payload, llen):
        data = payload
        try:
            r = self.s.get(self.url + "?" + data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
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
        try:
            r = self.s.get(self.url + "?" + data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime-ptime > dtime:
            return 1
        else:
            return 0

    def PostLen(self, payload):
        data = payload
        r = self.s.post(self.url, data=data, headers=self.headers)
        return len(r.text.encode('utf-8'))

    def PostData(self, payload):
        data = payload
        try:
            r = self.s.post(self.url, data=data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        return r.text.encode('utf-8')

    def PostBuildData(self, payload, llen):
        data = payload
        try:
            r = self.s.post(self.url, data=data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        lens = len(r.text.encode('utf-8'))
        # print r.text.encode('utf-8')
        if lens == llen:
            return 1
        else:
            return 0

    def PostTimeData(self, payload, dtime):
        data = payload
        ptime = time.time()
        try:
            r = self.s.post(self.url, data=data, headers=self.headers)
        except:
            logger.error("Time out...")
            exit(0)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime - ptime > dtime:
            return 1
        else:
            return 0

