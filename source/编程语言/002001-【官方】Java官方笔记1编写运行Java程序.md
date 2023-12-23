# 【官方】Java官方笔记1编写运行Java程序
![](../wanggang.png)

你可能已经迫不及待想安装Java，写个Java程序跑起来了。但是在这之前，有些概念需要提前了解，因为Java跟C、C++和Python都有点不一样。

#### 编译和执行

我们在文本文件中编写英文代码，这些英文计算机是看不懂的，因此需要做一下转换，转换为计算机能识别和运行的格式，这个转换，是由**编译器**来完成的。有些语言没有编译器，但是Java是有的。

编译器转换后的文件，通常叫做二进制文件，或者可执行文件。文件内容从英文变成了字节码。字节码只有计算机能看懂，人是看不懂的，我们也不用关心，只需要保证我们编写的英文代码，能正确通过编译即可。执行的事，就交给计算机来做。

Java代码文件以`.java`结尾，Java可执行文件以`.class`结尾。

#### 创建Java类

Java文件里面的所有代码，都必须放在**Java Class**里面：

```java
public class MyFirstClass {
}
```

文件名必须叫做`MyFirstClass.java`，文件名跟类名必须保持一致。为什么Java要设计得这么严格呢？方便，让你看到文件名，就能知道类名是啥，不用去猜。

#### 安装JDK

如何编译类文件呢？下载Java。

下载Java，就是下载JDK，Java Development Kit，里面包含了Java编译器，将`MyFirstClass.java` 编译为`MyFirstClass.class`。

所谓的JRE，Java Runtime Environment，它是JDK的一部分，只能用来运行Java程序，不能用来编译。

下载地址： https://jdk.java.net/

安装后需要根据操作系统（Windows、Linux、macOS）设置环境变量JAVA_HOME和PATH。

验证安装成功：

```
java -version
```

#### 编译Class

使用`javac`命令编译：

```
javac MyFirstClass.java
```

如果代码有问题，会出现报错。如果没问题，就会生成`MyFirstClass.class`文件。

#### 运行HelloWorld

添加代码：

```java
public class MyFirstClass {

    public static void main(String... args) {
        System.out.println("Hello, World!");
    }
}
```

重新编译，确保生成了class文件，使用`java`命令运行：

```
java MyFirstClass
```

运行成功，控制台会打印一句：Hello, World!

#### 常见问题

问题1：javac HelloWorldApp，报错：

```
Class names, 'HelloWorldApp', are only accepted if annotation processing is explicitly requested
```

`javac HelloWorldApp.java` 编译命令**javac**后面应该跟**文件名**。

问题2：java HelloWorldApp.class，报错：

```
Could not find or load main class HelloWorldApp.class
```

`java HelloWorldApp` 运行命令**java**后面应该跟**类名**。

可以命令Help看到区别：

```
javac Usage: javac <options> <source files>
```

```
java Usage: java [-options] class [args...]
           (to execute a class)
   or  java [-options] -jar jarfile [args...]
           (to execute a jar file)
```

在复杂应用开发时，并不会直接使用javac和java命令，而是使用IDE，Integrated Development Environment，集成开发环境，比如Eclipse、NetBeans和IntelliJ IDEA。

> 参考资料：
>
> Getting Started with Java https://dev.java/learn/getting-started