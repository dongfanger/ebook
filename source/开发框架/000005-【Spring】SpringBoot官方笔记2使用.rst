【Spring】SpringBoot官方笔记2使用
=================================

|image1|

Build Systems
-------------

选择Maven or Gradle，而不要Ant（not particularly well supported）

In practice, you do not need to provide a **version** for any of these
dependencies (spring-boot-dependencies) in your build configuration, as
Spring Boot manages that for you. When you upgrade Spring Boot itself,
these dependencies are upgraded as well in a consistent way.

Each release of Spring Boot is associated with a base version of **the
Spring Framework**.

**Starters** are a set of convenient dependency descriptors that you can
include in your application.

starter命名区别：

-  official ``spring-boot-starter-*``

-  third-party ``thirdpartyproject-spring-boot-starter``

Structuring
-----------

We generally recommend that you locate your **main application class**
in a root package above other classes.

::

   com
    +- example
        +- myapplication
            +- MyApplication.java
            |
            +- customer
            |   +- Customer.java
            |   +- CustomerController.java
            |   +- CustomerService.java
            |   +- CustomerRepository.java
            |
            +- order
                +- Order.java
                +- OrderController.java
                +- OrderService.java
                +- OrderRepository.java

实际项目见得多的是controller、service这样的package，然后里面放多个文件。

Configuration
-------------

Although it is possible to use ``SpringApplication`` with XML sources,
we generally recommend that your primary source be a
single ``@Configuration`` class.

The ``@Import`` annotation can be used to import additional
configuration classes. Alternatively, you can use ``@ComponentScan`` to
automatically pick up all Spring components,
including ``@Configuration`` classes.

（因为@SpringBootApplication包含了@ComponentScan，所以能自动扫到@Configuration的配置类）

``@ImportResource`` annotation to load XML configuration files.

Auto-configuration
------------------

Spring Boot auto-configuration attempts to automatically configure your
Spring application based on the jar dependencies that you have added.

For example, if ``HSQLDB`` is on your classpath, and you have not
manually configured any database connection beans, then Spring Boot
**auto-configures an in-memory database**. If you **add your
own** ``DataSource`` bean, the default embedded database support **backs
away**.

exclude auto-configuration：

①annotation

.. code:: java

   import org.springframework.boot.autoconfigure.SpringBootApplication;
   import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

   @SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
   public class MyApplication {

   }

If the class is not on the classpath, you can use
the ``excludeName`` attribute of the annotation and specify the fully
qualified name instead.

②property

``spring.autoconfigure.exclude`` 

Spring Beans and Dependency Injection
-------------------------------------

 Spring Beans可以理解为功能模块

``@ComponentScan`` to find beans，all of your application components
(``@Component``, ``@Service``, ``@Repository``, ``@Controller``, and
others) are automatically registered as Spring Beans.

**constructor injection**\ ：

.. code:: java

   import org.springframework.stereotype.Service;

   @Service
   public class MyAccountService implements AccountService {

       private final RiskAssessor riskAssessor;

       public MyAccountService(RiskAssessor riskAssessor) {
           this.riskAssessor = riskAssessor;
       }

       // ...

   }

If a bean has more than one constructor, you will need to mark the one
you want Spring to use with ``@Autowired``:

.. code:: java

   import java.io.PrintStream;

   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;

   @Service
   public class MyAccountService implements AccountService {

       private final RiskAssessor riskAssessor;

       private final PrintStream out;

       @Autowired
       public MyAccountService(RiskAssessor riskAssessor) {
           this.riskAssessor = riskAssessor;
           this.out = System.out;
       }

       public MyAccountService(RiskAssessor riskAssessor, PrintStream out) {
           this.riskAssessor = riskAssessor;
           this.out = out;
       }

       // ...

   }

（更常见的做法是直接在类变量定义时使用@Autowired或@Resource，省去constructor）

@SpringBootApplication
----------------------

-  ``@EnableAutoConfiguration``: enable `Spring Boot’s
   auto-configuration
   mechanism <https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using.auto-configuration>`__

-  ``@ComponentScan``: enable ``@Component`` scan on the package where
   the application is located (see `the best
   practices <https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using.structuring-your-code>`__)

-  ``@SpringBootConfiguration``: enable registration of extra beans in
   the context or the import of additional configuration classes. An
   alternative to Spring’s standard ``@Configuration`` that
   aids `configuration
   detection <https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.testing.spring-boot-applications.detecting-configuration>`__ in
   your integration tests.

.. code:: java

   import org.springframework.boot.SpringApplication;
   import org.springframework.boot.autoconfigure.SpringBootApplication;

   // Same as @SpringBootConfiguration @EnableAutoConfiguration @ComponentScan
   @SpringBootApplication
   public class MyApplication {

       public static void main(String[] args) {
           SpringApplication.run(MyApplication.class, args);
       }

   }

Running
-------

jar包：using an embedded HTTP server

war包：your server

   参考资料：

   https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using

.. |image1| image:: ../wanggang.png
