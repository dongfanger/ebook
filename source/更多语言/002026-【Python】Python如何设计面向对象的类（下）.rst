【Python】Python如何设计面向对象的类（下）
==========================================

|image1|

本文将在上篇文章二维向量Vector2d类的基础上，定义表示多维向量的Vector类。

第1版：兼容Vector2d类
---------------------

代码如下：

.. code:: python

   from array import array
   import reprlib
   import math


   class Vector:
       typecode = 'd'

       def __init__(self, components):
           self._components = array(self.typecode, components)  # 多维向量存数组中

       def __iter__(self):
           return iter(self._components)  # 构建迭代器

       def __repr__(self):
           components = reprlib.repr(self._components)  # 有限长度表示形式
           components = components[components.find('['):-1]
           return 'Vector({})'.format(components)

       def __str__(self):
           return str(tuple(self))

       def __bytes__(self):
           return (bytes([ord(self.typecode)]) +
                   bytes(self._components))

       def __eq__(self, other):
           return tuple(self) == tuple(other)

       def __abs__(self):
           return math.sqrt(sum(x * x for x in self))

       def __bool__(self):
           return bool(abs(self))

       @classmethod
       def frombytes(cls, octets):
           typecode = chr(octets[0])
           memv = memoryview(octets[1:]).cast(typecode)
           return cls(memv)  # 因为构造函数入参是数组，所以不用再使用*拆包了

其中的reprlib.repr()函数用于生成大型结构或递归结构的安全表达形式，比如：

.. code:: python

   >>> Vector([3.1, 4.2])
   Vector([3.1, 4.2])
   >>> Vector((3, 4, 5))
   Vector([3.0, 4.0, 5.0])
   >>> Vector(range(10))
   Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])

超过6个的元素用\ ``...``\ 来表示。

第2版：支持切片
---------------

**Python协议是非正式的接口，只在文档中定义，在代码中不定义。**\ 比如Python的序列协议只需要\ ``__len__``\ 和\ ``__getitem__``\ 两个方法，Python的迭代协议只需要\ ``__getitem__``\ 一个方法，它们不是正式的接口，只是Python程序员默认的约定。

切片是序列才有的操作，所以Vector类要实现序列协议，也就是\ ``__len__``\ 和\ ``__getitem__``\ 两个方法，代码如下：

.. code:: python

   def __len__(self):
       return len(self._components)

   def __getitem__(self, index):
       cls = type(self)  # 获取实例所属的类
       if isinstance(index, slice):  # 如果index是slice切片对象
           return cls(self._components[index])  # 调用构造方法，返回新的Vector实例
       elif isinstance(index, numbers.Integral):  # 如果index是整型
           return self._components[index]  # 直接返回元素
       else:
           msg = '{cls.__name__} indices must be integers'
           raise TypeError(msg.format(cls=cls))

测试一下：

.. code:: python

   >>> v7 = Vector(range(7))
   >>> v7[-1]  # <1>
   6.0
   >>> v7[1:4]  # <2>
   Vector([1.0, 2.0, 3.0])
   >>> v7[-1:]  # <3>
   Vector([6.0])
   >>> v7[1,2]  # <4>
   Traceback (most recent call last):
     ...
   TypeError: Vector indices must be integers

第3版：动态存取属性
-------------------

通过实现\ ``__getattr__``\ 和\ ``__setattr__``\ ，我们可以对Vector类动态存取属性。这样就能支持\ ``v.my_property = 1.1``\ 这样的赋值。

   如果使用\ ``__setitem__``\ 方法，那么只能支持\ ``v[0] = 1.1``\ 。

代码如下：

