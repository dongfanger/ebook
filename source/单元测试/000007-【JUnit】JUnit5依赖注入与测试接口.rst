【JUnit】JUnit5依赖注入与测试接口
=================================

|image1|

依赖注入
--------

以前的JUnit的类构造方法和测试方法都是不能有参数的，\ **JUnit
Jupiter有一个颠覆性的改进，就是允许它们有入参，这样就能做依赖注入了。**

   如果你对pytest的fixture有了解的话，就知道这个技术是多么的强大。

ParameterResolver是一个接口类，类构造方法和测试方法在运行时，必须由被注册的ParameterResolver进行解析。JUnit
Jupiter有三个自动注册的内置解析器：

-  TestInfoParameterResolver 参数类型为TestInfo
-  RepetitionInfoParameterResolver 参数类型为RepetitionInfo
-  TestReporterParameterResolver 参数类型为TestReporter

**TestInfo**

TestInfo包含the display name, the test class, the test method, and
associated tags等信息。

示例：

.. code:: java

   import static org.junit.jupiter.api.Assertions.assertEquals;
   import static org.junit.jupiter.api.Assertions.assertTrue;

   import org.junit.jupiter.api.BeforeEach;
   import org.junit.jupiter.api.DisplayName;
   import org.junit.jupiter.api.Tag;
   import org.junit.jupiter.api.Test;
   import org.junit.jupiter.api.TestInfo;

   @DisplayName("TestInfo Demo")
   class TestInfoDemo {

       TestInfoDemo(TestInfo testInfo) {
           assertEquals("TestInfo Demo", testInfo.getDisplayName());
       }

       @BeforeEach
       void init(TestInfo testInfo) {
           String displayName = testInfo.getDisplayName();
           assertTrue(displayName.equals("TEST 1") || displayName.equals("test2()"));
       }

       @Test
       @DisplayName("TEST 1")
       @Tag("my-tag")
       void test1(TestInfo testInfo) {
           assertEquals("TEST 1", testInfo.getDisplayName());
           assertTrue(testInfo.getTags().contains("my-tag"));
       }

       @Test
       void test2() {
       }

   }

**RepetitionInfo**

主要是\ ``@RepeatedTest``\ 会用到，包含当前重复以及总重复次数等信息。

**TestReporter**

TestReporter能用来输出额外的信息。

示例：

.. code:: java

   class TestReporterDemo {

       @Test
       void reportSingleValue(TestReporter testReporter) {
           testReporter.publishEntry("a status message");
       }

       @Test
       void reportKeyValuePair(TestReporter testReporter) {
           testReporter.publishEntry("a key", "a value");
       }

       @Test
       void reportMultipleKeyValuePairs(TestReporter testReporter) {
           Map<String, String> values = new HashMap<>();
           values.put("user name", "dk38");
           values.put("award year", "1974");

           testReporter.publishEntry(values);
       }

   }

**传自定义参数**

除了内置解析器，如果想传自定义参数，那么需要使用\ ``@ExtendWith``\ 注册扩展，比如：

.. code:: java

   @ExtendWith(RandomParametersExtension.class)
   class MyRandomParametersTest {

       @Test
       void injectsInteger(@Random int i, @Random int j) {
           assertNotEquals(i, j);
       }

       @Test
       void injectsDouble(@Random double d) {
           assertEquals(0.0, d, 1.0);
       }

   }

有点插件的意思，更常见的是\ `MockitoExtension <https://github.com/mockito/mockito/blob/release/2.x/subprojects/junit-jupiter/src/main/java/org/mockito/junit/jupiter/MockitoExtension.java>`__\ 和\ `SpringExtension <https://github.com/spring-projects/spring-framework/tree/HEAD/spring-test/src/main/java/org/springframework/test/context/junit/jupiter/SpringExtension.java>`__\ 。

测试接口
--------

JUnit Jupiter除了测试类和测试方法，其实也有测试接口，比如：

.. code:: java

   @TestInstance(Lifecycle.PER_CLASS)
   interface TestLifecycleLogger {

       static final Logger logger = Logger.getLogger(TestLifecycleLogger.class.getName());

       @BeforeAll
       default void beforeAllTests() {
           logger.info("Before all tests");
       }

       @AfterAll
       default void afterAllTests() {
           logger.info("After all tests");
       }

       @BeforeEach
       default void beforeEachTest(TestInfo testInfo) {
           logger.info(() -> String.format("About to execute [%s]",
               testInfo.getDisplayName()));
       }

       @AfterEach
       default void afterEachTest(TestInfo testInfo) {
           logger.info(() -> String.format("Finished executing [%s]",
               testInfo.getDisplayName()));
       }

   }

