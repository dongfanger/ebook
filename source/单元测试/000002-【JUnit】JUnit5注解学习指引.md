# 【JUnit】JUnit5注解学习指引
![](../wanggang.png)

注解（Annotations）是JUnit的标志性技术，本文就来对它的20个注解，以及元注解和组合注解进行学习。

## 20个注解

在`org.junit.jupiter.api`包中定义了这些注解，它们分别是：

- `@Test` 测试方法，可以直接运行。

- `@ParameterizedTest` 参数化测试，比如：

  ```java
  @ParameterizedTest
  @ValueSource(strings = { "racecar", "radar", "able was I ere I saw elba" })
  void palindromes(String candidate) {
      assertTrue(StringUtils.isPalindrome(candidate));
  }
  ```

- `@RepeatedTest` 重复测试，比如：

  ```java
  @RepeatedTest(10)
  void repeatedTest() {
      // ...
  }
  ```

- `@TestFactory` 测试工厂，专门生成测试方法，比如：

  ```java
  import org.junit.jupiter.api.DynamicTest;
  
  @TestFactory
  Collection<DynamicTest> dynamicTestsFromCollection() {
      return Arrays.asList(
          dynamicTest("1st dynamic test", () -> assertTrue(isPalindrome("madam"))),
          dynamicTest("2nd dynamic test", () -> assertEquals(4, calculator.multiply(2, 2)))
      );
  }
  ```

- `@TestTemplate` 测试模板，比如：

  ```java
  final List<String> fruits = Arrays.asList("apple", "banana", "lemon");
  
  @TestTemplate
  @ExtendWith(MyTestTemplateInvocationContextProvider.class)
  void testTemplate(String fruit) {
      assertTrue(fruits.contains(fruit));
  }
  
  public class MyTestTemplateInvocationContextProvider
          implements TestTemplateInvocationContextProvider {
  
      @Override
      public boolean supportsTestTemplate(ExtensionContext context) {
          return true;
      }
  
      @Override
      public Stream<TestTemplateInvocationContext> provideTestTemplateInvocationContexts(
              ExtensionContext context) {
  
          return Stream.of(invocationContext("apple"), invocationContext("banana"));
      }
  }
  ```

  > @TestTemplate必须注册一个TestTemplateInvocationContextProvider，它的用法跟@Test类似。

- `@TestMethodOrder` 指定测试顺序，比如：

  ```java
  import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
  import org.junit.jupiter.api.Order;
  import org.junit.jupiter.api.Test;
  import org.junit.jupiter.api.TestMethodOrder;
  
  @TestMethodOrder(OrderAnnotation.class)
  class OrderedTestsDemo {
  
      @Test
      @Order(1)
      void nullValues() {
          // perform assertions against null values
      }
  
      @Test
      @Order(2)
      void emptyValues() {
          // perform assertions against empty values
      }
  
      @Test
      @Order(3)
      void validValues() {
          // perform assertions against valid values
      }
  
  }
  ```

- `@TestInstance` 是否生成多个测试实例，默认JUnit每个测试方法生成一个实例，使用这个注解能**让每个类只生成一个实例**，比如：

  ```java
  @TestInstance(Lifecycle.PER_CLASS)
  class TestMethodDemo {
  
      @Test
      void test1() {
      }
  
      @Test
      void test2() {
      }
  
      @Test
      void test3() {
      }
  
  }
  ```

- `@DisplayName` 自定义测试名字，会体现在测试报告中，比如：

  ```java
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  
  @DisplayName("A special test case")
  class DisplayNameDemo {
  
      @Test
      @DisplayName("Custom test name containing spaces")
      void testWithDisplayNameContainingSpaces() {
      }
  
      @Test
      @DisplayName("╯°□°）╯")
      void testWithDisplayNameContainingSpecialCharacters() {
      }
  
      @Test
      @DisplayName("😱")
      void testWithDisplayNameContainingEmoji() {
      }
  
  }
  ```

- `@DisplayNameGeneration` 测试名字统一处理，比如：

  ```java
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.DisplayNameGeneration;
  import org.junit.jupiter.api.DisplayNameGenerator;
  import org.junit.jupiter.api.IndicativeSentencesGeneration;
  import org.junit.jupiter.api.Nested;
  import org.junit.jupiter.api.Test;
  import org.junit.jupiter.params.ParameterizedTest;
  import org.junit.jupiter.params.provider.ValueSource;
  
  class DisplayNameGeneratorDemo {
  
      @Nested
      @DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
      class A_year_is_not_supported {
  
          @Test
          void if_it_is_zero() {
          }
  
          @DisplayName("A negative value for year is not supported by the leap year computation.")
          @ParameterizedTest(name = "For example, year {0} is not supported.")
          @ValueSource(ints = { -1, -4 })
          void if_it_is_negative(int year) {
          }
  
      }
  
      @Nested
      @IndicativeSentencesGeneration(separator = " -> ", generator = DisplayNameGenerator.ReplaceUnderscores.class)
      class A_year_is_a_leap_year {
  
          @Test
          void if_it_is_divisible_by_4_but_not_by_100() {
          }
  
          @ParameterizedTest(name = "Year {0} is a leap year.")
          @ValueSource(ints = { 2016, 2020, 2048 })
          void if_it_is_one_of_the_following_years(int year) {
          }
  
      }
  
  }
  ```