.. code:: python

   shortcut_names = 'xyzt'  # 4个分量属性名

   def __getattr__(self, name):
       cls = type(self)  # 获取实例所属的类
       if len(name) == 1:  # 只有一个字母
           pos = cls.shortcut_names.find(name)
           if 0 <= pos < len(self._components):  # 落在范围内
               return self._components[pos]
       msg = '{.__name__!r} object has no attribute {!r}'  # <5>
       raise AttributeError(msg.format(cls, name))


   def __setattr__(self, name, value):
       cls = type(self)
       if len(name) == 1:  
           if name in cls.shortcut_names:  # name是xyzt其中一个不能赋值
               error = 'readonly attribute {attr_name!r}'
           elif name.islower():  # 小写字母不能赋值，防止与xyzt混淆
               error = "can't set attributes 'a' to 'z' in {cls_name!r}"
           else:
               error = ''
           if error:
               msg = error.format(cls_name=cls.__name__, attr_name=name)
               raise AttributeError(msg)
       super().__setattr__(name, value)  # 其他name可以赋值

**值得说明的是，\ ``__getattr__``\ 的机制是**\ ：对my_obj.x表达式，Python会检查my_obj实例有没有名为x的属性，\ **如果有就直接返回，不调用\ ``__getattr__``\ 方法**\ ；如果没有，到\ ``my_obj.__class__``\ 中查找，如果还没有，才调用\ **``__getattr__``\ 方法**\ 。

正因如此，name是xyzt其中一个时才不能赋值，否则会出现下面的奇怪现象：

.. code:: python

   >>> v = Vector([range(5)])
   >>> v.x = 10
   >>> v.x
   10
   >>> v
   Vector([0.0, 1.0, 2.0, 3.0, 4.0])

对v.x进行了赋值，但实际未生效，因为赋值后Vector新增了一个x属性，值为10，对v.x表达式来说，直接就返回了这个值，不会走我们自定义的\ ``__getattr__``\ 方法，也就没办法拿到v[0]的值。

第4版：散列
-----------

通过实现\ ``__hash__``\ 方法，加上现有的\ ``__eq__``\ 方法，Vector实例就变成了可散列的对象。

代码如下：

.. code:: python

   import functools
   import operator


   def __eq__(self, other):
       return (len(self) == len(other) and
               all(a == b for a, b in zip(self, other)))

   def __hash__(self):
       hashes = (hash(x) for x in self)  # 创建一个生成器表达式
       return functools.reduce(operator.xor, hashes, 0)  # 计算聚合的散列值

其中\ ``__eq__``\ 方法做了下修改，用到了归约函数all()，比\ ``tuple(self) == tuple(other)``\ 的写法，能减少处理时间和内存。

   zip()函数取名自zipper拉链，把两个序列咬合在一起。比如：

   .. code:: python

      >>> list(zip(range(3), 'ABC'))
      [(0, 'A'), (1, 'B'), (2, 'C')]

第5版：格式化
-------------

Vector的格式化跟Vector2d大同小异，都是定义\ ``__format__``\ 方法，只是计算方式从极坐标换成了球面坐标：

.. code:: python

   def angle(self, n):
       r = math.sqrt(sum(x * x for x in self[n:]))
       a = math.atan2(r, self[n-1])
       if (n == len(self) - 1) and (self[-1] < 0):
           return math.pi * 2 - a
       else:
           return a

   def angles(self):
       return (self.angle(n) for n in range(1, len(self)))

   def __format__(self, fmt_spec=''):
       if fmt_spec.endswith('h'):  # hyperspherical coordinates
           fmt_spec = fmt_spec[:-1]
           coords = itertools.chain([abs(self)],
                                    self.angles())
           outer_fmt = '<{}>'
       else:
           coords = self
           outer_fmt = '({})'
       components = (format(c, fmt_spec) for c in coords)
       return outer_fmt.format(', '.join(components))

极坐标和球面坐标是啥？我也不知道，略过就好。

小结
----

经过上下两篇文章的介绍，我们知道了Python风格的类是什么样子的，跟常规的面向对象设计不同的是，Python的类通过魔法方法实现了Python协议，使Python类在使用时能够享受到语法糖，\ **不用通过get和set的方式来编写代码**\ 。

   参考资料：

   《流畅的Python》第10章 序列的修改、散列和切片

.. |image1| image:: ../wanggang.png
