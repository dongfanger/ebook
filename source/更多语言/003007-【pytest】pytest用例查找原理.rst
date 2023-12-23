【pytest】pytest用例查找原理
============================

|image1|

当执行pytest命令时，pytest会从project中查找test来执行。本文先从几个路径相关的概念讲起，这样便于理解pytest在遍历路径时的走向。

几个路径相关的概念
~~~~~~~~~~~~~~~~~~

PYTHONHOME
^^^^^^^^^^

定义了Python标准库的路径。

PYTHONPATH
^^^^^^^^^^

定义了Python import模块搜索的路径。

basedir
^^^^^^^

①如果是module，目录中不包括\ ``__init__.py``\ ，basedir的值等于a

::

   a
   |--b_test.py

②如果是package，目录中包括\ ``__init__.py``\ ，basedir的值等于y

::

   y
   |--a
   |  |--b_test.py
   |  |--__init__.py  // 表明a是package

③如果是package的package，目录中都包括\ ``__init__.py``\ ，basedir的值等于x

::

   x
   |--y
   |  |--a
   |  |--__init__.py  // 表明y是package
   |  |  |--b_test.py
   |  |  |--__init__.py  // 表明a是package

sys.path
^^^^^^^^

模块搜索路径集，包括以上3个目录。它决定了import能否找到模块。

current working directory
^^^^^^^^^^^^^^^^^^^^^^^^^

当前工作目录，缩写cwd，等于执行\ ``pytest``\ 命令的目录。

如果用\ ``python -m pytest``\ ，以模块的方式来执行，会把cwd也加入sys.path中。

例如，在a目录下执行pytest，cwd是a，basedir是y，sys.path中只包含y。如果执行python
-m pytest，sys.path中既包含y也包含a

::

   y
   |--a
   |  |--b_test.py
   |  |--__init__.py  // 表明a是package

pytest查找原理
~~~~~~~~~~~~~~

第一种情况
^^^^^^^^^^

pytest命令是可以加参数的，如果加了文件夹/文件参数，那么就只在参数指定的文件夹/文件中查找，可以指定多个。例如

.. code:: shell

   pytest a_dir b_dir c_test.py d_test.py

特殊的，如果a_dir中包含了c_test.py，那么会收集成2次，pytest也会执行2次。

也可以使用::来指定函数/类/方法，例如

::

   pytest test_mod.py::test_func

::

   pytest test_mod.py::TestClass::test_method

第二种情况
^^^^^^^^^^

pytest不带参数。

-  从“当前工作目录”开始找，递归查找子目录。匹配 test_*.py 或 \*_test.py
   的文件。

-  找到这些模块（Python中1个.py文件就是1个模块）以后，进一步根据上节所述找basedir。

-  调用\ ``sys.path.insert(0, basedir)``\ ，把basedir加入sys.path中。这些模块就可以被pytest
   import了。

-  import之后，查找test开头的函数或方法。如果是类中的方法，类必须以Test开头，并且没有__init__方法。

.. |image1| image:: ../wanggang.png
