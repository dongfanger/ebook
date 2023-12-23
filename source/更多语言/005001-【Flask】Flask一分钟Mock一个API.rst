【Flask】Flask一分钟Mock一个API
===============================

|image1|

如果安装了Python，并且安装了Flask：

.. code:: shell

   pip install flask

那么就可以在短短\ **一分钟**\ 内Mock出来\ **一个API**\ ，而且只需要用到\ **一个文件**\ 。

彻底告别在线Mock网站无法指定请求方法，Postman配置繁琐的问题。

建一个文件
----------

随便在哪创建一个py文件，比如app.py。

写一段代码
----------

.. code:: python

   from flask import Flask

   app = Flask(__name__)

   @app.route("/")
   def hello_world():
       return "Hello, World!"

   if __name__ == "__main__":
       app.run()

跑一条命令
----------

在cmd或shell执行\ ``python app.py``\ ，服务就起来了：

.. code:: shell

   D:\>python app.py
    * Serving Flask app "app" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

测试一下：

.. code:: shell

   D:\>curl http://127.0.0.1:5000/
   Hello, World!

GET请求
-------

不带参数
~~~~~~~~

代码：

.. code:: python

   @app.route("/testGet")
   def my_get():
       return "This is GET"

测试：

.. code:: shell

   D:\>curl http://127.0.0.1:5000/testGet
   This is GET

带参数
~~~~~~

代码：

.. code:: python

   @app.route("/testGetParams")
   def my_get_params():
       return request.args

测试：

.. code:: shell

   D:\>curl "http://127.0.0.1:5000/testGetParams?a=1&b=2"
   {"a":"1","b":"2"}

POST请求
--------

.. _不带参数-1:

不带参数
~~~~~~~~

代码：

.. code:: python

   @app.route("/testPost", methods=["POST"])
   def my_post():
       return "This is POST"

测试：

.. code:: shell

   D:\>curl -X POST "http://127.0.0.1:5000/testPost"
   This is POST

带Json参数
~~~~~~~~~~

代码：

.. code:: python

   @app.route("/testPostJson", methods=["POST"])
   def my_post_json():
       return request.json

``test.json``\ ：

.. code:: json

   {
       "name": "dongfanger",
       "alias": "redsun"
   }

测试：

.. code:: shell

   D:\>curl -H "Content-Type: application/json" -d "@test.json" "http://127.0.0.1:5000/testPostJson"
   {'name': 'dongfanger', 'alias': 'redsun'}

同时GET和POST
-------------

代码：

.. code:: python

   @app.route("/testGetPost", methods=["GET", "POST"])
   def my_get_post():
       if request.method == "GET":
           return "This is GET"
       if request.method == "POST":
           return "This is POST"

测试：

.. code:: shell

   D:\>curl http://127.0.0.1:5000/testGetPost
   This is GET
   D:\>curl http://127.0.0.1:5000/testGetPost -X POST
   This is POST

请求头
------

代码：

.. code:: python

   @app.route("/testHeaders")
   def my_headers():
       return str(request.headers)

测试：

.. code:: shell

   D:\>curl http://127.0.0.1:5000/testHeaders
   Host: 127.0.0.1:5000
   User-Agent: curl/7.55.1
   Accept: */*

完整代码解析
------------

.. code:: python

   from flask import Flask, request

   ## Flask实例
   app = Flask(__name__)


   ## @app.route添加路由
   @app.route("/testGet")
   def my_get():
       return "This is GET"


   @app.route("/testGetParams")
   def my_get_params():
       # flask.request里面封装了请求数据，可以看需要获取
       return request.args

   ## methods指定请求方法
   @app.route("/testPost", methods=["POST"])
   def my_post():
       return "This is POST"


   @app.route("/testPostJson", methods=["POST"])
   def my_post_json():
       return request.json

   ## 可以同时指定GET和POST
   @app.route("/testGetPost", methods=["GET", "POST"])
   def my_get_post():
       # 判断请求方法是GET或POST
       if request.method == "GET":
           return "This is GET"
       if request.method == "POST":
           return "This is POST"


   @app.route("/testHeaders")
   def my_headers():
       return str(request.headers)


   if __name__ == "__main__":
       app.run()

小结
----

本文介绍了如何使用Flask在一分钟内Mock一个API，只需要\ **一个文件，一段代码，一条命令**\ ，即可完成。然后分别介绍了常用的GET请求和POST请求，以及带不带参数，获取请求头的用法。在测试时用到了curl命令，它的名字是Client
URL的意思，在Mac和Windows都可以安装使用。

   参考资料：

   https://flask.palletsprojects.com/en/2.0.x/quickstart/

   http://www.ruanyifeng.com/blog/2019/09/curl-reference.html

.. |image1| image:: ../wanggang.png
