#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.log import logger
from random import Random

__author__ = "LoRexxar"


"""
若注入方式为normal，则会用到解包函数
"""


def UnpackFunction(r, padding):

    index = r.find(padding)
    index2 = r[index+4:].find(padding)

    r = r[index+4:index2+index+4]
    return r


def random_string(randomlength=4):
    strs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        strs += chars[random.randint(0, length)]
    return strs
