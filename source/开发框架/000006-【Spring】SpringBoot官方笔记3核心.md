# 【Spring】SpringBoot官方笔记3核心
![](../wanggang.png)

## SpringApplication

By default, `INFO` logging messages are shown, including some relevant startup details, such as the user that launched the application.

**Lazy Initialization**

When lazy initialization is enabled, beans are created as they are needed rather than during application startup.

```
spring.main.lazy-initialization=true
```

`@Lazy(false)` annotation：disable lazy initialization for certain beans

**Customizing the Banner**

adding a `banner.txt` file to your classpath or by setting the `spring.banner.location` property to the location of such a file. If the file has an encoding other than UTF-8, you can set `spring.banner.charset`.

`SpringApplication.setBanner(…​)` method

`spring.main.banner-mode` property `System.out`(`console`)、logger (`log`)、not produced at all (`off`)

The printed banner is registered as a singleton bean under the following name: `springBootBanner`.

**Customizing SpringApplication**

```java
import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyApplication {

    public static void main(String[] args) {
        SpringApplication application = new SpringApplication(MyApplication.class);
        application.setBannerMode(Banner.Mode.OFF);
        application.run(args);
    }

}
```

The internal state of Spring Boot applications is mostly represented by the Spring `ApplicationContext`.

Internally, Spring Boot uses events to handle a variety of tasks. **Application events** are sent in the following order, as your application runs:

1. An `ApplicationStartingEvent` is sent at the start of a run but before any processing, except for the registration of listeners and initializers.

2. An `ApplicationEnvironmentPreparedEvent` is sent when the `Environment` to be used in the context is known but before the context is created.

3. An `ApplicationContextInitializedEvent` is sent when the `ApplicationContext` is prepared and ApplicationContextInitializers have been called but before any bean definitions are loaded.

4. An `ApplicationPreparedEvent` is sent just before the refresh is started but after bean definitions have been loaded.

5. An `ApplicationStartedEvent` is sent after the context has been refreshed but before any application and command-line runners have been called.

6. An `AvailabilityChangeEvent` is sent right after with `LivenessState.CORRECT` to indicate that the application is considered as live.

7. An `ApplicationReadyEvent` is sent after any [application and command-line runners](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.spring-application.command-line-runner) have been called.

8. An `AvailabilityChangeEvent` is sent right after with `ReadinessState.ACCEPTING_TRAFFIC` to indicate that the application is ready to service requests.

9. An `ApplicationFailedEvent` is sent if there is an exception on startup.

**Accessing Application Arguments**

```java
import java.util.List;

import org.springframework.boot.ApplicationArguments;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

    public MyBean(ApplicationArguments args) {
        boolean debug = args.containsOption("debug");
        List<String> files = args.getNonOptionArgs();
        if (debug) {
            System.out.println(files);
        }
        // if run with "--debug logfile.txt" prints ["logfile.txt"]
    }

}
```

If you need to run some specific code once the `SpringApplication` has started, you can implement the `ApplicationRunner` or `CommandLineRunner` interfaces.

```java
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class MyCommandLineRunner implements CommandLineRunner {

    @Override
    public void run(String... args) {
        // Do something...
    }

}
```

**Application Exit**

Each `SpringApplication` registers a shutdown hook with the JVM to ensure that the `ApplicationContext` closes gracefully on exit.

## Externalized Configuration

Sources are considered in the following order:

1. Default properties (specified by setting `SpringApplication.setDefaultProperties`).

