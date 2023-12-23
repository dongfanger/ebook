【Python】Python如何设计面向对象的类（上）
==========================================

|image1|

Python是一门高级语言，支持面向对象设计，如何设计一个符合Python风格的面向对象的类，是一个比较复杂的问题，本文提供一个参考，表达一种思路，探究一层原理。

目标
----

期望实现的类具有以下基本行为：

-  ``__repr__``
   为repr()提供支持，返回便于\ **开发者**\ 理解的对象字符串表示形式。
-  ``__str__``
   为str()提供支持，返回便于\ **用户**\ 理解的对象字符串表示形式。
-  ``__bytes__`` 为bytes()提供支持，返回对象的二进制表示形式。
-  ``__format__``
   为format()和str.format()提供支持，使用特殊的格式代码显示对象的字符串表示形式。

Vector2d是一个向量类，期望它能支持以下操作：

.. code:: python

   >>> v1 = Vector2d(3, 4)
   >>> print(v1.x, v1.y)  # 通过属性直接访问
   3.0 4.0
   >>> x, y = v1  # 支持拆包
   >>> x, y
   (3.0, 4.0)
   >>> v1  # 支持repr
   Vector2d(3.0, 4.0)
   >>> v1_clone = eval(repr(v1))  # 验证repr描述准确
   >>> v1 == v1_clone  # 支持==运算符
   True
   >>> print(v1)  # 支持str
   (3.0, 4.0)
   >>> octets = bytes(v1)  # 支持bytes
   >>> octets
   b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
   >>> abs(v1)  # 实现__abs__
   5.0
   >>> bool(v1), bool(Vector2d(0, 0))  # 实现__bool__
   (True, False)

基本实现
--------

代码与解析如下：

.. code:: python

   from array import array
   import math


   class Vector2d:
       # Vector2d实例和二进制之间转换时使用
       typecode = 'd'  

       def __init__(self, x, y):
           # 转换为浮点数
           self.x = float(x)    
           self.y = float(y)

       def __iter__(self):
           # 生成器表达式，把Vector2d实例变成可迭代对象，这样才能拆包
           return (i for i in (self.x, self.y))  

       def __repr__(self):
           class_name = type(self).__name__
           # {!r}是个万能的格式符
           # *self是拆包，*表示所有元素
           return '{}({!r}, {!r})'.format(class_name, *self)

       def __str__(self):
           # Vector2d实例是可迭代对象，可以得到一个元组，并str
           return str(tuple(self))

       def __bytes__(self):
           # 转换为二进制
           return (bytes([ord(self.typecode)]) +  
                   bytes(array(self.typecode, self)))  

       def __eq__(self, other):
           # 比较相等
           return tuple(self) == tuple(other)  

       def __abs__(self):
           # 向量的模是直角三角形的斜边长
           return math.hypot(self.x, self.y) 

       def __bool__(self):
           # 0.0是False，非零值是True
           return bool(abs(self))  
       
       @classmethod
       def frombytes(cls, octets):  # classmethod不传self传cls
           typecode = chr(octets[0])
           memv = memoryview(octets[1:]).cast(typecode)
           return cls(*memv)  # 拆包后得到构造方法所需的一对参数

代码最后用到了@classmethod装饰器，它容易跟@staticmethod混淆。

**@classmethod**\ 的用法是：定义操作类，而不是操作实例的方法。常用来定义备选构造方法。

**@staticmethod**\ 其实就是个普通函数，只不过刚好放在了类的定义体里。实际定义在类中或模块中都可以。

格式化显示
----------

代码与解析如下：

