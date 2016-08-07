# Feigong --非攻
## 非攻
取自《秦时明月》--非攻，针对不同情况自由变化的武器

Feigong，针对各种情况自由变化的mysql注入脚本

Feigong，In view of the different things freely change the mysql injection script

## 什么是非攻？ ##

在sqlmap的使用过程中，常常碰到很普通的绕过过滤方式，例如空格-->%0b、%0a，但是却没办法使用sqlmap来获取数据的情况，于是花了很长时间来完善脚本，让非攻可以通过修改config.py一个文件中的设置，让非攻在面对不同情况时成为了灵活多变的注入脚本...

非攻目前集成了对mysql的normal、build、time，3种注入方式...

### 在使用非攻之前 ###

1、首先你需要找到一个注入点（再考虑写一个这样的工具）
2、判断数据库为mysql
3、通过巧妙地过滤可以获取数据
4、开始使用非攻

## TODO ##

* <del>完成基本功能</del>
* 优化log存储方式
* 优化build注入、time注入算法
* 添加线程池优化注入速度
* 增加更多注入语句
* 增加更多绕过过滤方式
* 增加多种数据库


## 更新日志 ##
* 2016-8-5
	* Feigong 0.9.9完成
	* 增加 payload处理模块完成


## 使用文档 ##

Feigong
│  .gitignore
│  feigong.py
│  README.md
│
├─demo
│      demo1.py
│      demo2.py
│
├─lib
│      dealpayload.py
│      log.py
│      ltqdm.py
│      __init__.py
│
├─log
└─sqlier
        columns.py
        config.py
        config_default.py
        content.py
        data.py
        database.py
        expand.py
        tables.py
        test.py
        __init__.py


Feigong一切一切的核心在于sqlier/config.py
