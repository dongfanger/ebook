# 【pytest】pytest132个命令行参数用法
![](../wanggang.png)


在Shell执行`pytest -h`可以看到pytest的命令行参数有这10大类，共132个

| 序号<img width=5px/> | 类别 | 中文名       | 包含命令行参数数量<img width=10px/> |
| ---- | ---------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| 1    | positional arguments                           | 形参                                       | 1                                                            |
| 2    | general                                        | 通用                                       | 31                                                           |
| 3    | reporting                                      | 报告                                       | 18                                                           |
| 4    | collection                                     | 收集                                       | 15                                                           |
| 5    | test session debugging and configuration       | 测试session调试和配置                      | 11                                                           |
| 6    | pytest-warnings                                | pytest警告                                 | 1                                                            |
| 7    | logging                                        | 日志                                       | 11                                                           |
| 8    | reporting-allure                               | allure测试报告                             | 3                                                            |
| 9    | ini-options                                    | pytest.ini/tox.ini/setup.cfg<br />配置文件 | 37                                                           |
| 10   | environment variables                          | 环境变量                                   | 4                                                            |

### 1.positional arguments

file_or_dir

指定一个或多个文件/目录

```shell
pytest [file_or_dir] [file_or_dir] [...]
```

### 2.general

-k EXPRESSION

名字包含test\_method或test\_other的函数或类

```shell
-k "test_method or test_other"
```

名字不包含test\_method

```shell
-k "not test_method"
```

名字不包含test\_method不包含test\_other

```shell
-k 'not test_method and not test_other'
```

大小写敏感。

源码这里不是很明白，先放这，以后再补充解释吧

```python
@classmethod
def from_item(cls, item: "Item") -> "KeywordMatcher":
    mapped_names = set()

    # Add the names of the current item and any parent items.
    import pytest

    for node in item.listchain():
        if not isinstance(node, (pytest.Instance, pytest.Session)):
            mapped_names.add(node.name)

    # Add the names added as extra keywords to current or parent items.
    mapped_names.update(item.listextrakeywords())

    # Add the names attached to the current function through direct assignment.
    function_obj = getattr(item, "function", None)
    if function_obj:
        mapped_names.update(function_obj.__dict__)

    # Add the markers to the keywords as we no longer handle them correctly.
    mapped_names.update(mark.name for mark in item.iter_markers())

    return cls(mapped_names)
```

-m MARKEXPR

包含mark1，不包含mark2

```shell
-m 'mark1 and not mark2'
```

--markers 

显示markers

```shell
pytest --markers
```

-x, --exitfirst

第一个error或failed的test就退出，2个参数等价

```shell
pytest -x
```

```shell
pytest --exitfirst
```

--maxfail=num

2个errors或failures就退出

```shell
pytest --maxfail=2
```

--strict-config

解析配置文件中`pytest`部分时，遇到warning就抛出error

```shell
pytest --strict-config
```

-c file

从`my.ini`文件加载配置

```shell
pytest -c my.ini
```

--continue-on-collection-errors

收集test失败，仍然强制继续执行

```shell
pytest --continue-on-collection-errors
```

--rootdir=ROOTDIR

tests根目录，相对路径

```shell
pytest --rootdir="root_dir"
```

```shell
pytest --rootdir="./root_dir"
```

```shell
pytest --rootdir="root_dir/another_dir/"
```

绝对路径

```shell
pytest --rootdir="/home/user/root_dir"
```

带变量

```shell
pytest --rootdir="$HOME/root_dir"
```

--fixtures, --funcargs

显示fixtures，以下等价

```shell
pytest --fixtures
```

```shell
pytest --funcargs
```

显示以\_开头的fixture

```shell
pytest --fixtures -v
```

--fixtures-per-test

显示每个test用到的fixture

```shell
pytest --fixtures-per-test
```

--pdb

在errors或KeyboardInterrupt时，启用默认Python debugger

```shell
pytest --pdb
```

--pdbcls=modulename:classname

启用自定义Python debugger，由`IPython.terminal.debugger` module下的`TerminalPdb` class定义

```shell
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
```

--trace

run每个test时break，进入debugger交互

```shell
pytest --trace
```

--capture=method

文件描述符（默认）

```shell
pytest --capture=fd
```

stdout/stderr 内存

```shell
pytest --capture=sys
```

显示print

```shell
pytest --capture=no
```

tee-sys

```shell
pytest --capture=tee-sys
```

-s

等价于`--capture=no`

