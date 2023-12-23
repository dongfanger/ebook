【Spring】SpringBoot官方笔记7IO
===============================

|image1|

Caching
-------

Spring Boot auto-configures the cache infrastructure as long as caching
support is enabled by using the ``@EnableCaching`` annotation.

.. code:: java

   import org.springframework.cache.annotation.Cacheable;
   import org.springframework.stereotype.Component;

   @Component
   public class MyMathService {

       @Cacheable("piDecimals")
       public int computePiDecimal(int precision) {
           ...
       }

   }

Before invoking ``computePiDecimal``, the abstraction looks for an entry
in the ``piDecimals`` cache that matches the ``i`` argument. If an entry
is found, the content in the cache is immediately returned to the
caller, and the method is not invoked. Otherwise, the method is invoked,
and the cache is updated before returning the value.

Redis
-----

If `Redis <https://redis.io/>`__ is available and configured,
a ``RedisCacheManager`` is auto-configured.

::

   spring.cache.cache-names=cache1,cache2
   spring.cache.redis.time-to-live=10m

.. code:: java

   import java.time.Duration;

   import org.springframework.boot.autoconfigure.cache.RedisCacheManagerBuilderCustomizer;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.data.redis.cache.RedisCacheConfiguration;

   @Configuration(proxyBeanMethods = false)
   public class MyRedisCacheManagerConfiguration {

       @Bean
       public RedisCacheManagerBuilderCustomizer myRedisCacheManagerBuilderCustomizer() {
           return (builder) -> builder
                   .withCacheConfiguration("cache1", RedisCacheConfiguration
                           .defaultCacheConfig().entryTtl(Duration.ofSeconds(10)))
                   .withCacheConfiguration("cache2", RedisCacheConfiguration
                           .defaultCacheConfig().entryTtl(Duration.ofMinutes(1)));

       }

   }

If you need to disable caching altogether in certain environments, force
the cache type to ``none`` to use a no-op implementation, as shown in
the following example:

::

   spring.cache.type=none

Sending Email
-------------

The Spring Framework provides an abstraction for sending email by using
the ``JavaMailSender`` interface, and Spring Boot provides
auto-configuration for it as well as a starter module.

::

   spring.mail.properties[mail.smtp.connectiontimeout]=5000
   spring.mail.properties[mail.smtp.timeout]=3000
   spring.mail.properties[mail.smtp.writetimeout]=5000

Web Services
------------

::

   spring.webservices.wsdl-locations=classpath:/wsdl

..

   参考资料：

   https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#io

.. |image1| image:: ../wanggang.png
