# 【JUnit】JUnit5的Tag、Filter、Order、Lifecycle
![](../wanggang.png)

## Tag

JUnit5可以使用`@Tag`注解给测试类和测试方法打tag，这些tag能用来在执行时进行过滤，它跟group有点类似。

tag应该遵循以下规则：

- 不能为null或者为空。
- 不能包含空格。
- 不能包含ISO控制字符。
- 不能包含保留字符：`,` `(` `)` `&` `|` `!`

示例代码：

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

> `@Tag`还可以通过元注解和组合注解，实现自定义注解，参考：
>
> https://dongfanger.gitee.io/blog/JUnit/002-JUnit5%E6%B3%A8%E8%A7%A3%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%BC%95.html#id2

## Filter

打好了tag后，在执行时可以进行过滤，比如Maven配置：

```xml
<!-- ... -->
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <groups>acceptance | !feature-a</groups>
                <excludedGroups>integration, regression</excludedGroups>
            </configuration>
        </plugin>
    </plugins>
</build>
<!-- ... -->
```

groups用来指定包含哪些tag，excludedGroups用来指定排除哪些tag。

## Order

JUnit5默认使用了某种算法来确定test方法的执行顺序。我们可以通过`@TestMethodOrder`进行自定义，既可以使用内置类，也可以使用实现了MethodOrderer接口的类。

内置类如下：

- DisplayName 按DisplayName的字母数字顺序
- OrderAnnotation 通过`@Order`注解指定顺序
- Random 随机顺序
- Alphanumeric 按test方法名和参数列表的字母数字顺序

示例：

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

也可以配置全局的JUnit5的默认执行顺序，比如在`src/test/resources/junit-platform.properties`中：

```
junit.jupiter.testmethod.order.default = \
    org.junit.jupiter.api.MethodOrderer$OrderAnnotation
```

## Lifecycle

JUnit5默认会在执行测试方法前给每个测试类创建一个实例对象，让测试方法相互独立，这叫做`per-method`测试实例生命周期。

> 就算测试方法被disable了也会创建实例。

如果想让每个测试类只创建一个实例对象，测试方法共用这一个实例，那么可以使用注解`@TestInstance(Lifecycle.PER_CLASS)`，这叫做`pre-class`测试实例生命周期。

`pre-class`有一些好处，比如：

- 在实例中存储变量，然后通过`@BeforeEach`或`@AfterEach`修改。
- `@BeforeAll`、`@AfterAll`可以作用于非静态方法和接口`default`方法。
- `@BeforeAll`、`@AfterAll`可以作用于`@Nested`嵌套测试类。

有两种方式可以设置全局的生命周期模式，第一种是JVM启动参数：

```
-Djunit.jupiter.testinstance.lifecycle.default=per_class
```

第二种方式是配置文件，比如`src/test/resources/junit-platform.properties`：

```
junit.jupiter.testinstance.lifecycle.default = per_class
```

> 如果要进行全局配置，建议使用配置文件，这样在出现问题时方便进行追溯。

## 小结

本文首先介绍了给测试类和测试方法打tag进行分组，然后可以在运行时根据tag进行过滤，接着介绍了如何制定测试方法的执行顺序，最后介绍了两种生命周期：`per-method`和`pre-class`。

> 参考资料：
>
> https://junit.org/junit5/docs/current/user-guide/#writing-tests-tagging-and-filtering
>
> https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-execution-order
>
> https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-instance-lifecycle