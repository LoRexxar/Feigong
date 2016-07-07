#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlier.config import conf
from sqlier.expand import ExpandFunction
from sqlier.data import DataProcess
from sqlier.columns import SqliColums
from sqlier.content import SqliContent
from sqlier.tables import SqliTables
from sqlier.test import SqliTest
from sqlier.data import logger

__author__ = "LoRexxar"


def main():
    logger.info('start sqli...')
    SqliTest.test()
    SqliTables.get_tables()
    SqliColums.get_columns()
    SqliContent.get_flag()
    print ExpandFunction.crack_code('593e')


if __name__ == '__main__':
    main()
