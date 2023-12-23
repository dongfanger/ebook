【Spring】SpringBoot官方笔记8其他
=================================

|image1|

Container Images
----------------

::

   FROM eclipse-temurin:17-jre as builder
   WORKDIR application
   ARG JAR_FILE=target/*.jar
   COPY ${JAR_FILE} application.jar
   RUN java -Djarmode=layertools -jar application.jar extract

   FROM eclipse-temurin:17-jre
   WORKDIR application
   COPY --from=builder application/dependencies/ ./
   COPY --from=builder application/spring-boot-loader/ ./
   COPY --from=builder application/snapshot-dependencies/ ./
   COPY --from=builder application/application/ ./
   ENTRYPOINT ["java", "org.springframework.boot.loader.JarLauncher"]

::

   $ docker build --build-arg JAR_FILE=path/to/myapp.jar .

Production-ready Features
-------------------------

The ```spring-boot-actuator`` <https://github.com/spring-projects/spring-boot/tree/v3.1.1/spring-boot-project/spring-boot-actuator>`__ module
provides all of Spring Boot’s production-ready features.

.. code:: xml

   <dependencies>
       <dependency>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-actuator</artifactId>
       </dependency>
   </dependencies>

**Endpoints**

Actuator endpoints let you monitor and interact with your application.
Spring Boot includes a number of built-in endpoints and lets you add
your own. For example, the ``health`` endpoint provides basic
application health information.

**Monitoring and Management Over HTTP**

If you are developing a web application, Spring Boot Actuator
auto-configures all enabled endpoints to be exposed over HTTP. The
default convention is to use the ``id`` of the endpoint with a prefix
of ``/actuator`` as the URL path. For example, ``health`` is exposed
as ``/actuator/health``.

**Loggers**

-  ``TRACE``

-  ``DEBUG``

-  ``INFO``

-  ``WARN``

-  ``ERROR``

-  ``FATAL``

-  ``OFF``

-  ``null``

Deploying Spring Boot Applications
----------------------------------

 You can deploy Spring Boot applications to a variety of cloud
platforms, to virtual/real machines, or make them fully executable for
Unix systems.

**Kubernetes**

Spring Boot auto-detects Kubernetes deployment environments by checking
the environment
for ``"*_SERVICE_HOST"`` and ``"*_SERVICE_PORT"`` variables. You can
override this detection with
the ``spring.main.cloud-platform`` configuration property.

总结
----

快速刷完SpringBoot官方网站，刚开始还比较能看懂，越到后面越发现，整个内容偏向于“配置”说明，能吸收和理解的知识很少，从我做的笔记也是能看出来这点。

这跟SpringBoot本身的设计也是一致的，即SpringBoot是在Spring
Framework基础之上做的“自动配置”，从繁杂的xml配置中解脱出来，SpringBoot本身就是一个外壳。

学习SpirngBoot，需要对它的内核进行学习，也就是Spring
Framework，还好也有官方文档，虽然有点难找：

https://docs.spring.io/spring-framework/reference/overview.html

.. |image1| image:: ../wanggang.png
