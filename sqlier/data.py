#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from lib.log import logger
from config import conf

__author__ = "LoRexxar"


class DataProcess:
    # 获取返回数据
    def __init__(self):
        self.url = conf['url']
        # self.sqlimethod = conf['SqliMethod']
        # self.payload = Queue.Queue

    def GetLen(self, payload):
        data = payload
        r = conf['s'].get(self.url+"?"+data)
        lens = len(r.text.encode('utf-8'))
        return lens

    def GetData(self, payload):
        data = payload
        r = conf['s'].get(self.url + "?" + data)
        return r.text.encode('utf-8')

    def GetBuildData(self, payload, llen):
        data = payload
        r = conf['s'].get(self.url+"?"+data)
        lens = len(r.text.encode('utf-8'))
        # print r.text.encode('utf-8')
        if lens == llen:
            return 1
        else:
            return 0

    def GetTimeData(self, payload, dtime):
        data = payload
        ptime = time.time()
        r = conf['s'].get(self.url + "?" + data)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime-ptime > dtime:
            return 1
        else:
            return 0

    def PostLen(self, payload):
        data = payload
        r = conf['s'].post(self.url, data=data)
        return len(r.text.encode('utf-8'))

    def PostData(self, payload):
        data = payload
        r = conf['s'].post(self.url, data=data)
        return r.text.encode('utf-8')

    def PostBuildData(self, payload, llen):
        data = payload
        r = conf['s'].post(self.url, data=data)
        lens = len(r.text.encode('utf-8'))
        # print r.text.encode('utf-8')
        if lens == llen:
            return 1
        else:
            return 0

    def PostTimeData(self, payload, dtime):
        data = payload
        ptime = time.time()
        r = conf['s'].post(self.url, data=data)
        rr = r.text.encode('utf-8')
        ntime = time.time()
        if ntime - ptime > dtime:
            return 1
        else:
            return 0