--runxfail

强制运行xfail标记的test

```shell
pytest --runxfail
```

--lf, --last-failed

重跑上次失败的tests，如果没有失败就重跑全部，以下等价

```sh
pytest -lf
```

```shell
pytest --last-failed
```

--ff, --failed-first

优先跑上次失败的test，tests的顺序会被打乱，以下等价

```shell
pytest -ff
```

```shell
pytest --failed-first
```

--nf, --new-first

优先跑新添加的tests，剩余的按文件mtime顺序，以下等价

```shell
pytest --nf
```

```shell
pytest --new-first
```

--cache-show=[CACHESHOW]

显示缓存，默认`*`

```shell
pytest --cache-show
```

显示缓存，带参数`cache\nodeids`

```shell
pytest --cache-show=cache\nodeids
```

--cache-clear

运行开始时清缓存

```shell
pytest --cache-clear
```

--lfnf={all,none}, --last-failed-no-failures={all,none}

没有last-failed缓存数据，或上次没有失败时，

跑全部tests

```shell
pytest --lfnf=all
```

```shell
pytest --last-failed-no-failures=all
```

不运行

```shell
pytest --lfnf=none
```

```shell
pytest --last-failed-no-failures=none
```

--sw, --stepwise

逐步运行，在失败时退出，下次运行时从失败的用例开始

```shell
pytest -sw
```

```shell
pytest --stepwise
```

--stepwise-skip

跳过第一个失败的test，如果再遇到失败就退出

```shell
pytest --stepwise-skip
```

--allure-severities=SEVERITIES_SET

指定allure severities运行

```shell
pytest --allure-severities=blocker, critical, normal, minor, trivial
```

--allure-epics=EPICS_SET

指定allure epics运行

```shell
pytest --allure-epics=my_epic
```

--allure-features=FEATURES_SET

指定allure features运行

```shell
pytest --allure-features=my_feature
```

--allure-stories=STORIES_SET

指定allure stories运行

```shell
pytest --allure-stories=my_story
```

--allure-link-pattern=LINK_TYPE:LINK_PATTERN

不知道怎么用，溜了溜了

```
pytest --allure-link-pattern=
```

### 3.reporting

--durations=N

显示2个最慢的setup/test的耗时

```shell
pytest --durations=2
```

显示所有耗时

```shell
pytest --durations=0
```

-v, --verbose

输出详细信息

```shell
pytest -v
```

```sh
pytest --verbose
```

-q, --quiet

输出简要信息

```sh
pytest -q
```

```shell
pytest --quiet
```

--verbosity=VERBOSE

设置信息显示等级为2

```shell
pytest --verbosity=2
```

-r chars

默认"fE"

显示failed的信息

```shell
pytest -r f
```

显示Error的信息

```shell
pytest -r E
```

显示skipped的信息

```shell
pytest -r s
```

显示xfailed的信息

```shell
pytest -r x
```

显示Xpassed的信息

```shell
pytest -r X
```

显示passed的信息

```shell
pytest -r p
```

显示Passed with output的信息

```shell
pytest -r P
```

显示all except passed的信息

```shell
pytest -r a
```

```shell
pytest -r A
```

显示warnings are enabled by default (--disable-warnings)的信息

```shell
pytest -r w
```

重置list

```shell
pytest -r N
```

-l, --showlocals

在tracebacks中显示局部变量，默认不显示

```shell
pytest -l
```

```shell
pytest --showlocals
```

--tb=style

traceback打印模式

```shell
pytest --tb=auto
```

```shell
pytest --tb=long
```

```shell
pytest --tb=short
```

```shell
pytest --tb=line
```

```shell
pytest --tb=native
```

```shell
pytest --tb=no
```

--show-capture

失败的tests如何显示，默认"all"

```shell
pytest --show-capture=no
```

```shell
pytest --show-capture=stdout
```

```shell
pytest --show-capture=stderr
```

```shell
pytest --show-capture=log
```

```shell
pytest --show-capture=all
```

--full-trace

不截取traceback，默认会截断

```shell
pytest --full-trace
```

--color=color

显示颜色

```shell
pytest --color=yes
```

不显示颜色

```shell
pytest --color=no
```

自动

```shell
pytest --color=auto
```

--pastebin=mode

没什么用

```shell
pytest --pastebin=mode
```

--junit-xml=path

创建junit-xml风格的测试报告

```shell
pytest --junit-xml=path
```

--junit-prefix=str

junit-xml输出中的classnames添加前缀hello

