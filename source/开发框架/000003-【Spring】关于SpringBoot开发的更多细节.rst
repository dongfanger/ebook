【Spring】关于SpringBoot开发的更多细节
======================================

|image1|

在上篇文章《开发你的第一个SpringBoot应用》已经对SpringBoot基本开发流程有了大体了解，本文将继续对SpringBoot官网进行学习，发现关于SpringBoot开发的更多细节。

依赖管理
--------

推荐使用Maven或者Gradle进行依赖管理，其他工具比如Ant，SpringBoot对它们的支持不是很好。

SpringBoot提供了很多starter来批量添加依赖，比如\ ``spring-boot-starter-web``\ 。官方定义的starter都是\ ``spring-boot-starter-*``\ 这种命名方式，由\ ``org.springframework.boot``\ 提供：

https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using.build-systems.starters

而自定义的第三方starter命名方式往往会把名字放在前面，像这样：\ ``thirdpartyproject-spring-boot-starter``\ 。

代码目录
--------

官方推荐的代码目录是这样：

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

-  包名采用\ ``com.example.myapplication``\ 这种方式。
-  main启动入口类\ ``MyApplication.java``\ 放在根目录，便于查找其他文件。
-  其他模块跟\ ``MyApplication.java``\ 并列。

配置
----

**尽量不使用xml进行配置**\ ，而是定义一个配置类加上\ ``@Configuration``\ 注解。如果非得用xml，那么可以用\ ``@ImportResource``\ 进行导入。配置类也不用写成一个，多个配置类可以使用多个\ ``@Configuration``\ ，也可以拆成多个使用\ ``@Import``\ 相互导入。

   xml一直被很多人吐槽，其实SpringBoot也是反对使用xml的。

``@SpringBootApplication``\ 注解已经包含了\ ``@EnableAutoConfiguration``\ 注解，会对配置进行\ **自动导入**\ ，比如在classpath中有一个\ ``HSQLDB``\ ，如果没有手动配置数据库连接，那么SpringBoot会自动进行配置。一般只添加\ ``@SpringBootApplication``\ 就可以了，不需要再重复添加\ ``@EnableAutoConfiguration``\ 。

通过启动应用时加上\ ``--debug``\ 可以查看有哪些自动配置类，也可以对自动配置类进行移除，比如：

.. code:: java

   @SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
   public class MyApplication {

   }

还可以使用\ ``excludeName``\ 或\ ``spring.autoconfigure.exclude``\ 属性来指定要移除的自动配置类。

依赖注入
--------

SpringBoot可以添加\ ``@ComponentScan``\ 来自动查找bean，比如\ ``@Component``\ 、\ ``@Service``\ 、\ ``@Repository``\ 、\ ``@Controller``\ 会被自动注册为Spring
Beans。\ ``@SpringBootApplication``\ 已经包含了\ ``@ComponentScan``\ ，所以不需要重复添加。

比如\ ``@Service``\ 使用构造器来包含一个bean：

.. code:: java

   @Service
   public class MyAccountService implements AccountService {

       private final RiskAssessor riskAssessor;

       public MyAccountService(RiskAssessor riskAssessor) {
           this.riskAssessor = riskAssessor;
       }

       // ...

   }

如果有多个构造器，那么可以使用\ ``@Autowired``\ 让Spring来自动注入：

.. code:: java

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

@SpringBootApplication
----------------------

一般在main方法上面会有这个注解，它实际上包含了3个注解：

-  ``@EnableAutoConfiguration``
-  ``@ComponentScan``
-  ``@SpringBootConfiguration``

.. code:: java

   @SpringBootApplication // same as @SpringBootConfiguration @EnableAutoConfiguration
                           // @ComponentScan
   public class MyApplication {

       public static void main(String[] args) {
           SpringApplication.run(MyApplication.class, args);
       }

   }

如果只想包含其中部分注解，那么可以不用\ ``@SpringBootApplication``\ ：

.. code:: java

   @SpringBootConfiguration(proxyBeanMethods = false)
   @EnableAutoConfiguration
   @Import({ SomeConfiguration.class, AnotherConfiguration.class })
   public class MyApplication {

       public static void main(String[] args) {
           SpringApplication.run(MyApplication.class, args);
       }

   }

启动方式
--------

①IDEA使用Run as Java Application。

②命令行启动jar包。

::

   $ java -jar target/myapplication-0.0.1-SNAPSHOT.jar

开启远程调式

::

   $ java -Xdebug -Xrunjdwp:server=y,transport=dt_socket,address=8000,suspend=n \
          -jar target/myapplication-0.0.1-SNAPSHOT.jar

③maven

::

   $ mvn spring-boot:run

..

   参考资料：

   https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using

.. |image1| image:: ../wanggang.png
