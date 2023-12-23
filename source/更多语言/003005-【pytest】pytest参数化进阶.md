# 【pytest】pytest参数化进阶
![](../wanggang.png)


用过unittest的朋友，肯定知道可以借助DDT实现参数化。用过JMeter的朋友，肯定知道JMeter自带了4种参数化方式（见参考资料）。pytest同样支持参数化，而且很简单很实用。

### 语法

在《pytest封神之路第三步 精通fixture》和《pytest封神之路第四步 内置和自定义marker》两篇文章中，都提到了pytest参数化。那么本文就趁着热乎，赶紧聊一聊pytest的参数化是怎么玩的。

**@pytest.mark.parametrize** 

```python
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

- 可以自定义变量，test_input对应的值是"3+5" "2+4" "6\*9"，expected对应的值是8 6 42，**多个变量用tuple，多个tuple用list**

- 参数化的变量是引用而非复制，意味着如果值是list或dict，改变值会影响后续的test

- 重叠产生笛卡尔积

  ```python
  import pytest
  
  
  @pytest.mark.parametrize("x", [0, 1])
  @pytest.mark.parametrize("y", [2, 3])
  def test_foo(x, y):
      pass
  ```



**@pytest.fixture()**  

```python
@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
```

- 只能使用request.param来引用

- 参数化生成的test带有ID，可以使用`-k`来筛选执行。默认是根据`函数名[参数名]`来的，可以使用ids来定义

  ```python
  // list
  @pytest.fixture(params=[0, 1], ids=["spam", "ham"])
  // function
  @pytest.fixture(params=[0, 1], ids=idfn)
  ```

  使用`--collect-only  `命令行参数可以看到生成的IDs。



**参数添加marker**

我们知道了参数化后会生成多个tests，如果有些test需要marker，可以用pytest.param来添加

marker方式

```python
## content of test_expectation.py
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

fixture方式

```python
## content of test_fixture_marks.py
import pytest


@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
    return request.param
def test_data(data_set):
    pass
```



**pytest_generate_tests**

用来自定义参数化方案。使用到了hook，hook的知识我会写在《pytest hook》中，欢迎关注公众号dongfanger获取最新文章。

```python
## content of conf.py


def pytest_generate_tests(metafunc):
    if "test_input" in metafunc.fixturenames:
        metafunc.parametrize("test_input", [0, 1])
```

```python
## content of test.py


def test(test_input):
    assert test_input == 0
```

- 定义在conftest.py文件中
- metafunc有5个属性，fixturenames，module，config，function，cls
- metafunc.parametrize() 用来实现参数化
- 多个metafunc.parametrize() 的参数名不能重复，否则会报错



### 参数化误区

在讲示例之前，先简单分享我的菜鸡行为。假设我们现在需要对50个接口测试，验证某一角色的用户访问这些接口会返回403。我的做法是，把接口请求全部参数化了，test函数里面只有断言，**伪代码**大致如下

```python
def api():
    params = []
    def func():
        return request()
    params.append(func)
    ...


@pytest.mark.parametrize('req', api())
def test():
    res = req()
    assert res.status_code == 403
```

这样参数化以后，会产生**50个tests**，如果断言失败了，会单独标记为failed，不影响其他test结果。咋一看还行，但是有个问题，在回归的时候，可能只需要验证其中部分接口，就没有办法灵活的调整，必须全部跑一遍才行。这是一个**相对错误的示范**，至于正确的应该怎么写，相信每个人心中都有一个答案，能解决问题就是ok的。我想表达的是，**参数化要适当，不要滥用，最好只对测试数据做参数化**。

### 实践

本文的**重点**来了，参数化的语法比较简单，实际应用是关键。这部分通过11个例子，来实践一下。**示例覆盖的知识点有点多，建议留大段时间细看。**

1.使用hook添加命令行参数--all，"param1"是参数名，带--all参数时是range(5) == [0, 1, 2, 3, 4]，生成5个tests。不带参数时是range(2)。

```python
## content of test_compute.py


def test_compute(param1):
    assert param1 < 4

```

```python
## content of conftest.py


def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")
def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = 5
        else:
            end = 2
        metafunc.parametrize("param1", range(end))

```

2.testdata是测试数据，包括2组。test_timedistance_v0不带ids。test_timedistance_v1带list格式的ids。test_timedistance_v2的ids为函数。test_timedistance_v3使用pytest.param同时定义测试数据和id。

```python
## content of test_time.py
from datetime import datetime, timedelta

import pytest

testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]


@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_v1(a, b, expected):
    diff = a - b
    assert diff == expected


def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime("%Y%m%d")


@pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
def test_timedistance_v2(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(
            datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1), id="forward"
        ),
        pytest.param(
            datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1), id="backward"
        ),
    ],
)
def test_timedistance_v3(a, b, expected):
    diff = a - b
    assert diff == expected

```

3.兼容unittest的testscenarios

```python
## content of test_scenarios.py
def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


scenario1 = ("basic", {"attribute": "value"})
scenario2 = ("advanced", {"attribute": "value2"})


class TestSampleWithScenarios:
    scenarios = [scenario1, scenario2]

    def test_demo1(self, attribute):
        assert isinstance(attribute, str)

    def test_demo2(self, attribute):
        assert isinstance(attribute, str)

```

4.初始化数据库连接

```python
## content of test_backends.py
import pytest


def test_db_initialized(db):
    # a dummy test
    if db.__class__.__name__ == "DB2":
        pytest.fail("deliberately failing for demo purposes")

```