.. code:: python

   def angle(self):
       return math.atan2(self.y, self.x)


   def __format__(self, fmt_spec=''):
       if fmt_spec.endswith('p'):  # 以'p'结尾，使用极坐标
           fmt_spec = fmt_spec[:-1]
           coords = (abs(self), self.angle())  # 计算极坐标(magnitude, angle)
           outer_fmt = '<{}, {}>'  # 尖括号
       else:
           coords = self  # 不以'p'结尾，构建直角坐标(x, y)
           outer_fmt = '({}, {})'  # 圆括号
       components = (format(c, fmt_spec) for c in coords)  # 使用内置format函数格式化字符串
       return outer_fmt.format(*components)  # 拆包后代入外层格式

它实现了以下效果：

直角坐标：

.. code:: python

   >>> format(v1)
   '(3.0, 4.0)'
   >>> format(v1, '.2f')
   '(3.00, 4.00)'
   >>> format(v1, '.3e')
   '(3.000e+00, 4.000e+00)'

极坐标：

.. code:: python

   >>> format(Vector2d(1, 1), 'p')  # doctest:+ELLIPSIS
   '<1.414213..., 0.785398...>'
   >>> format(Vector2d(1, 1), '.3ep')
   '<1.414e+00, 7.854e-01>'
   >>> format(Vector2d(1, 1), '0.5fp')
   '<1.41421, 0.78540>'

可散列的
--------

实现\ ``__hash__``\ 特殊方法能让Vector2d变成可散列的，不过在这之前需要先让属性不可变，代码如下：

.. code:: python

   def __init__(self, x, y):
       # 双下划线前缀，变成私有的
       self.__x = float(x)
       self.__y = float(y)

   @property  # 标记为特性
   def x(self):
       return self.__x

   @property
   def y(self):
       return self.__y

这样x和y就只读不可写了。

   属性名字的双下划线前缀叫做名称改写（name
   mangling），相当于\ ``_Vector2d__x``\ 和\ ``_Vector2d__y``\ ，能避免被子类覆盖。

然后使用位运算符异或混合x和y的散列值：

.. code:: python

   def __hash__(self):
       return hash(self.x) ^ hash(self.y)

节省内存
--------

Python默认会把实例属性存储在\ ``__dict__``\ 字典里，字典的底层是散列表，数据量大了以后会消耗大量内存（以空间换时间）。通过\ ``__slots__``\ 类属性，能把实例属性存储到元组里，大大节省内存空间。

示例：

.. code:: python

   class Vector2d:
       __slots__ = ('__x', '__y')

       typecode = 'd'

有几点需要注意：

-  必须把所有属性都定义到\ ``__slots__``\ 元组中。
-  子类也必须定义\ ``__slots__``\ 。
-  实例如果要支持弱引用，需要把\ ``__weakref``\ 也加入\ ``__slots__``\ 。

覆盖类属性
----------

实例覆盖
~~~~~~~~

Python有个很独特的特性：类属性可用于为实例属性提供默认值。实例代码中的typecode就能直接被self.typecode拿到。但是，如果为不存在的实例属性赋值，会新建实例属性，类属性不会受到影响，self.typecode拿到的是实例属性的typecode。

示例：

.. code:: python

   >>> v1 = Vector2d(1, 2)
   >>> v1.typecode = 'f'
   >>> v1.typecode
   'f'
   >>> Vector2d.typecode
   'd'

子类覆盖
~~~~~~~~

类属性是公开的，所以可以直接通过\ ``Vector2d.typecode = 'f'``\ 进行修改。但是更符合Python风格的做法是定义子类：

.. code:: python

   class ShortVector2d(Vector2d):
       typecode = 'f'

Django基于类的视图大量使用了这个技术。

小结
----

本文先介绍了如何实现特殊方法来设计一个Python风格的类，然后分别实现了格式化显示与可散列对象，使用\ ``__slots__``\ 能为类节省内存，最后讨论了类属性覆盖技术，子类覆盖是Django基于类的视图大量用到的技术。

   参考资料：

   《流畅的Python》第9章 符合Python风格的对象

   https://www.jianshu.com/p/7fc0a177fd1f

.. |image1| image:: ../wanggang.png
