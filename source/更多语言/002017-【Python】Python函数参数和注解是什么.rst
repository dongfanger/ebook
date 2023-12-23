【Python】Python函数参数和注解是什么
====================================

|image1|

四种参数
--------

Python函数func定义如下：

.. code:: python

   def func(first, *args, second="Hello World", **kwargs):
       print(first)
       print(args)
       print(second)
       print(kwargs)


   func("dongfanger", "san", py="good")

运行后会输出：

.. code:: python

   dongfanger
   ('san',)
   Hello World
   {'py': 'good'}

它有四种参数：

-  first是定位参数，positional parameter，不可省略。
-  ``*args``\ 是可变参数，arguments，存入元组。
-  second是默认值参数，default argument values，可以省略。
-  ``**args``\ 是关键字参数，keyword arguments，存入字典。

func函数的调用方式有以下这些：

①传入单个定位参数。

.. code:: python

   func("dongfanger")  

::

   dongfanger
   ()
   Hello World
   {}

②第一个参数后的任意个参数会被\ ``*args``\ 捕获，存入一个元组。

.. code:: python

   func("dongfanger", "a", "b", "c")

::

   dongfanger
   ('a', 'b', 'c')
   Hello World
   {}

③没有明确指定名称的关键字参数会被\ ``**kwargs``\ 捕获，存入一个字典。

.. code:: python

   func("dongfanger", j="1", k="2")

::

   dongfanger
   ()
   Hello World
   {'j': '1', 'k': '2'}

④second只能作为关键字参数传入。

.. code:: python

   func("dongfanger", second="cool")

::

   dongfanger
   ()
   cool
   {}

⑤定位函数也能作为关键字参数传入。

.. code:: python

   func(first="san")

::

   san
   ()
   Hello World
   {}

⑥字典前加上\ ``**``\ ，其所有元素作为单个参数传入，同名键会绑定到对应具名参数上，余下的被\ ``**args``\ 捕获。

.. code:: python

   my_dict = {"first": "dongfanger", "location": "cd", "second": "cool", "age": "secret"}
   func(**my_dict)

::

   dongfanger
   ()
   cool
   {'location': 'cd', 'age': 'secret'}

除了这四种参数，还有一种Python3新增加的仅限关键字参数。

仅限关键字参数
--------------

仅限关键字参数（keyword-only
argument）是Python3的新特性，func函数的second参数就是仅限关键字参数，“仅限”的意思是说，只能通过关键字参数指定，它一定不会捕获未命名的定位参数。

假如把参数位置调整一下定义another_func函数：

.. code:: python

   def another_func(first, another_second="Hello World", *args,  **kwargs):
       print(first)
       print(another_second)
       print(args)
       print(kwargs)


   another_func("dongfanger", "a", "b", "c")

输出会变成：

::

   dongfanger
   a  # 注意这里
   ('b', 'c')
   {}

another_second不是仅限关键字参数，而只是默认值参数，因为它捕获到了定位参数。

由此得知，定义仅限关键字参数，必须把它放到\ ``*args``\ 参数后面，就像func函数一样，反例是another_func函数。

还有第二个方法定义仅限关键字参数，在签名中放一个\ ``*``\ ：

.. code:: python

   >>> def f(a, *, b):  # b是仅限关键字参数
   ...    return a, b
   ...
   >>> f(1, b=2)  # 只能传关键字参数
   (1, 2)
   >>> f(1, 2)  # 不能传定位参数
   Traceback (most recent call last):
     File "<input>", line 1, in <module>
   TypeError: f() takes 1 positional argument but 2 were given
   >>> f(1, 2, 3)  # 不能传定位参数
   Traceback (most recent call last):
     File "<input>", line 1, in <module>
   TypeError: f() takes 1 positional argument but 3 were given

..

   仅限关键字参数不一定要有默认值，就像b一样，强制必须传入实参。

内省中的函数参数
----------------

函数内省的意思是说，当你拿到一个“函数对象”的时候，你可以继续知道，它的名字，参数定义等信息。这些信息可以通过函数对象的属性（一些双下划线的魔法方法）得到。

对于func函数：

.. code:: python

   def func(first, *args, second="Hello World", **kwargs):
       print(first)
       print(second)
       print(args)
       print(kwargs)

和another_func函数：

.. code:: python

   def another_func(first, another_second="Hello World", *args,  **kwargs):
       print(first)
       print(another_second)
       print(args)
       print(kwargs)

**``__defaults__``\ 属性**

元组，保存着定位参数和关键字参数的默认值。

.. code:: python

   print(func.__defaults__)  # None

   print(another_func.__defaults__)  # ('Hello World',)

**``__kwdefaults__``\ 属性**

字典，保存仅限关键字参数。

.. code:: python

   print(func.__kwdefaults__)  # {'second': 'Hello World'}

   print(another_func.__kwdefaults__)  # None

**``__code__``\ 属性**

code对象引用，code对象自身有很多属性，其中包括参数名称。

.. code:: python

   print(func.__code__.co_varnames)  # ('first', 'second', 'args', 'kwargs')

   print(another_func.__code__.co_varnames)  # ('first', 'another_second', 'args', 'kwargs')

另外还可以使用inspect库的signature方法来查看内省中的函数参数：

.. code:: python

   from inspect import signature

   print(signature(func))  
   ## (first, *args, second='Hello World', **kwargs)

框架和IDE等工具可以使用这些信息验证代码。

函数注解
--------

如果刷过力扣算法题，那么对函数注解就不会陌生。比如：

.. code:: python

   def clip(text:str, max_len:'int > 0'=80) -> str:
       pass

参数\ ``:``\ 后面是注解表达式，可以用来注解参数类型和约束。如果参数有默认值，注解放在参数名和=号之间。

可以在函数末尾的\ ``)``\ 和\ ``:``\ 之间添加\ ``->``\ 和注解表达式，来对返回值添加注解。

注解表达式可以是任何类型，最常用的类型是类（如str或int）和字符串（如\ ``'int > 0'``\ ）。

函数注解只是个注解，Python对注解所做的唯一的事情是，把它们存入函数的\ ``__annotations__``\ 属性中：

.. code:: python

   print(clip.__annotations__)
   #{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}

Python不做检查，不做强制，不做验证，什么操作都不做！注解只是元数据，可以供框架和IDE等工具使用。

小结
----

本文介绍了Python函数的四种参数：定位参数、可变参数、默认值参数、关键字参数，和第五种Python3新特性参数：仅限关键字参数。拿到一个函数对象后，可以通过函数属性（一些双下划线的魔法方法）查看内省中的参数信息。函数注解是一种元数据，存在\ ``__annotations__``\ 属性中，备注函数的参数和返回值的类型，它只是个注解，Python不会做任何强制检查。

   参考资料：

   《流畅的Python》

   https://blog.csdn.net/cadi2011/article/details/86641811

   https://segmentfault.com/q/1010000012595419

.. |image1| image:: ../wanggang.png
