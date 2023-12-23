接口自动化项目落地之HTTPBin网站
===============================

|image1|

接口自动化项目落地系列
----------------------

找个开源网站或开源项目，用\ **tep**\ 实现整套\ **pytest**\ 接口自动化项目落地，归档到电子书，作为\ **tep完整教程**\ 的\ **项目篇**\ 一部分。自从tep完整教程发布以后，tep被越来越多小伙伴了解。教程只是纯理论，是骡子是马，拉出来遛遛才知道。做接口自动化项目落地，一方面是为了让自己脑海中的构想实实在在的呈现出来，现实和理想存在多少差距，不断尝试去弥补和修缮；另一方面也是方便读者朋友们学习使用，借助实际项目来练习，才能在赛道中弯道超车。

HTTPBin网站
-----------

httpbin.org是一个简单的在线提供HTTP服务的网站：

|image2|

|image3|

它能够用来对HTTP进行在线测试。

测试报告
--------

HTTPBin网站的接口自动化项目包含\ **11个用例集**\ ：

|image4|

**67条测试用例**\ ：

|image5|

**自动化执行正确率98.5%**\ ，其中有1条错误结果，是我故意为之的，因为想展示下断言失败的效果。

环境配置
--------

包含http和https两套环境，因为HTTPBin支持HTTP&HTTPS：

*fixtures/fixture_env_vars.py*

.. code:: python

   #!/usr/bin/python
   ## encoding=utf-8

   from tep.fixture import *


   @pytest.fixture(scope="session")
   def env_vars(config):
       class Clazz(TepVars):
           env = config["env"]

           """变量定义开始"""
           # 环境变量
           mapping = {
               "http": {  # http环境
                   "domain": "http://httpbin.org",
               },
               "https": {  # https环境
                   "domain": "https://httpbin.org",
               }
               # 继续添加
           }
           # 定义类属性，敲代码时会自动补全
           domain = mapping[env]["domain"]
           """变量定义结束"""

       return Clazz()

配置默认为http环境：

*conf.yaml*

.. code:: yaml

   env: http

用例集
------

http-methods
~~~~~~~~~~~~

|image6|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("get请求")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/get",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

auth
~~~~

|image7|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("Authorization以Bearer开头，认证成功")
   def test(env_vars):
       # 描述
       # http://httpbin.org/#/Auth/get_basic_auth__user___passwd_
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/bearer",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'Authorization': 'Bearer ZG9uZ2ZhbmdlcjoxMjM0NTY=',  # 替换token
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

status-codes
~~~~~~~~~~~~

|image8|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("post返回状态码300")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "post",
           url=env_vars.domain + "/status/300",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'Content-Length': '0', 'accept': 'text/plain',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Origin': 'http://httpbin.org', 'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           json={}
       )
       # 提取
       # 断言
       assert response.status_code == 300

request_inspection
~~~~~~~~~~~~~~~~~~

|image9|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("捕获请求信息--headers")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/headers",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400
       assert response.json()["headers"]

response_inspection
~~~~~~~~~~~~~~~~~~~

|image10|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("捕获响应信息--缓存")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/cache",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                    'accept': 'application/json', 'If-None-Match': '1', 'If-Modified-Since': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code == 304

response_formats
~~~~~~~~~~~~~~~~

|image11|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("txt文本text/plain")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/robots.txt",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'text/plain',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400
       assert response.headers["content-type"] == "text/plain"

dynamic_data
~~~~~~~~~~~~

|image12|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("base64解码")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/base64/SFRUUEJJTiBpcyBhd2Vzb21l",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'text/html',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400
       assert "HTTPBIN is awesome" == response.text

cookies
~~~~~~~

|image13|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("cookies")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/cookies",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400
       assert response.json()["cookies"]

images
~~~~~~

|image14|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("图片")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/image",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'image/webp',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

redirects
~~~~~~~~~

|image15|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("重定向")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/redirect/1",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'text/html',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code == 404

anything
~~~~~~~~

|image16|

.. code:: python

   import allure
   from tep.client import request


   @allure.title("返回所有数据")
   def test(env_vars):
       # 描述
       # 数据
       # 请求
       response = request(
           "delete",
           url=env_vars.domain + "/anything",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Origin': '', 'Referer': '/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           json={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

       # 描述
       # 数据
       # 请求
       response = request(
           "get",
           url=env_vars.domain + "/anything",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Referer': '/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           params={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

       # 描述
       # 数据
       # 请求
       response = request(
           "patch",
           url=env_vars.domain + "/anything",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Origin': '', 'Referer': '/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           json={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

       # 描述
       # 数据
       # 请求
       response = request(
           "post",
           url=env_vars.domain + "/anything",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'Content-Length': '0',
                    'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Origin': '', 'Referer': '/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           json={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

       # 描述
       # 数据
       # 请求
       response = request(
           "put",
           url=env_vars.domain + "/anything",
           headers={'Host': 'httpbin.org', 'Proxy-Connection': 'keep-alive', 'Content-Length': '0',
                    'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                    'Origin': '', 'Referer': '/', 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Cookie': 'stale_after=never; fake=fake_value; freeform=3; name=dongfanger'},
           json={}
       )
       # 提取
       # 断言
       assert response.status_code < 400

只花了3小时完成
---------------

通过mitmproxy来录制流量自动生成用例，效率得到了极大的提高，从原来的1天缩短到3小时就完成了整个项目落地。相比于手工编写用例，这次写HTTPBin的接口自动化，我使用了\ ``utils/mitm.py``\ 来录制流量，mitmproxy稍微不方便的是需要手动开启代理，不过适应了以后还是能接受。录制流量后就会生成自动化用例，但是还需要二次修改，才会变成最终的用例。主要修改的工作量是在添加断言，根据业务设置合理的断言。其次是替换url为\ ``env_vars.domain + "/api"``\ 拼接方式，直接批量Replace即可。然后就是修改文件名和\ ``@allure.title``\ 了，给用例加上标题。工欲善其事，必先利其器。

tep共建
-------

欢迎添加微信：\ **cekaigang**\ ，分享交流tep实践案例，可以提供开源项目我来写，也可以写好后发我一起看看，优秀的项目会添加到tep完整教程的项目篇，以便更多测试同行们借鉴，大佬们赶快来加入我们吧。

   参考资料：

   HTTPBin接口自动化项目源码 https://github.com/dongfanger/httpbin

   postman https://www.postman.com/postman/workspace/httpbin/collection/

.. |image1| image:: ../wanggang.png
.. |image2| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-17-43-28-image.png
.. |image3| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-17-43-51-image.png
.. |image4| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-17-45-27-image.png
.. |image5| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-17-46-03-image.png
.. |image6| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-41-03-image.png
.. |image7| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-40-29-image.png
.. |image8| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-39-56-image.png
.. |image9| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-39-17-image.png
.. |image10| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-38-45-image.png
.. |image11| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-37-50-image.png
.. |image12| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-37-12-image.png
.. |image13| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-35-04-image.png
.. |image14| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-34-25-image.png
.. |image15| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-33-27-image.png
.. |image16| image:: 000012-接口自动化项目落地之HTTPBin网站/2022-03-15-18-32-27-image.png