.. code:: java

   interface TestInterfaceDynamicTestsDemo {

       @TestFactory
       default Stream<DynamicTest> dynamicTestsForPalindromes() {
           return Stream.of("racecar", "radar", "mom", "dad")
               .map(text -> dynamicTest(text, () -> assertTrue(isPalindrome(text))));
       }

   }

``@Test``, ``@RepeatedTest``, ``@ParameterizedTest``, ``@TestFactory``,
``@TestTemplate``, ``@BeforeEach``, and
``@AfterEach``\ 能作用到接口的\ ``default``\ 方法上。

   ``default``\ 方法是接口已经实现好了的方法，接口的实现类不需要再编写实现代码，就能直接使用。

如果测试类是\ ``@TestInstance(Lifecycle.PER_CLASS)``\ 注解，那么可以使用\ ``@BeforeAll``
and ``@AfterAll``\ 。

**测试接口可以作为模版**\ 。如果测试接口有\ ``@ExtendWith`` and
``@Tag``\ 注解，那么它的实现类也会继承tags and extensions。比如：

.. code:: java

   @Tag("timed")
   @ExtendWith(TimingExtension.class)
   interface TimeExecutionLogger {
   }

.. code:: java

   class TestInterfaceDemo implements TestLifecycleLogger,
           TimeExecutionLogger, TestInterfaceDynamicTestsDemo {

       @Test
       void isEqualValue() {
           assertEquals(1, "a".length(), "is always equal");
       }

   }

结果：

::

   INFO  example.TestLifecycleLogger - Before all tests
   INFO  example.TestLifecycleLogger - About to execute [dynamicTestsForPalindromes()]
   INFO  example.TimingExtension - Method [dynamicTestsForPalindromes] took 19 ms.
   INFO  example.TestLifecycleLogger - Finished executing [dynamicTestsForPalindromes()]
   INFO  example.TestLifecycleLogger - About to execute [isEqualValue()]
   INFO  example.TimingExtension - Method [isEqualValue] took 1 ms.
   INFO  example.TestLifecycleLogger - Finished executing [isEqualValue()]
   INFO  example.TestLifecycleLogger - After all tests

**测试接口也可以作为契约。**\ 比如：

.. code:: java

   public interface Testable<T> {

       T createValue();

   }

.. code:: java

   public interface EqualsContract<T> extends Testable<T> {

       T createNotEqualValue();

       @Test
       default void valueEqualsItself() {
           T value = createValue();
           assertEquals(value, value);
       }

       @Test
       default void valueDoesNotEqualNull() {
           T value = createValue();
           assertFalse(value.equals(null));
       }

       @Test
       default void valueDoesNotEqualDifferentValue() {
           T value = createValue();
           T differentValue = createNotEqualValue();
           assertNotEquals(value, differentValue);
           assertNotEquals(differentValue, value);
       }

   }

.. code:: java

   public interface ComparableContract<T extends Comparable<T>> extends Testable<T> {

       T createSmallerValue();

       @Test
       default void returnsZeroWhenComparedToItself() {
           T value = createValue();
           assertEquals(0, value.compareTo(value));
       }

       @Test
       default void returnsPositiveNumberWhenComparedToSmallerValue() {
           T value = createValue();
           T smallerValue = createSmallerValue();
           assertTrue(value.compareTo(smallerValue) > 0);
       }

       @Test
       default void returnsNegativeNumberWhenComparedToLargerValue() {
           T value = createValue();
           T smallerValue = createSmallerValue();
           assertTrue(smallerValue.compareTo(value) < 0);
       }

   }

实现类：

.. code:: java

   class StringTests implements ComparableContract<String>, EqualsContract<String> {

       @Override
       public String createValue() {
           return "banana";
       }

       @Override
       public String createSmallerValue() {
           return "apple"; // 'a' < 'b' in "banana"
       }

       @Override
       public String createNotEqualValue() {
           return "cherry";
       }

   }

小结
----

本文先介绍了JUnit
Jupiter的颠覆性技术，允许传参以实现依赖注入，然后介绍了除了测试类和测试方法以外的测试接口，它既可以作为测试模板，也可以作为测试契约。

   参考资料：

   https://junit.org/junit5/docs/current/user-guide/#writing-tests-dependency-injection

   https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-interfaces-and-default-methods

   https://blog.csdn.net/qq_35387940/article/details/104767746

.. |image1| image:: ../wanggang.png
