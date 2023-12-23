【Spring】SpringBoot官方笔记5Data
=================================

|image1|

Spring Boot integrates with a number of data technologies, both SQL and
NoSQL.

SQL Databases
-------------

 `Spring Data <https://spring.io/projects/spring-data>`__ provides an
additional level of functionality:
creating ``Repository`` implementations directly from interfaces and
using conventions to generate queries from your method names.

The ``spring-boot-starter-data-jpa`` POM provides a quick way to get
started. It provides the following key dependencies:

-  Hibernate: One of the most popular JPA implementations.

-  Spring Data JPA: Helps you to implement JPA-based repositories.

-  Spring ORM: Core ORM support from the Spring Framework.

A typical entity class resembles the following example:

.. code:: java

   import java.io.Serializable;

   import jakarta.persistence.Column;
   import jakarta.persistence.Entity;
   import jakarta.persistence.GeneratedValue;
   import jakarta.persistence.Id;

   @Entity
   public class City implements Serializable {

       @Id
       @GeneratedValue
       private Long id;

       @Column(nullable = false)
       private String name;

       @Column(nullable = false)
       private String state;

       // ... additional members, often include @OneToMany mappings

       protected City() {
           // no-args constructor required by JPA spec
           // this one is protected since it should not be used directly
       }

       public City(String name, String state) {
           this.name = name;
           this.state = state;
       }

       public String getName() {
           return this.name;
       }

       public String getState() {
           return this.state;
       }

       // ... etc

   }

Working with NoSQL Technologies
-------------------------------

**Redis**

`Redis <https://redis.io/>`__ is a cache, message broker, and
richly-featured key-value store. Spring Boot offers basic
auto-configuration for
the `Lettuce <https://github.com/lettuce-io/lettuce-core/>`__\ and `Jedis <https://github.com/xetorthio/jedis/>`__ client
libraries and the abstractions on top of them provided by `Spring Data
Redis <https://github.com/spring-projects/spring-data-redis>`__.

By default, the instance tries to connect to a Redis server
at ``localhost:6379``.

::

   spring.data.redis.host=localhost
   spring.data.redis.port=6379
   spring.data.redis.database=0
   spring.data.redis.username=user
   spring.data.redis.password=secret

**MongoDB**

The auto-configured ``MongoClient`` is created using
a ``MongoClientSettings`` bean.

::

   spring.data.mongodb.host=mongoserver1.example.com
   spring.data.mongodb.port=27017
   spring.data.mongodb.additional-hosts[0]=mongoserver2.example.com:23456
   spring.data.mongodb.database=test
   spring.data.mongodb.username=user
   spring.data.mongodb.password=secret

**Elasticsearch**

Spring Boot supports several clients:

-  The official low-level REST client

-  The official Java API client

-  The ``ReactiveElasticsearchClient`` provided by Spring Data
   Elasticsearch

::

   spring.elasticsearch.uris=https://search.example.com:9200
   spring.elasticsearch.socket-timeout=10s
   spring.elasticsearch.username=user
   spring.elasticsearch.password=secret

**InfluxDB**

`InfluxDB <https://www.influxdata.com/>`__ is an open-source time series
database optimized for fast, high-availability storage and retrieval of
time series data in fields such as operations monitoring, application
metrics, Internet-of-Things sensor data, and real-time analytics.

::

   spring.influx.url=https://172.0.0.1:8086

..

   参考资料：

   https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#data

.. |image1| image:: ../wanggang.png
