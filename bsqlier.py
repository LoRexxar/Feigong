#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlier.expand import ExpandFunction
from sqlier.data import DataProcess
from sqlier.columns import SqliColumns
from sqlier.content import SqliContent
from sqlier.tables import SqliTables
from sqlier.test import SqliTest
from sqlier.data import logger
from lib.log import log
import logging

__author__ = "LoRexxar"


def main():
    log(logging.INFO)
    logger.info('start sqli...')
    s = SqliContent()
    s.get_now_database()
    # SqliTables.get_tables()
    # SqliColums.get_columns()
    # SqliContent.get_flag()
    # print ExpandFunction.crack_code('593e')


if __name__ == '__main__':
    main()