```shell
pytest --junit-prefix="hello"
```

--result-log=path

不建议使用

```shell
pytest --result-log=path
```

### 4.collection

--collect-only, --co

只收集，不执行。**可以用来统计写了多少条自动化用例**

```shell
pytest --collect-only
```

```shell
pytest --co
```

--pyargs

把所有参数解释为python包(package)

```shell
pytest --pyargs
```

--ignore=path

忽略不收集，可以多个(逗号隔开)

```shell
pytest --ignore=path1,path2,path3
```

--ignore-glob=path

path匹配，可以多个(逗号隔开)

```shell
pytest --ignore-glob="*_01.py"
```

--deselect=nodeid_prefix

通过node id prefix反选。可以多个(逗号隔开)

取消选择tests/foobar/test_foobar_01.py::test_a

```shell
--deselect="tests/foobar/test_foobar_01.py::test_a"
```

--confcutdir=dir

只加载相对于tests/foobar/目录的conftest.py文件

```shell
pytest --confcutdir="tests/foobar/"
```

--noconftest

不加载conftest.py文件

```shell
pytest --noconftest
```

--keep-duplicates

收集重复的test文件，默认只会收集1item，加参数后会收集2items

```shell
pytest test.py test.py --keep-duplicates
```

--collect-in-virtualenv

收集本地虚拟环境目录的tests

```shell
pytest --collect-in-virtualenv
```

--doctest-modules

doctest没啥用

```shell
pytest --doctest-modules
```

--doctest-report={none,cdiff,ndiff,udiff,only_first_failure}

doctest没啥用

```shell
pytest --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
```

--doctest-glob=pat

doctest没啥用

```shell
pytest --doctest-glob=pat
```

--doctest-ignore-import-errors

doctest没啥用

```shell
pytest --doctest-ignore-import-errors
```

--doctest-continue-on-failure

doctest没啥用

```shell
pytest --doctest-continue-on-failure
```

### 5.test session debugging and configuration

--basetemp=dir

test run的base临时目录（如果存在会先删除）

```shell
pytest --basetemp=dir
```

-V, --version

pytest版本

```shell
pytest -V
```

```shell
pytest --version
```

-h, --help

pytest帮助

```shell
pytest -h
```

```shell
pytest --help
```

-p name

加载plugin module或 entry point

```shell
pytest -p name
```

不加载doctest

```shell
pytest -p no:doctest
```

--trace-config

查看本地安装好的第三方插件

```shell
pytest --trace-config
```

--debug

保存debug信息到'pytestdebug.log'文件

```shell
pytest --debug
```

-o OVERRIDE_INI, --override-ini=OVERRIDE_INI

覆盖ini文件配置

```shell
pytest -o xfail_strict=True -o cache_dir=cache
```

```shell
pytest --override-ini=OVERRIDE_INI
```

--assert=MODE

默认rewrite

```shell
pytest --assert=rewrite
```

无assertion debugging

```shell
pytest --assert=plain
```

--setup-only

只setup fixtures，不执行tests

```shell
pytest --setup-only
```

--setup-show

执行tests的时候显示fixture setup

```shell
pytest --setup-show
```

--setup-plan

显示fixtures和tests计划会执行什么，但是不执行

也可以用来统计自动化用例

```shell
pytest --setup-plan
```

### 6.pytest-warnings

-W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS

设置报告哪些warnings

```shell
pytest -W PYTHONWARNINGS
```

```shell
pytest --pythonwarnings=PYTHONWARNINGS
```

### 7.logging

推荐直接使用**loguru**第三方库。

--log-level=LEVEL

默认没有设置，依赖log handler

WARNING DEBUG INFO ERROR

```shell
pytest --log-level=LEVEL
```

--log-format=LOG_FORMAT

日志格式

```shell
pytest --log-format="%(asctime)s %(levelname)s %(message)s"
```

--log-date-format=LOG_DATE_FORMAT

日期格式

```shell
pytest --log-date-format="%Y-%m-%d %H:%M:%S"
```

--log-cli-level=LOG_CLI_LEVEL

cli日志级别

```shell
pytest --log-cli-level=LOG_CLI_LEVEL
```

--log-cli-format=LOG_CLI_FORMAT

cli日志格式

```shell
pytest --log-cli-format="%(asctime)s %(levelname)s %(message)s"
```

--log-cli-date-format=LOG_CLI_DATE_FORMAT

cli日志级别

```shell
pytest --log-cli-date-format="%Y-%m-%d %H:%M:%S"
```