2. [`@PropertySource`](https://docs.spring.io/spring-framework/docs/6.0.10/javadoc-api/org/springframework/context/annotation/PropertySource.html) annotations on your `@Configuration` classes. Please note that such property sources are not added to the `Environment` until the application context is being refreshed. This is too late to configure certain properties such as `logging.*` and `spring.main.*` which are read before refresh begins.

3. Config data (such as `application.properties` files).

4. A `RandomValuePropertySource` that has properties only in `random.*`.

5. OS environment variables.

6. Java System properties (`System.getProperties()`).

7. JNDI attributes from `java:comp/env`.

8. `ServletContext` init parameters.

9. `ServletConfig` init parameters.

10. Properties from `SPRING_APPLICATION_JSON` (inline JSON embedded in an environment variable or system property).

11. Command line arguments.

12. `properties` attribute on your tests. Available on [`@SpringBootTest`](https://docs.spring.io/spring-boot/docs/3.1.1/api/org/springframework/boot/test/context/SpringBootTest.html) and the [test annotations for testing a particular slice of your application](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.testing.spring-boot-applications.autoconfigured-tests).

13. [`@DynamicPropertySource`](https://docs.spring.io/spring-framework/docs/6.0.10/javadoc-api/org/springframework/test/context/DynamicPropertySource.html) annotations in your tests.

14. [`@TestPropertySource`](https://docs.spring.io/spring-framework/docs/6.0.10/javadoc-api/org/springframework/test/context/TestPropertySource.html) annotations on your tests.

15. [Devtools global settings properties](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using.devtools.globalsettings) in the `$HOME/.config/spring-boot` directory when devtools is active.

Config data files are considered in the following order:

1. [Application properties](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.files) packaged inside your jar (`application.properties` and YAML variants).

2. [Profile-specific application properties](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.files.profile-specific) packaged inside your jar (`application-{profile}.properties` and YAML variants).

3. [Application properties](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.files) outside of your packaged jar (`application.properties` and YAML variants).

4. [Profile-specific application properties](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.files.profile-specific) outside of your packaged jar (`application-{profile}.properties` and YAML variants).

**If you have configuration files with both `.properties`and YAML format in the same location, `.properties` takes precedence.**

读取配置：

Property values can be injected directly into your beans by using the `@Value` annotation, accessed through Spring’s `Environment`abstraction, or be [bound to structured objects](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.typesafe-configuration-properties) through `@ConfigurationProperties`.

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

    @Value("${name}")
    private String name;

    // ...

}
```

**command line properties (that is, arguments starting with `--`, such as `--server.port=9000`) always take precedence over file-based property sources.**

Spring Boot will automatically find and load `application.properties` and `application.yaml` files from the following locations when your application starts:

1. From the classpath
   
   1. The classpath root
   
   2. The classpath `/config` package

2. From the current directory
   
   1. The current directory
   
   2. The `config/` subdirectory in the current directory
   
   3. Immediate child directories of the `config/` subdirectory

**Wildcard locations only work with external directories. You cannot use a wildcard in a classpath: location.**

**Profile Specific Files**

`application-{profile}`. For example, if your application activates a profile named `prod` and uses YAML files, then both `application.yaml` and `application-prod.yaml` will be considered.

configtree：

```
etc/
  config/
    myapp/
      username
      password
```

```
spring.config.import=optional:configtree:/etc/config/
```

You can then access or inject `myapp.username` and `myapp.password` properties from the `Environment` in the usual way.

**Property placeholders** can also specify a default value using a `:` to separate the default value from the property name, for example `${name:default}`.

```
app.name=MyApp
app.description=${app.name} is a Spring Boot application written by ${username:Unknown}
```

**Working With YAML**

If you use “Starters”, SnakeYAML is automatically provided by `spring-boot-starter`.

> YAML files cannot be loaded by using the `@PropertySource` or `@TestPropertySource` annotations. So, in the case that you need to load values that way, you need to use a properties file.

The `YamlPropertiesFactoryBean`loads YAML as `Properties` and the `YamlMapFactoryBean` loads YAML as a `Map`. `YamlPropertySourceLoader` class if you want to load YAML as a Spring `PropertySource`.

**Configuring Random Values**

RandomValuePropertySource

```
my.secret=${random.value}
my.number=${random.int}
my.bignumber=${random.long}
my.uuid=${random.uuid}
my.number-less-than-ten=${random.int(10)}
my.number-in-range=${random.int[1024,65536]}
```

**Type-safe Configuration Properties**

@ConfigurationProperties

**Relaxed Binding**

As an example, consider the following `@ConfigurationProperties` class:

```java
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "my.main-project.person")
public class MyPersonProperties {

    private String firstName;

    public String getFirstName() {
        return this.firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

}
```

With the preceding code, the following properties names can all be used:

-  `my.main-project.person.first-name` Kebab case, which is recommended for use in `.properties` and YAML files. 

-  `my.main-project.person.firstName` Standard camel case syntax. 

- `my.main-project.person.first_name`  Underscore notation, which is an alternative format for use in `.properties` and YAML files. 

- `MY_MAINPROJECT_PERSON_FIRSTNAME`  Upper case format, which is recommended when using system environment variables. 

We recommend that, when possible, properties are stored in lower-case kebab format, such as my.person.first-name=Rod.

## Profiles

make it be available only in certain environments

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration(proxyBeanMethods = false)
@Profile("production")
public class ProductionConfiguration {

    // ...

}
```

## Logging

By default, if you use the “Starters”, Logback is used for logging.

**Log Format**

```
2023-06-22T12:08:05.861Z  INFO 22768 --- [           main] o.s.b.d.f.s.MyApplication                : Starting MyApplication using Java 17.0.7 with PID 22768 (/opt/apps/myapp.jar started by myuser in /opt/apps/)
2023-06-22T12:08:05.872Z  INFO 22768 --- [           main] o.s.b.d.f.s.MyApplication                : No active profile set, falling back to 1 default profile: "default"
2023-06-22T12:08:09.854Z  INFO 22768 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2023-06-22T12:08:09.892Z  INFO 22768 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2023-06-22T12:08:09.892Z  INFO 22768 --- [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.10]
2023-06-22T12:08:10.160Z  INFO 22768 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2023-06-22T12:08:10.162Z  INFO 22768 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 4038 ms
2023-06-22T12:08:11.512Z  INFO 22768 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2023-06-22T12:08:11.534Z  INFO 22768 --- [           main] o.s.b.d.f.s.MyApplication                : Started MyApplication in 7.251 seconds (process running for 8.584)
```

- Date and Time: Millisecond precision and easily sortable.

- Log Level: `ERROR`, `WARN`, `INFO`, `DEBUG`, or `TRACE`.

- Process ID.

- A `---` separator to distinguish the start of actual log messages.

- Thread name: Enclosed in square brackets (may be truncated for console output).

- Logger name: This is usually the source class name (often abbreviated).

- The log message.

## Internationalization

```
spring.messages.basename=messages,config.i18n.messages
spring.messages.fallback-to-system-locale=false
```

## JSON

Jackson is the preferred and default library. Auto-configuration for Jackson is provided and Jackson is part of `spring-boot-starter-json`.

@JsonComponent Custom Serializers and Deserializers

```java
import java.io.IOException;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.ObjectCodec;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import org.springframework.boot.jackson.JsonComponent;

@JsonComponent
public class MyJsonComponent {

    public static class Serializer extends JsonSerializer<MyObject> {

        @Override
        public void serialize(MyObject value, JsonGenerator jgen, SerializerProvider serializers) throws IOException {
            jgen.writeStartObject();
            jgen.writeStringField("name", value.getName());
            jgen.writeNumberField("age", value.getAge());
            jgen.writeEndObject();
        }

    }

    public static class Deserializer extends JsonDeserializer<MyObject> {

        @Override
        public MyObject deserialize(JsonParser jsonParser, DeserializationContext ctxt) throws IOException {
            ObjectCodec codec = jsonParser.getCodec();
            JsonNode tree = codec.readTree(jsonParser);
            String name = tree.get("name").textValue();
            int age = tree.get("age").intValue();
            return new MyObject(name, age);
        }

    }

}
```

## Task Execution and Scheduling

In the absence of an `Executor` bean in the context, Spring Boot auto-configures a `ThreadPoolTaskExecutor` with sensible defaults that can be automatically associated to asynchronous task execution (`@EnableAsync`) and Spring MVC asynchronous request processing.

A `ThreadPoolTaskScheduler` can also be auto-configured if need to be associated to scheduled task execution (using `@EnableScheduling` for instance).

## Testing

Most developers use the `spring-boot-starter-test` “Starter”, which imports both Spring Boot test modules as well as JUnit Jupiter, AssertJ, Hamcrest, and a number of other useful libraries.

- [JUnit 5](https://junit.org/junit5/): The de-facto standard for unit testing Java applications.

- [Spring Test](https://docs.spring.io/spring-framework/docs/6.0.10/reference/html/testing.html#integration-testing) & Spring Boot Test: Utilities and integration test support for Spring Boot applications.

- [AssertJ](https://assertj.github.io/doc/): A fluent assertion library.

- [Hamcrest](https://github.com/hamcrest/JavaHamcrest): A library of matcher objects (also known as constraints or predicates).

- [Mockito](https://site.mockito.org/): A Java mocking framework.

- [JSONassert](https://github.com/skyscreamer/JSONassert): An assertion library for JSON.

- [JsonPath](https://github.com/jayway/JsonPath): XPath for JSON.

**One of the major advantages of dependency injection is that it should make your code easier to unit test.** You can instantiate objects by using the `new` operator without even involving Spring. You can also use *mock objects* instead of real dependencies.

By default, `@SpringBootTest` will not start a server. You can use the `webEnvironment` attribute of `@SpringBootTest` to further refine how your tests run:

- `MOCK`(Default) : Loads a web `ApplicationContext` and provides a mock web environment. Embedded servers are not started when using this annotation. If a web environment is not available on your classpath, this mode transparently falls back to creating a regular non-web `ApplicationContext`. It can be used in conjunction with [`@AutoConfigureMockMvc` or `@AutoConfigureWebTestClient`](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.testing.spring-boot-applications.with-mock-environment) for mock-based testing of your web application.

- `RANDOM_PORT`: Loads a `WebServerApplicationContext` and provides a real web environment. Embedded servers are started and listen on a random port.

- `DEFINED_PORT`: Loads a `WebServerApplicationContext` and provides a real web environment. Embedded servers are started and listen on a defined port (from your `application.properties`) or on the default port of `8080`.

- `NONE`: Loads an `ApplicationContext` by using `SpringApplication` but does not provide *any* web environment (mock or otherwise).

## Docker Compose Support

A `compose.yml` file is typically created next to your application which defines and configures service containers.

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-docker-compose</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## Creating Your Own Auto-configuration

Classes that implement auto-configuration are annotated with `@AutoConfiguration`.

## SSL

```
spring.ssl.bundle.jks.mybundle.key.alias=application
spring.ssl.bundle.jks.mybundle.keystore.location=classpath:application.p12
spring.ssl.bundle.jks.mybundle.keystore.password=secret
spring.ssl.bundle.jks.mybundle.keystore.type=PKCS12
```



> 参考资料：
> 
> https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features
