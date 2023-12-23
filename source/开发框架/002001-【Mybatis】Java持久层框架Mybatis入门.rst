【Mybatis】Java持久层框架Mybatis入门
====================================

|image1|

MyBatis是什么
-------------

MyBatis是Java的持久层框架，GitHub的star数高达15.8k，是Java技术栈中最热门的ORM框架之一。它支持自定义SQL、存储过程以及高级映射，可以通过XML或注解来配置和映射原始类型、接口和Java
POJOs为数据库中的记录。

   POJOs，Plain Old Java Objects，纯的传统意义的Java对象，最基本的Java
   Bean只有属性加上属性的get和set方法。

|image2|

安装
----

Maven pom.xml：

.. code:: xml

   <dependency>
     <groupId>org.mybatis</groupId>
     <artifactId>mybatis</artifactId>
     <version>x.x.x</version>
   </dependency>

..

   版本查询：https://mvnrepository.com/artifact/org.mybatis/mybatis

SqlSessionFactory
-----------------

SqlSessionFactory的实例是每个MyBatis应用的核心，通过SqlSessionFactoryBuilder创建，能基于XML配置，也能使用Configuration类。

基于XML配置：

.. code:: java

   String resource = "org/mybatis/example/mybatis-config.xml";
   InputStream inputStream = Resources.getResourceAsStream(resource);
   SqlSessionFactory sqlSessionFactory =
     new SqlSessionFactoryBuilder().build(inputStream);

实际项目中不会手动设置XML文件路径，而是直接读取classpath去找XML。

使用Configuration类：

.. code:: java

   DataSource dataSource = BlogDataSourceFactory.getBlogDataSource();
   TransactionFactory transactionFactory =
     new JdbcTransactionFactory();
   Environment environment =
     new Environment("development", transactionFactory, dataSource);
   Configuration configuration = new Configuration(environment);
   configuration.addMapper(BlogMapper.class);
   SqlSessionFactory sqlSessionFactory =
     new SqlSessionFactoryBuilder().build(configuration);

由于Java注解的一些限制以及某些MyBatis映射的复杂性，MyBatis会优先选择XML配置。在上面的示例中，MyBatis会根据classpath和BlogMapper.class去找BlogMapper.xml。

SqlSession
----------

SqlSessionFactory能创建SqlSession实例，SqlSession提供了在数据库执行SQL的所有方法。比如：

.. code:: java

   try (SqlSession session = sqlSessionFactory.openSession()) {
     BlogMapper mapper = session.getMapper(BlogMapper.class);
     Blog blog = mapper.selectBlog(101);
   }

背后的SQL语句
-------------

隐藏在mapper.selectBlog()方法背后的SQL语句是配置在XML文件里面的。

一般XML的配置信息如下：

.. code:: xml

   <?xml version="1.0" encoding="UTF-8" ?>
   <!DOCTYPE configuration
     PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
     "http://mybatis.org/dtd/mybatis-3-config.dtd">
   <configuration>
     <environments default="development">
       <environment id="development">
         <transactionManager type="JDBC"/>
         <dataSource type="POOLED">
           <property name="driver" value="${driver}"/>
           <property name="url" value="${url}"/>
           <property name="username" value="${username}"/>
           <property name="password" value="${password}"/>
         </dataSource>
       </environment>
     </environments>
     <mappers>
       <mapper resource="org/mybatis/example/BlogMapper.xml"/>
     </mappers>
   </configuration>

environment配置了数据源和连接池。

mapper包含了SQL语句：

.. code:: xml

   <?xml version="1.0" encoding="UTF-8" ?>
   <!DOCTYPE mapper
     PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
     "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
   <mapper namespace="org.mybatis.example.BlogMapper">
     <select id="selectBlog" resultType="Blog">
       select * from Blog where id = #{id}
     </select>
   </mapper>

mapper.selectBlog()方法映射到了XML里面的id selectBlog。

值得注意的是，对于简单SQL来说，可以直接使用Java注解：

.. code:: java

   package org.mybatis.example;
   public interface BlogMapper {
     @Select("SELECT * FROM blog WHERE id = #{id}")
     Blog selectBlog(int id);
   }

但是对于复杂SQL还是写XML更方便。

作用域与生命周期
----------------

从前面几个小节我们知道了SqlSessionFactoryBuilder→SqlSessionFactory→SqlSession→Mapper
Instances的实例对象产生链路，接下来看看它们各自的作用域与生命周期：

-  SqlSessionFactoryBuilder

   作用域是method，用完就释放，避免XML解析资源占用。

-  SqlSessionFactory

   作用域是application，只要创建就一直存在，可以通过单例模式来实现。

-  SqlSession

   作用域是request或method，每个线程独一份，每次收到HTTP请求，打开一个SqlSession，返回响应后，就关闭它。以下代码能确保每次关闭：

   .. code:: java

      try (SqlSession session = sqlSessionFactory.openSession()) {
        // do work
      }

-  Mapper Instances

   它是由SqlSession创建的，作用域类似，不过更建议放到method，用完就释放，比如：

   .. code:: java

      try (SqlSession session = sqlSessionFactory.openSession()) {
        BlogMapper mapper = session.getMapper(BlogMapper.class);
        // do work
      }

小结
----

本文首先介绍了MyBatis是什么，然后通过SqlSessionFactoryBuilder→SqlSessionFactory→SqlSession→Mapper
Instances链路阐述了MyBatis是如何从数据库查询SQL映射到代码里面的，最后给出了这几个类实例的作用域的使用建议。

   参考资料：

   https://mybatis.org/mybatis-3/getting-started.html

   https://www.jianshu.com/p/b934b0d72602

.. |image1| image:: ../wanggang.png
.. |image2| image:: 002001-【Mybatis】Java持久层框架Mybatis入门/mybatis-logo.png
