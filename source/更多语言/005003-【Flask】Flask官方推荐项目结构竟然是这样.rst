【Flask】Flask官方推荐项目结构竟然是这样
========================================

|image1|

Flask有个特点：千人千面。它没有硬性规定，你必须采用哪种项目结构来组织代码，这就导致每个人都按照自己的习惯和喜好来写，写出来的项目结构往往是千差万别。在Flask2.0的官方文档中，有一节内容介绍了Flask的项目结构，我们可以窥探一番。

Mock式结构
----------

Flask是很适合用来做Mock的，比如调试前端代码时，后端服务不一定准备好了，那么就可以先用Flask模拟后端接口返回数据。

Mock式项目结构很简单，创建一个文件夹：

.. code:: shell

   $ mkdir flask-tutorial
   $ cd flask-tutorial

然后在这个文件夹下面随便创建一些\ ``.py``\ 文件，来写Mock代码即可。

比如创建一个\ ``hello.py``\ 文件：

.. code:: python

   from flask import Flask

   app = Flask(__name__)


   @app.route('/hello')
   def hello():
       return 'Hello, World!'

再创建一个\ ``order.py``\ 文件：

.. code:: python

   from flask import Flask

   app = Flask(__name__)


   @app.route('/order')
   def order():
       return {"id": 123456789}

项目结构如下所示：

::

   /home/user/Projects/flask-tutorial
   ├── hello.py
   ├── order.py

Project式结构
-------------

Flask最正统的用法是写Web后端服务，相对于Django来说，Flask的项目结构要简洁很多，如下所示：

::

   /home/user/Projects/flask-tutorial
   ├── flaskr/
   │   ├── __init__.py
   │   ├── db.py
   │   ├── schema.sql
   │   ├── auth.py
   │   ├── blog.py
   ├── tests/
   │   ├── conftest.py
   │   ├── data.sql
   │   ├── test_factory.py
   │   ├── test_db.py
   │   ├── test_auth.py
   │   └── test_blog.py
   ├── venv/
   ├── setup.py
   └── MANIFEST.in

-  ``flaskr/`` 存放项目主要源文件的包。
-  ``tests/`` 存放测试代码的目录。(使用pytest框架来写)
-  ``venv/`` Python虚拟环境目录。
-  ``setup.py`` 项目构建信息的描述。
-  ``MANIFEST.in`` 项目包含或排除其他文件夹的说明。

可以看出来官方并没有给出\ ``flaskr/``\ 更为具体的目录结构设计了，项目规模不同，编程经验不一，自由发挥空间越大，结构差异化就越明显。这跟Flask的设计理念其实是保持一致的，\ **Flask只提供核心功能，不限制你做什么，把选择权交给你自己**\ 。

Git忽略文件
-----------

如果采用Git对源代码进行管理，可以配置下面的\ ``.gitignore``\ 文件：

::

   venv/

   *.pyc
   __pycache__/

   instance/

   .pytest_cache/
   .coverage
   htmlcov/

   dist/
   build/
   *.egg-info/

把这些文件夹和文件，排除到提交的代码之外。

   参考资料：

   https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

   https://blog.csdn.net/cckavin/article/details/97945913

.. |image1| image:: ../wanggang.png
