【Python】Python变量小秘密
==========================

|image1|

变量全都是引用
--------------

跟其他编程语言不同，Python的变量不是盒子，不会存储数据，它们只是引用，就像标签一样，贴在对象上面。

比如：

.. code:: python

   >>> a = [1, 2, 3]
   >>> b = a
   >>> a.append(4)
   >>> b
   [1, 2, 3, 4]
   >>> b is a
   True

a变量和b变量引用的是同一个列表\ ``[1, 2, 3]``\ 。b可以叫做a的别名。

比较来看：

.. code:: python

   >>> a = [1, 2, 3]
   >>> c = [1, 2, 3]
   >>> c == a
   True
   >>> c is a
   False

c引用的是另外一个列表，虽然和a引用的列表的值相等，但是它们是不同的对象。

浅复制与深复制
--------------

**浅复制**\ 是指只复制最外层容器，\ **副本中的元素是源容器中元素的引用**\ 。如果所有元素都是不可变的，那么这样没有问题，还能节省内容。但是，如果有可变的元素，那么结果可能会出乎意料之外。\ **构造方法或\ ``[:]``\ 做的都是浅复制。**

示例：

.. code:: python

   >>> x1 = [3, [66, 55, 44], (7, 8, 9)]
   ## x2是x1的浅复制
   >>> x2 = list(x1)

   ## 不可变元素没有影响
   >>> x1.append(100)
   >>> x1
   [3, [66, 55, 44], (7, 8, 9), 100]
   >>> x2
   [3, [66, 55, 44], (7, 8, 9)]  

   ## x1[1]是列表，可变元素会影响x2
   ## 因为它们引用的是同一个对象
   >>> x1[1].remove(55)
   >>> x1
   [3, [66, 44], (7, 8, 9), 100]
   >>> x2
   [3, [66, 44], (7, 8, 9)]  

   ## x2[1]也会反过来影响x1
   >>> x2[1] += [33, 22]
   >>> x1
   [3, [66, 44, 33, 22], (7, 8, 9), 100]  
   >>> x2
   [3, [66, 44, 33, 22], (7, 8, 9)]

   ## 不可变元组也不会有影响
   ## +=运算符创建了一个新元组
   >>> x2[2] += (10, 11)
   >>> x1
   [3, [66, 44, 33, 22], (7, 8, 9), 100]  
   >>> x2
   [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]

**深复制**\ 是指我们常规理解的复制，副本不共享内部对象的引用，是\ **完全独立的一个副本**\ 。这可以借助copy.deepcopy来实现。

示例：

.. code:: python

   >>> a = [10, 20]
   >>> b = [a, 30]
   >>> a.append(b)
   >>> a
   [10, 20, [[...], 30]]
   >>> from copy import deepcopy
   >>> c = deepcopy(a)
   >>> c
   [10, 20, [[...], 30]]

即使是有循环引用也能正确复制。

   注意copy.copy()是浅复制，copy.deepcopy()是深复制。

函数传参
--------

Python唯一支持的参数传递模式是共享传参，也就是指函数的各个形式参数获得实参中各个引用的副本。因为Python的变量全都是引用。对于不可变对象来说没有问题，但是对于可变对象就不一样了。

示例：

.. code:: python

   >>> def f(a, b):
   ...     a += b
   ...     return a
   ... 

   ## 数字不变
   >>> x = 1
   >>> y = 2
   >>> f(x, y)
   3
   >>> x, y
   (1, 2)

   ## 列表变了
   >>> a = [1, 2]
   >>> b = [3, 4]
   >>> f(a, b)
   [1, 2, 3, 4]
   >>> a, b
   ([1, 2, 3, 4], [3, 4])

   ## 元组不变
   >>> t = (10, 20)
   >>> u = (30, 40)
   >>> f(t, u)
   (10, 20, 30, 40)
   >>> t, u
   ((10, 20), (30, 40))

由此可以得出一条警示：\ **函数参数尽量不要使用可变参数，如果非用不可，应该考虑在函数内部进行复制。**

示例：

