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
    # log(logging.INFO)
    log(logging.ERROR)
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
    elif s.wsqli:
        if s.sqlilocation['all']:
            s.run_content()
        elif s.sqlilocation['content']:
            s.run_content()
        elif s.sqlilocation['columns']:
            s.get_columns()
        elif s.sqlilocation['tables']:
            s.get_tables()
        elif s.sqlilocation['database']:
            s.get_database()
        else:
            logger.error("Sqlilocation error, Not choose any injection pattern")
            exit(0)
    else:
        logger.error("Did not select any mode")
        exit(0)

    # SqliTables.get_tables()
    # SqliColumns.get_columns()
    # SqliContent.get_flag()
    # print ExpandFunction.crack_code('593e')


if __name__ == '__main__':
    main()