--log-file=LOG_FILE

日志文件路径

```shell
pytest --log-file=LOG_FILE
```

--log-file-level=LOG_FILE_LEVEL

日志文件级别

```shell
pytest --log-file-level=LOG_FILE_LEVEL
```

--log-file-format=LOG_FILE_FORMAT

日志文件格式

```shell
pytest --log-file-format="%(asctime)s %(levelname)s %(message)s"
```

--log-file-date-format=LOG_FILE_DATE_FORMAT

日志文件日期

```shell
pytest --log-file-date-format="%Y-%m-%d %H:%M:%S"
```

--log-auto-indent=LOG_AUTO_INDENT

自动换行

true|flase  on|off

```shell
pytest --log-auto-indent=LOG_AUTO_INDENT
```

### 8.reporting-allure

--alluredir=DIR

allure数据生成目录，注意不是html哦，而是json文件，需要`allure generate data_dir -o html_dir`才能生成html

```shell
pytest --alluredir=DIR
```

--clean-alluredir

如果存在alluredir，先清除

```shell
pytest --clean-alluredir
```

--allure-no-capture

报告不捕获pytest的logging/stdout/stderr信息

```shell
pytest --allure-no-capture
```

### 9.ini-options

ini文件用例设置一些初始化默认值。

部分内容其实质跟参数是一样用法。

markers (linelist)

自定义marker

```ini
## pytest.ini
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case
```

empty_parameter_set_mark (string)

默认情况下，如果`@pytest.mark.parametrize`的`argnames`中的参数没有接收到任何的实参的话，用例的结果将会被置为`SKIPPED`；empty_parameter_set_mark可以设置为skip、xfail、fail_at_collect。

norecursedirs (args)

忽略一些目录

```ini
## pytest.ini
 
[pytest]
 
norecursedirs = .* build dist CVS _darcs {arch} *.egg venv src
```

testpaths (args)

指定目录

```ini
## pytest.ini
 
[pytest]
 
testpaths = test_path
```

usefixtures (args)

默认使用fixtures。

python_files (args)

glob文件匹配模式的python test modules。

python_classes (args)

前缀/glob文件匹配模式的python test classes。

python_functions (args)

前缀/glob文件匹配模式的python test functions。

ty_support (bool)

有风险，没用。

console_output_style (string)

控制台输出样式

- classic 经典样式
- progress: 带进度百分比
- count 计数而不是百分比

xfail_strict (bool)

默认false，true时@pytest.mark.xfail的test，会被强制失败，即使是成功的。

enable_assertion_pass_hook (bool)

确保删除之前生成的pyc缓存文件。

junit_suite_name (string)

不用学。

junit_logging (string)

不用学。

junit_log_passing_tests (bool)

不用学。

junit_duration_report (string)

不用学。

junit_family (string)

不用学。

doctest_optionflags (args)

不用学。

doctest_encoding (string)

不用学。

cache_dir (string)

缓存目录。

filterwarnings (linelist)

同 -W/--pythonwarnings。

log_level (string)

同命令行参数。

log_format (string)

同命令行参数。

log_date_format (string)

同命令行参数。

log_cli (bool)

true，test run的时候，实时显示日志。

log_cli_level (string)

同命令行参数。

log_cli_format (string)

同命令行参数。

log_cli_date_format (string)

同命令行参数。

log_file (string)

同命令行参数。

log_file_level (string)

同命令行参数。

log_file_format (string)

同命令行参数。

log_file_date_format (string)

同命令行参数。

log_auto_indent (string)

同命令行参数。

faulthandler_timeout (string)

如果test的运行时间超过设定的时间（超时），会打印相关traceback。

addopts (args)

执行时带的默认参数，可以避免每次都要输入一遍

```ini
addopts = -rsxX -v --reruns=1 --count=2
```

minversion (string)

pytest最小版本号。如果pytest低于这个版本，运行会报错。

required_plugins (args)

必须的插件。

### 10.environment variables

PYTEST_ADDOPTS

命令行选项

```
export PYTEST_ADDOPTS=
```

PYTEST_PLUGINS

包含应作为插件加载的以逗号分隔的模块列表

```
export PYTEST_PLUGINS=mymodule.plugin,xdist
```

PYTEST_DISABLE_PLUGIN_AUTOLOAD

禁用插件自动加载

```
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=
```

PYTEST_DEBUG

启用pytest调试

```
export PYTEST_DEBUG=
```