.. code:: python

   class TwilightBus:
       """A bus model that makes passengers vanish"""

       def __init__(self, passengers=None):
           if passengers is None:
               self.passengers = []
           else:
               self.passengers = passengers

       def pick(self, name):
           self.passengers.append(name)

       def drop(self, name):
           self.passengers.remove(name)

测试一下：

.. code:: python

   >>> basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
   >>> bus = TwilightBus(basketball_team)
   >>> bus.drop('Tina')
   >>> bus.drop('Pat')
   >>> basketball_team
   ['Sue', 'Maya', 'Diana']

TwilightBus下车的学生，竟然从basketball_team中消失了。这是因为self.passengers引用的是同一个列表对象。修改方法很简单，复制个副本：

.. code:: python

       def __init__(self, passengers=None):
           if passengers is None:
               self.passengers = []
           else:
               self.passengers = list(passengers)  # 使用构造函数复制副本

del和垃圾回收
-------------

del语句删除的是引用，而不是对象。但是del可能会导致对象没有引用，进而被当做垃圾回收。

示例：

.. code:: python

   >>> import weakref
   >>> s1 = {1, 2, 3}
   ## s2和s1引用同一个对象
   >>> s2 = s1
   >>> def bye():
   ...     print("Gone")
   ...     
   ## 监控对象和调用回调
   >>> ender = weakref.finalize(s1, bye)
   >>> ender.alive
   True
   ## 删除s1后还存在s2引用
   >>> del s1
   >>> ender.alive
   True
   ## s2重新绑定导致{1, 2, 3}引用归零
   >>> s2 = "spam"
   Gone
   ## 对象被销毁了
   >>> ender.alive
   False

在CPython中，对象的引用数量归零后，对象会被立即销毁。如果除了循环引用之外没有其他引用，两个对象都会被销毁。

弱引用
------

某些情况下，可能需要保存对象的引用，但不留存对象本身。比如，有个类想要记录所有实例。这个需求可以使用弱引用实现。

比如上面示例中的weakref.finalize(s1,
bye)，finalize就持有\ ``{1, 2, 3}``\ 的弱引用，虽然有引用，但是不会影响对象被销毁。

其他使用弱引用的方式是WeakDictionary、WeakValueDictionary、WeakSet。

示例：

.. code:: python

   class Cheese:

       def __init__(self, kind):
           self.kind = kind

       def __repr__(self):
           return 'Cheese(%r)' % self.kind

.. code:: python

   >>> import weakref
   >>> stock = weakref.WeakValueDictionary()
   >>> catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
   ...                 Cheese('Brie'), Cheese('Parmesan')]
   ...
   >>> for cheese in catalog:
           # 用作缓存
           # key是cheese.kind
           # value是cheese的弱引用
   ...     stock[cheese.kind] = cheese
   ...
   >>> sorted(stock.keys())
   ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']

   ## 删除catalog引用，stock弱引用不影响垃圾回收
   ## WeakValueDictionary的值引用的对象被销毁后，对应的键也会自动删除
   >>> del catalog
   >>> sorted(stock.keys())  # 还存在一个cheese临时变量的引用
   ['Parmesan']

   ## 删除cheese临时变量的引用，stock就完全清空了
   >>> del cheese
   >>> sorted(stock.keys())
   []

..

   注意不是每个Python对象都可以作为弱引用的目标，比如基本的list和dict就不可以，但是它们的子类是可以的：

   .. code:: python

      class MyList(list):
          pass
      a_list = MyList(range(10))
      weakref_to_a_list = weakref.ref(a_list)

小结
----

本文首先阐述了Python变量全部都是引用的这个事实，这意味着在Python中，简单的赋值是不创建副本的。如果要创建副本，可以选择浅复制和深复制，浅复制使用构造方法、\ ``[:]``\ 或\ ``copy.copy()``\ ，深复制使用\ ``copy.deepcopy()``\ 。del删除的是引用，但是会导致对象没有引用而被当做垃圾回收。有时候需要保留引用而不保留对象（比如缓存），这叫做弱引用，weakref库提供了相应的实现。

   参考资料：

   《流畅的Python》

.. |image1| image:: ../wanggang.png
