【UI自动化】webdriver使用已打开过的chrome
=========================================

|image1|

基本功能：

::

   执行脚本a，打开一个chrome，脚本a执行完成，chrome未关闭。
   执行脚本b，继续使用a打开的chrome，不新启浏览器。

附加：

::

   如果已打开的chrome未关闭，则在chrome中新建标签页来打开新的页面。
   如果已打开的chrome已关闭，则新启浏览器。

最近用python+selenium+pytest，写了个测试小工具用来自动化登陆浏览器，一方面是方便管理网址、账号、密码，存放在脚本中，另一方面也省去了频繁输入登陆网站的操作，节省了不少时间。

但这个小工具用起来存在明显问题：每次都新启一个浏览器，多了后就是这样的

|image2|

根本不知道谁是谁。

于是就想到要实现前面提到的这些功能。

首先要解决的第一个问题就是，怎么重新使用已打开的chrome。百度后知晓，是通过session_id。浏览器都有一个session_id，拿到这个session_id就可以通过webdriver.Remote去调chrome。

.. code:: python

   driver = webdriver.Chrome()
   params["session_id"] = driver.session_id
   params["server_url"] = driver.command_executor._url

   driver = webdriver.Remote(command_executor=params["server_url"])
   driver.session_id = params["session_id"]

经过试验，python存在一个坑是每次初始化就会调start_session去新开一个空白的浏览器。网上有解决方案是继承Remote，重写start_session方法。然而，仔细看完代码就发现，何必多此一举，直接quit()就搞定。

.. code:: python

   driver = webdriver.Remote(command_executor=params["server_url"])
   driver.quit()  # 退出start_session新开的空白浏览器
   driver.session_id = params["session_id"]

quit是quit了，但driver还存在呀，所以还是多理清思路，才能避免走冤枉路。

然后要解决的第二个问题就是，如何在执行脚本b的时候再接着用session。当然就是存本地咯。这里用到的是pickle，能很方便的在本地存取变量。

存

.. code:: python

   with open(session_file, 'wb') as f:
       pickle.dump(params, f)

取

.. code:: python

   with open(session_file, 'rb') as f:
       params = pickle.load(f)

第三个问题就是新开标签页和切换窗口。

.. code:: python

   driver.execute_script('window.open("");')  # 调js
   driver.switch_to.window(driver.window_handles[-1])  # 切换到最后一个页签

最后要解决的一个问题就是，如果已经打开的chrome关掉了，从本地文件读取的session就会过时。拿这个过时session去用，就会”chrome
not
reachable“。解决思路就是，捕获driver抛出的WebDriverException，重新创建新的driver。

.. code:: python

   try:
       driver = webdriver.Remote(command_executor=params["server_url"])
       driver.quit()  # 退出start_session新开的空白浏览器
       driver.session_id = params["session_id"]
       driver.execute_script('window.open("");')
       driver.switch_to.window(driver.window_handles[-1])
   except:
       driver = create_driver()

完整代码

.. code:: python

   session_file = 'browser_session.data'


   def create_driver():
       driver = webdriver.Chrome()
       with open(session_file, 'wb') as f:
           params = {"session_id": driver.session_id, "server_url": driver.command_executor._url}
           pickle.dump(params, f)
       return driver

     
   if not Path(session_file).exists():
       driver = create_driver()
   else:
       with open(session_file, 'rb') as f:
           params = pickle.load(f)
           try:
               driver = webdriver.Remote(command_executor=params["server_url"])
               driver.quit()  # 退出start_session新开的空白浏览器
               driver.session_id = params["session_id"]
               driver.execute_script('window.open("");')
               driver.switch_to.window(driver.window_handles[-1])
           except:
               driver = create_driver()

.. |image1| image:: ../wanggang.png
.. |image2| image:: 013001-【UI自动化】webdriver使用已打开过的chrome/20190830170629375.png
