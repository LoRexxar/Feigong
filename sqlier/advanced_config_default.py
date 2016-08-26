#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import logging
from lib.Conpayload import ConPayload
from sqlier.config import BaseConfig

__author__ = "LoRexxar"


class AdvanceConfig(BaseConfig):
    def __init__(self):
        """
        进阶配置，如果对代码不够熟悉，建议不修改这部分配置
        """
        BaseConfig.__init__(self)

        # 版本号
        self.version = "V1.1.1"

        # 初始化request
        self.s = requests.Session()

        # log日志级别，debug为显示大部分信息，info为注入结果的显示
        LogLevel = (
            logging.DEBUG,
            logging.INFO,
            logging.WARN
        )
        self.loglevel = LogLevel[0]

        """
            若注入方式为build盲注，则通过返回长度判断
            永真条件的长度（盲注时需要使用），默认为0，可设置, 如果不设置会默认使用self.payload获取的返回长度为self.len
            """
        self.len = 0

        """
        若注入方式为time，你需要设置延时，建议根据自己的网络环境选择，如果网络环境较差，建议还是大一点儿
        建议2-5，现在版本还是单线程，所以时间盲注会比较慢...
        """
        self.time = 3

        """
        database可以自定义，默认为空，若为空会调用get_database(),这里是一个列表，必须按照列表格式
        self.databases_name = ['test', 'test2']（当然，如果database_name错误...则不会注到数据）
        """
        # self.databases_name = ['hctfsqli1', 'test']
        self.databases_name = []

        """
        然后是table name，tables_name的格式为字典+元组
        self.tables_name = {'hctfsqli1': ('test1', 'test2'), 'test',('test1', 'test2')}(如果有写错某些值，则会注不到数据)
        """
        # self.tables_name = {'test': ('test',), 'hctfsqli1': ('hhhhctf', 'test', 'users')}
        self.tables_name = {}

        """
        然后是self.columns_name，columns_name的格式为字典套字典+元组
        self.columns_name = {'test': {'test': ('test', 'test1', 'test2')}, 'test2': {'test': ('test', 'test1', 'test2')}}
        (同样，如果有写错的值，则会注入不到数据)
        """
        # self.columns_name = {'test': {'test': ('test',)}, 'hctfsqli1': {'test': ('test1', 'testtest', 'flag1'), 'users': ('id', 'username'), 'hhhhctf': ('flag',)}}
        self.columns_name = {}

        """
        当选择注入content时，你需要指定输入数据的上限，默认为10
        """
        self.content_count = 10

        """
        初始化dealpayload类，传入self.sqlimethod，self.payload, self.requestformat, self.filter
        """
        self.dealpayload = ConPayload(self.sqlirequest, self.payload, self.requesetformat, self.filter, self.time)
