#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlier.content import SqliContent
from lib.log import logger
from lib.log import log
import re

__author__ = "LoRexxar"


def main():
    s = SqliContent()

    # 处理下url，作为logname
    name = re.findall("[\w\.-]+", s.url)
    del name[0]
    try:
        url_name = "%2f".join(name)
    except IndexError:
        logger.error("url matching fail!")
        exit(0)
    log(s.loglevel, url_name)

    logger.info('start sqli...')
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
        if s.sqlilocation['content']:
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