- `@BeforeEach` 在每个`@Test`, `@RepeatedTest`, `@ParameterizedTest`, or `@TestFactory`之前执行。

- `@AfterEach` 在每个`@Test`, `@RepeatedTest`, `@ParameterizedTest`, or `@TestFactory`之后执行。

- `@BeforeAll` 在**所有的**`@Test`, `@RepeatedTest`, `@ParameterizedTest`, **and** `@TestFactory`之前执行。

- `@AfterAll` 在**所有的**`@Test`, `@RepeatedTest`, `@ParameterizedTest`, **and** `@TestFactory`之后执行。

- `@Nested` 嵌套测试，一个类套一个类，例子参考上面那个。

- `@Tag` 打标签，相当于分组，比如：

  ```java
  import org.junit.jupiter.api.Tag;
  import org.junit.jupiter.api.Test;
  
  @Tag("fast")
  @Tag("model")
  class TaggingDemo {
  
      @Test
      @Tag("taxes")
      void testingTaxCalculation() {
      }
  
  }
  ```

- `@Disabled` 禁用测试，比如：

  ```java
  import org.junit.jupiter.api.Disabled;
  import org.junit.jupiter.api.Test;
  
  @Disabled("Disabled until bug #99 has been fixed")
  class DisabledClassDemo {
  
      @Test
      void testWillBeSkipped() {
      }
  
  }
  ```

- `@Timeout` 对于test, test factory, test template, or lifecycle method，如果超时了就认为失败了，比如：

  ```java
  class TimeoutDemo {
  
      @BeforeEach
      @Timeout(5)
      void setUp() {
          // fails if execution time exceeds 5 seconds
      }
  
      @Test
      @Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
      void failsIfExecutionTimeExceeds100Milliseconds() {
          // fails if execution time exceeds 100 milliseconds
      }
  
  }
  ```

- `@ExtendWith` 注册扩展，比如：

  ```java
  @ExtendWith(RandomParametersExtension.class)
  @Test
  void test(@Random int i) {
      // ...
  }
  ```

  > JUnit5提供了标准的扩展机制来允许开发人员对JUnit5的功能进行增强。JUnit5提供了很多的标准扩展接口，第三方可以直接实现这些接口来提供自定义的行为。

- `@RegisterExtension` 通过字段注册扩展，比如：

  ```java
  class WebServerDemo {
  
      @RegisterExtension
      static WebServerExtension server = WebServerExtension.builder()
          .enableSecurity(false)
          .build();
  
      @Test
      void getProductList() {
          WebClient webClient = new WebClient();
          String serverUrl = server.getServerUrl();
          // Use WebClient to connect to web server using serverUrl and verify response
          assertEquals(200, webClient.get(serverUrl + "/products").getResponseStatus());
      }
  
  }
  ```

- `@TempDir` 临时目录，比如：

  ```java
  @Test
  void writeItemsToFile(@TempDir Path tempDir) throws IOException {
      Path file = tempDir.resolve("test.txt");
  
      new ListWriter(file).write("a", "b", "c");
  
      assertEquals(singletonList("a,b,c"), Files.readAllLines(file));
  }
  ```

## 元注解和组合注解

JUnit Jupiter支持元注解，能继承后实现自定义注解，比如自定义@Fast注解：

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.junit.jupiter.api.Tag;

@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Tag("fast")
public @interface Fast {
}
```

使用：

```java
@Fast
@Test
void myFastTest() {
    // ...
}
```

这个@Fast注解也是组合注解，甚至可以更进一步和@Test组合：

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Tag("fast")
@Test
public @interface FastTest {
}
```

只用@FastTest就可以了：

```java
@FastTest
void myFastTest() {
    // ...
}
```

## 小结

本文对JUnit20个主要的注解进行了介绍和示例演示，JUnit Jupiter支持元注解，可以自定义注解，也可以把多个注解组合起来。

> 参考资料：
>
> https://junit.org/junit5/docs/current/user-guide/#writing-tests-annotations
>
> https://vitzhou.gitbooks.io/junit5/content/junit/extension_model.html#%E6%A6%82%E8%BF%B0

