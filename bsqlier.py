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
    if s.wtest:
        if s.testmethod['test']:
            s.test(output=1)
        if s.testmethod['database']:
            s.get_now_database()
        if s.testmethod['version']:
            s.get_version()
        if s.testmethod['user']:
            s.get_user()
    else:
        pass

    # SqliTables.get_tables()
    # SqliColumns.get_columns()
    # SqliContent.get_flag()
    # print ExpandFunction.crack_code('593e')


if __name__ == '__main__':
    main()
