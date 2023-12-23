# 【Python】原来Python函数只是个对象
![](../wanggang.png)

写Python越多，写函数越多，于是乎有人觉得Python是函数式语言，其实不然，Python只是从函数式语言中借鉴了一些好的想法而已。

## 函数是对象

Python中万物皆对象，函数也不例外，这意味着函数有以下特点：

- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传给函数
- 能作为函数的返回结果

用代码把函数类型打出来看到本质：

```python
>>> def hello():
...     print("dongfanger")
...     
>>> type(hello)
<class 'function'>
```

hello函数是function类的实例。再看一个例子，把函数赋值：

```python
>>> def hello():
...     print("dongfanger")
...     
>>> a = hello
>>> a()
dongfanger
```

Python函数就是个普普通通的对象！

## 高阶函数

接受函数为参数或者把函数作为结果返回的函数，叫做高阶函数，比如map、filter、reduce，但是！作者并不建议使用这3个高阶函数，因为在Python3中有更好的替代品，而且更易于阅读。

### 列表推导替代map、filter

比如，1-10，计算对每个数字的平方：

```python
## 使用map
result = map(lambda x: x ** 2, range(1, 11))

## 使用列表推导
result = [x ** 2 for x in range(1, 11)]
```

过滤奇数：

```python
## 用filter
result = map(lambda x: x ** 2, filter(lambda x: x % 2, range(1, 11)))

## 使用列表推导
result = [x ** 2 for x in range(1, 11) if x % 2]
```

真香。

### sum替代reduce

计算0~99之和：

```python
## 使用reduce
>>> from functools import reduce
>>> from operator import add
>>> reduce(add, range(100))
4950

## 使用sum
>>> sum(range(100))
4950
```

> sum叫做归约函数，内置归约函数还有all(iterable)，如果每个元素都是真值返回True。any(iterable)，只要有元素是真值，就返回True。

## 匿名函数

在Python中使用lambda表达式来创建匿名函数，示例：

```python
fruits = ["strawberry", "fig", "apple", "cherry", "raspberry", "banana"]
sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

它只是个表达式，不能使用while和try等语句。除了作为参数传给高阶函数之外，Python很少使用匿名函数，它的可读性并不好，如果表达式不是特别简单，那么建议不要使用lambda表达式，比如：

```python
import re

s = "192.0.0.1?!289.0.0.1!0.0.0.0!192.163.10.20?192.0.0.1"
ips = re.split(r"\?!|!|\?", s)


def last_one(i):
    return i.split('.')[-1]


ips.sort(key=last_one)
print(ips)
```

通过def定义有名字的函数，可读性更佳。

## 可调用对象

Python函数是对象，是可调用对象，可以使用内置的callable()函数来判断对象能否调用，比如：

```python
>>> abs, str, 13
(<built-in function abs>, <class 'str'>, 13)
>>> [callable(obj) for obj in (abs, str, 13)]
[True, True, False]
```

Python共有7种可调用对象：

**用户自定义函数**

def语句或lambda表达式创建。

**内置函数**

C语言（CPython）实现的函数，如len或time.strftime。

**内置方法**

C语言（CPython）实现的方法，如dict.get。

**方法**

类的定义体中定义的函数。

**类**

类是可调用的，调用类时会调用类的`__new__`方法创建一个实例，然后调用`__init__`方法初始化实例，最后返回实例给调用方。

> Python没有new运算符，调用类相当于调用函数。

**类的实例**

如果类定义了`__call__`方法，那么它的实例可以作为函数调用。比如：

```python
class Test:
    def __init__(self):
        self.name = "dongfanger"

    def __call__(self, *args, **kwargs):
        return self.name


test = Test()
print(test())  # dongfanger
```

> 不定义`__call__`方法，运行test()会报错`TypeError: 'Test' object is not callable`。

**生成器函数**

yield关键字定义的函数或方法。

> 生成器函数的返回值是生成器对象。

## 函数内省

函数对象有很多属性：

```python
>>> def func():
...     pass
... 
>>> dir(func)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', 
'__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', 
'__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

Django源码修改函数属性示例：

```python
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
## 修改函数属性
upper_case_name.short_description = 'Customer name'
```

通过计算类实例和函数的差集，可以得出函数特有的属性：

```python
>>> class C: pass
... 
>>> obj = C()
>>> def func(): pass
... 
>>> sorted(set(dir(func)) - set(dir(obj)))
['__annotations__', '__call__', '__closure__', '__code__', 
'__defaults__', '__get__', '__globals__', '__kwdefaults__', 
'__name__', '__qualname__']
```

其中的`__defaults__`、`__code__`、`__annotations__`属性，IDE和框架使用它们提取关于函数签名的信息。

## 小结

本文通过示例看到了函数是对象的事实，高阶函数map、filter和reduce在现在已经被列表推导、生成器表达式、和sum、all、any等内置的归约函数替代。labmda表达式创建的匿名函数只在参数中且逻辑简单时使用。函数是可调用对象，实现了`__call__`的类也是可调用的，可以使用callable()函数来判断。最后列出了函数属性，它们记录了函数各个方面的信息。

> 参考资料：
>
> 《流畅的Python》