```python
## content of conftest.py
import pytest


def pytest_generate_tests(metafunc):
    if "db" in metafunc.fixturenames:
        metafunc.parametrize("db", ["d1", "d2"], indirect=True)


class DB1:
    "one database object"


class DB2:
    "alternative database object"


@pytest.fixture
def db(request):
    if request.param == "d1":
        return DB1()
    elif request.param == "d2":
        return DB2()
    else:
        raise ValueError("invalid internal test config")

```

5.如果不加indirect=True，会生成2个test，fixt的值分别是"a"和"b"。如果加了indirect=True，会先执行fixture，fixt的值分别是"aaa"和"bbb"。indirect=True结合fixture可以在生成test前，对参数变量额外处理。

```python
import pytest


@pytest.fixture
def fixt(request):
    return request.param * 3


@pytest.mark.parametrize("fixt", ["a", "b"], indirect=True)
def test_indirect(fixt):
    assert len(fixt) == 3

```

6.多个参数时，indirect赋值list可以指定某些变量应用fixture，没有指定的保持原值。

```python
## content of test_indirect_list.py
import pytest


@pytest.fixture(scope="function")
def x(request):
    return request.param * 3


@pytest.fixture(scope="function")
def y(request):
    return request.param * 2


@pytest.mark.parametrize("x, y", [("a", "b")], indirect=["x"])
def test_indirect(x, y):
    assert x == "aaa"
    assert y == "b"

```

7.兼容unittest参数化

```python
## content of ./test_parametrize.py
import pytest


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


class TestClass:
    # a map specifying multiple argument sets for a test method
    params = {
        "test_equals": [dict(a=1, b=2), dict(a=3, b=3)],
        "test_zerodivision": [dict(a=1, b=0)],
    }

    def test_equals(self, a, b):
        assert a == b

    def test_zerodivision(self, a, b):
        with pytest.raises(ZeroDivisionError):
            a / b

```

8.在不同python解释器之间测试对象序列化。python1把对象pickle-dump到文件。python2从文件中pickle-load对象。

```python
"""
module containing a parametrized tests testing cross-python
serialization via the pickle module.
"""
import shutil
import subprocess
import textwrap

import pytest

pythonlist = ["python3.5", "python3.6", "python3.7"]


@pytest.fixture(params=pythonlist)
def python1(request, tmpdir):
    picklefile = tmpdir.join("data.pickle")
    return Python(request.param, picklefile)


@pytest.fixture(params=pythonlist)
def python2(request, python1):
    return Python(request.param, python1.picklefile)


class Python:
    def __init__(self, version, picklefile):
        self.pythonpath = shutil.which(version)
        if not self.pythonpath:
            pytest.skip("{!r} not found".format(version))
        self.picklefile = picklefile

    def dumps(self, obj):
        dumpfile = self.picklefile.dirpath("dump.py")
        dumpfile.write(
            textwrap.dedent(
                r"""
                import pickle
                f = open({!r}, 'wb')
                s = pickle.dump({!r}, f, protocol=2)
                f.close()
                """.format(
                    str(self.picklefile), obj
                )
            )
        )
        subprocess.check_call((self.pythonpath, str(dumpfile)))

    def load_and_is_true(self, expression):
        loadfile = self.picklefile.dirpath("load.py")
        loadfile.write(
            textwrap.dedent(
                r"""
                import pickle
                f = open({!r}, 'rb')
                obj = pickle.load(f)
                f.close()
                res = eval({!r})
                if not res:
                raise SystemExit(1)
                """.format(
                    str(self.picklefile), expression
                )
            )
        )
        print(loadfile)
        subprocess.check_call((self.pythonpath, str(loadfile)))


@pytest.mark.parametrize("obj", [42, {}, {1: 3}])
def test_basic_objects(python1, python2, obj):
    python1.dumps(obj)
    python2.load_and_is_true("obj == {}".format(obj))

```

9.假设有个API，basemod是原始版本，optmod是优化版本，验证二者结果一致。

```python
## content of conftest.py
import pytest


@pytest.fixture(scope="session")
def basemod(request):
    return pytest.importorskip("base")


@pytest.fixture(scope="session", params=["opt1", "opt2"])
def optmod(request):
    return pytest.importorskip(request.param)

```

```python
## content of base.py


def func1():
    return 1
```

```python
## content of opt1.py


def func1():
    return 1.0001
```

```python
## content of test_module.py
def test_func1(basemod, optmod):
    assert round(basemod.func1(), 3) == round(optmod.func1(), 3)
```

10.使用pytest.param添加marker和id。

```python
## content of test_pytest_param_example.py
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("3+5", 8),
        pytest.param("1+7", 8, marks=pytest.mark.basic),
        pytest.param("2+4", 6, marks=pytest.mark.basic, id="basic_2+4"),
        pytest.param(
            "6*9", 42, marks=[pytest.mark.basic, pytest.mark.xfail], id="basic_6*9"
        ),
    ],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected

```

11.使用pytest.raises让部分test抛出Error。

```python
from contextlib import contextmanager

import pytest


// 3.7+ from contextlib import nullcontext as does_not_raise
@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "example_input,expectation",
    [
        (3, does_not_raise()),
        (2, does_not_raise()),
        (1, does_not_raise()),
        (0, pytest.raises(ZeroDivisionError)),
    ],
)
def test_division(example_input, expectation):
    """Test how much I know division."""
    with expectation:
        assert (6 / example_input) is not None

```

### 简要回顾

本文先讲了参数化的语法，包括marker，fixture，hook方式，以及如何给参数添加marker，然后重点列举了几个实战示例。参数化用好了能节省编码，达到事半功倍的效果。

> *参考资料*
>
> docs-pytest-org-en-stable
>



