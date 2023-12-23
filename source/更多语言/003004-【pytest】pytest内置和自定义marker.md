# 【pytest】pytest内置和自定义marker
![](../wanggang.png)


可以通过命令行查看所有marker，包括内置和自定义的

```shell
pytest --markers
```

### 内置marker

内置marker本文先讲usefixtures  、filterwarnings   、skip  、skipif  、xfail这5个。参数化的marker我会写在《pytest参数化》中，hook的marker我会写在《pytest hook》中，插件的marker（pytest-ordering、allure等）我会写在《pytest插件》中。当前只需知道有以上这些分类的marker即可，更多内容请关注后续文章。

#### usefixtures 

如果我们只想把fixture注入到test中，test不直接访问fixture的时候，就需要用到usefixtures。

示例，test需要一个临时目录，但是并不需要知道这个目录具体路径在哪

```python
## content of conftest.py
import os
import shutil
import tempfile

import pytest


@pytest.fixture
def cleandir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)

```

```python
## content of test_setenv.py
import os

import pytest


@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

    with open("myfile", "w") as f:
        f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

```

TestDirectoryInit的测试方法需要一个临时目录作为当前工作目录，在类上添加`@pytest.mark.usefixtures("cleandir")`，类的方法不加fixture也能有"cleandir"的效果。

usefixtures可以添加多个fixture

```python
@pytest.mark.usefixtures("cleandir", "anotherfixture")
```

usefixtures可以用在**pytestmark**，作用域是定义所在module的所有tests

```python
pytestmark = pytest.mark.usefixtures("cleandir")
```

usefixtures也可以用在**pytest.ini**，作用域是整个项目的所有tests

```ini
## content of pytest.ini
[pytest]
usefixtures = cleandir
```

不过需要注意的是fixture函数本身是不能用usefixtures的，如果想要嵌套fixture，只能通过在fixture修饰的函数中，添加参数这种方式。

#### filterwarnings 

过滤警告信息。

示例，api_v1()抛出了“api v1”的警告，test_one()函数使用filterwarnings过滤掉了

```python
import warnings


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


@pytest.mark.filterwarnings("ignore:api v1")
def test_one():
    assert api_v1() == 1

```

同样可以添加到pytestmark和pytest.ini中。

#### skip 

跳过，不测试。

示例，skip需要添加reason哦

```python
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...
```

不过，更实用的方式是调用pytest.skip(reason)函数，而不是用mark，这样就可以用if判断跳不跳

```python
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

allow_module_level 可以跳过整个module

```python
import sys
import pytest

if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)
```

#### skipif 

if判断跳不跳，还可以用skipif。

示例，如果Python版本小于3.6就跳过测试

```python
import sys

@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_function():
    ...
```

如果想在summary中看到reason，需要添加-rs参数。

可以把skipif赋值给**变量**，然后直接引用变量，或者把变量import到其他module中使用

```python
## content of test_mymodule.py
import mymodule

minversion = pytest.mark.skipif(
    mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
)


@minversion
def test_function():
    ...

```

```python
## test_myothermodule.py
from test_mymodule import minversion

@minversion
def test_anotherfunction():
    ...

```

skipif添加到class上，会跳过类中所有方法。

可以使用pytestmark跳过module内所有test

```python
## test_module.py
pytestmark = pytest.mark.skipif(...)
```

如果function有多个skipif作用，只要有一个为True，就会跳过。

#### xfail

明知失败，依然前行！不好意思跑偏了。xfail就是expected fail，预期失败

```python
@pytest.mark.xfail
def test_function():
    ...
```

执行后summary不会统计为"failed"，会单独列出来。如果结果失败了，“expected to fail” (XFAIL)；如果结果成功了，“unexpectedly passing” (XPASS)。但是**整个执行结果是”Tests passed“。**

if判断

```python
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")
```

值得注意的是，marker会继续执行所有test代码，pytest.xfail()函数会抛出异常，中断执行后续代码

添加**condition**，判断条件

```python
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function():
    ...
```

添加**reason**，理由

```python
@pytest.mark.xfail(reason="known parser issue")
def test_function():
    ...
```

添加**raises**，抛出异常/错误

```python
@pytest.mark.xfail(raises=RuntimeError)
def test_function():
    ...
```

添加**run**，禁止运行

```python
@pytest.mark.xfail(run=False)
def test_function():
    ...
```

添加**strict**，严格模式，即使xpass也会强制失败，summary中有输出信息”[XPASS(strict)] “，测试结果为”Tests failed“。

```python
@pytest.mark.xfail(strict=True)
def test_function():
    ...
```

断言成功也强制失败，确实够强势的！

可以在ini文件中定义全局strict

```ini
[pytest]
xfail_strict=true
```

在命令行添加**--runxfail**，忽略xfail marker，相当于没有添加这个标记的效果，该成功就成功，该失败就失败，再强势也不虚，哈哈，恶灵退散。

```shell
pytest --runxfail
```

```python
pytest --runxfail
```

再强势也不虚，恶灵退散，哈哈。

### 自定义marker

通过注解自定义marker

```python
## content of test_server.py
import pytest


@pytest.mark.webtest
def test_send_http():
    pass  # perform some webtest test for your app


def test_something_quick():
    pass


def test_another():
    pass


class TestClass:
    def test_method(self):
        pass

```

在命令行通过`-m`指定运行mark打标的test

```shell
$ pytest -v -m webtest
```

也可以反选

```shell
$ pytest -v -m "not webtest"
```

但是，这样定义的marker是**未注册**的！在执行后会警告，PytestUnknownMarkWarning。如果添加了命令行参数`--strict-markers  `，未注册的marker会**报错**。

可以在pytest.ini文件中注册，冒号后面的所有代码都是marker说明，包括换行

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    serial
```

更高级的，可以在pytest_configure hook函数中注册，这主要用在第三方插件

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )
```

### 简要回顾

本文介绍了5个pytest内置的marker，接着介绍了如何自定义marker和注册marker。通过marker，可以让我们更灵活的执行用例。

> *参考资料*
>
> docs-pytest-org-en-stable

