【Django】Django匆匆一眼却解答了多年疑惑
========================================

|image1|

Django 是 Python 的 一款 Web 开发框架，另外还有
Tornado，Flask，Twisted。为什么我要选择学
Django？原因很简单，上家公司来了个网易的测开，就是用 Django
开发的测试平台。

   这位测开没多久就离职去腾讯了，我啥也没学到，看了他的代码，很多是写的
   Vue 代码，哭啊。

Django 诞生于 2003 年的秋天，由 Lawrence Journal-World 报纸的程序员
Adrian Holovaty 和 Simon Willison
编写而成。新闻编辑室的开发节奏是非常快的，正因如此，Django
相比于其他框架的特点就是短、平、快。这也符合 Python
的风格。时至今日，Django 已经发展到了 3.1.3
版本。本系列将基于这一版本的官方文档，边学习边实践，整理成文，分享给大家。

   Django
   系列不是教程，而是学习笔记、心得体会、踩坑记录，内容编排上可能会有点乱。需要看教程请阅读官方文档，水平有限，实在抱歉。

Django 遵循 MVC 架构模式，所以接下来就看看如何使用 Django 完成 Web
开发。特别注意，本文的内容不具有实操性，看看即可。

定义 model
----------

model 是数据模型，定义了数据库的表和字段。

例如：

.. code:: python

   from django.db import models

   class Reporter(models.Model):
       full_name = models.CharField(max_length=70)

       def __str__(self):
           return self.full_name

   class Article(models.Model):
       pub_date = models.DateField()
       headline = models.CharField(max_length=200)
       content = models.TextField()
       reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

       def __str__(self):
           return self.headline

通过类和属性，分别定义了 2 张表 Reporter 和
Article，以及它们的字段（Reporter 1 个字段，Article 4 个字段）。

这其实就是 ORM，即 Object Relational
Mapping，对象关系映射，把程序代码中的对象映射到关系型数据库中，不用写
SQL，就可以直接操作数据了。ORM
实现了数据持久化。我们都知道程序是运行在内存中的，跑完就没了。为了把数据保存下来，就需要使用
ORM
技术把内存中的数据（程序对象）存到关系型数据库中，进而转移到磁盘上。Django
自带了一个 ORM，开箱即用。

数据迁移
--------

使用 2 条命令，就可以把 model 迁移到数据库中：

.. code:: shell

   $ python manage.py makemigrations
   $ python manage.py migrate

执行完成后，就会在数据库中按照 model
定义的表名、字段名、约束条件等，创建表结构。

数据操作
--------

接着就可以在程序中写代码操作数据了。为了直观看到结果，这里以命令行形式进行演示：

.. code:: shell

   # 导入已创建的 models
   >>> from news.models import Article, Reporter

   # 查询表 Reporter 为空
   >>> Reporter.objects.all()
   <QuerySet []>

   # 实例化对象，创建 1 条数据，表 Reporter 的字段是 full_name
   >>> r = Reporter(full_name='John Smith')

   # 必须显式调用 save() 函数，才会真正写数据到数据库
   >>> r.save()

   # 保存后就有 id 了
   >>> r.id
   1

   # 查询表 Reporter 有数据了
   >>> Reporter.objects.all()
   <QuerySet [<Reporter: John Smith>]>

   # 访问对象属性
   >>> r.full_name
   'John Smith'

   # Django 提供了 get() 函数来支持更多查询方式
   >>> Reporter.objects.get(id=1)
   <Reporter: John Smith>
   >>> Reporter.objects.get(full_name__startswith='John')
   <Reporter: John Smith>
   >>> Reporter.objects.get(full_name__contains='mith')
   <Reporter: John Smith>
   >>> Reporter.objects.get(id=2)
   Traceback (most recent call last):
       ...
   DoesNotExist: Reporter matching query does not exist.

   # 给表 Article 添加 1 条数据
   # 有 4 个字段 pub_date, headline, content, reporter
   # reporter=r，用 Reporter 对象赋值
   >>> from datetime import date
   >>> a = Article(pub_date=date.today(), headline='Django is cool',
   ...     content='Yeah.', reporter=r)
   >>> a.save()

   # 表 Article 也有数据了
   >>> Article.objects.all()
   <QuerySet [<Article: Django is cool>]>

   # a.reporter 可以赋值给 r
   >>> r = a.reporter
   >>> r.full_name
   'John Smith'

   # r 也可以访问 Article
   >>> r.article_set.all()
   <QuerySet [<Article: Django is cool>]>

   # 可以借助 filter() 函数按条件过滤数据
   >>> Article.objects.filter(reporter__full_name__startswith='John')
   <QuerySet [<Article: Django is cool>]>

   # 赋值后调用 save() 函数更新数据
   >>> r.full_name = 'Billy Goat'
   >>> r.save()

   # 使用 delete() 函数删除对象，数据库这条数据也会被删除
   >>> r.delete()

自带 Admin 后台
---------------

一般不会用它。

设计 URLs
---------

我们是通过 URL
发送请求的，服务端程序做处理，处理的函数叫做回调函数。Django 在 urls.py
文件中编写 URL 和回调函数的映射关系。例如：

.. code:: python

   from django.urls import path

   from . import views

   urlpatterns = [
       path('articles/<int:year>/', views.year_archive),
       path('articles/<int:year>/<int:month>/', views.month_archive),
       path('articles/<int:year>/<int:month>/<int:pk>/', views.article_detail),
   ]

``path()`` 的第一参数是 URL，这里使用了 ``<>`` 参数标签来获取 URL
中的数据，然后传入到回调函数中。第二个参数是回调函数，位于 views 中。

如果请求 URL “/articles/2005/05/39323/”，Django
就会获取参数值后调用回调函数：

.. code:: python

   news.views.article_detail(request, year=2005, month=5, pk=39323)

Django 在启动加载时就会把这些 path
编译为正则表达式，查找速度飞快。匹配到第一个后就会停止查找，调用回调函数。如果找完了都没有，就会调用
404 这个特殊 view，表示没找到。

编写 views
----------

在 views 中编写回调函数。每个回调函数只做 1 件事，要么返回包含响应的
``HttpResponse`` 对象，要么抛出异常，如 ``Http404`` 。例如：

.. code:: python

   from django.shortcuts import render

   from .models import Article

   def year_archive(request, year):
       a_list = Article.objects.filter(pub_date__year=year)
       context = {'year': year, 'article_list': a_list}
       return render(request, 'news/year_archive.html', context)

return render() 函数会返回一个 ``HttpResponse`` 对象。

注意，这个例子用到的是 Django 自带的模板引擎。所谓模板引擎，就是前端的
HTML
模板，里面的数据可以写成变量，从后端动态获取。除了内置的这个，还有其他模板引擎如
Thymeleaf、FreeMarker
等。不过这些使用都很少了。现在流行前后端分离，后端不需要写 HTML，只提供
RESTful 接口就可以了。说到 RESTful，就不得不提另外一个 Django 的衍生框架
DRF（Django REST Framework）。一步一步来，先学好了 Django，才能更好理解
DRF。

内置模板引擎
------------

暂时不做介绍。

小结
----

本文以 Web 后台为例，讲解了从 model，到 ORM，到数据操作，到 URL 映射，到
views
回调函数的编写链路。实际操作会复杂得多。以前学其他框架有点懵，写这篇文章，倒是让我明白了
MVC 这一套是这么一回事。

参考资料：

https://docs.djangoproject.com/en/3.1/intro/overview/

.. |image1| image:: ../wanggang.png
