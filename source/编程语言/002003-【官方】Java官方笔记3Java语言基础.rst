【官方】Java官方笔记3Java语言基础
=================================

|image1|

变量
^^^^

**Instance Variables (Non-Static Fields)** 实例变量（非静态变量）

一个类可以创造多个实例，实例中的变量叫做实例变量，相互独立。

**Class Variables (Static Fields)** 类变量（静态变量）

对比来看，类变量就是类的变量，一个类只能有一份，不能复制，使用\ ``static``\ 关键字来定义类变量。

代码：

.. code:: java

   public class MyVar {
       static int classVar = 1;  // 类变量（静态变量）
       int instanceVar = 2;  // 实例变量
   }

..

   对比Python来看就很清楚：

   .. code:: python

      class MyVar:
      class_var = 1

      def __int__(self):
        instance_var = 2

**Local Variables** 局部变量

局部变量是由代码位置决定的，前面的实例变量和类变量，是放到Field位置，而局部变量是放到Method里面。也就是说，局部变量是放在方法的花括号里面的变量，并且只能在方法内部访问，不能被其他地方访问，这就是所谓的局部。

.. code:: java

   public class MyVar {
       static int classVar = 1;  // 类变量（静态变量）
       int instanceVar = 2;  // 实例变量

       void method() {
           int localVar = 3;  // 局部变量
       }
   }

**Parameters** 参数

参数就是方法名后面小括号里面的变量。

.. code:: java

   public class MyVar {
       static int classVar = 1;  // 类变量（静态变量）
       int instanceVar = 2;  // 实例变量

       void method(int parameter) {  // 参数
           int localVar = 3;  // 局部变量
       }
   }

**变量命名规则**

驼峰命名法，可参考阿里规范： https://github.com/alibaba/p3c

基本数据类型
^^^^^^^^^^^^

Java有\ **8**\ 个基本数据类型：byte、short、int、long、float、double、boolean、char。

   对比Python的\ **6**\ 个基本数据类型：Number（数字）、String（字符串）、List（列表）、Tuple（元组）、Set（集合）、Dictionary（字典），你发现了什么吗？

Java的String严格来说不算基本数据类型，因为它其实是一个类，\ ``java.lang.String``\ 。

**默认值**

只声明不赋值的字段（\ **定义在类级别的field**\ ），编译器会给它赋予默认值：

-  byte：0

-  short：0

-  int：0

-  long：0L

-  float：0.0f

-  double：0.0d

-  boolean：false

-  char：\ ``\u0000``

String或任何对象，会赋值为null。

而对于局部变量（\ **定义在方法里面的variable**\ ），编译器不会自动赋值，只声明不赋值，会报编译错误。

   类的field会赋默认值。方法的局部variable不会。

**字面量Literals**

基本数据类型的初始化可以不使用new，而直接使用字面量：

.. code:: java

   byte b = 100;
   short s = 10000;
   int i = 100000;
   int hexadecimalValue = 0x1a;  // 十六进制
   int binaryValue = 0b11010;  // 二进制
   long x = 10000000L;
   float f1  = 123.4f;
   double d1 = 123.4;
   double d2 = 1.234e2;  // 科学计数法
   boolean result = true;
   char capitalC = 'C';

String也不需要new就能初始化：

.. code:: java

   String s = "this is a string";

另外还有一个字面量\ ``.class``\ ，比如\ ``String.class``\ ，用来表示自己的类型。

数组
^^^^

An *array* is a container object that holds a fixed number of values of
a single type.

注意这里说的是\ **container
object**\ ，数组不是基本数据类型，而是容器对象。这一点也可以从数组初始化来论证，数组初始化是需要new的：

.. code:: java

   int[] anArray;
   anArray = new int[10];

代码示例：

.. code:: java

   class ArrayDemo {
       public static void main(String[] args) {
           // declares an array of integers
           int[] anArray;

           // allocates memory for 10 integers
           anArray = new int[10];

           // initialize first element
           anArray[0] = 100;
           // initialize second element
           anArray[1] = 200;
           // and so forth
           anArray[2] = 300;
           anArray[3] = 400;
           anArray[4] = 500;
           anArray[5] = 600;
           anArray[6] = 700;
           anArray[7] = 800;
           anArray[8] = 900;
           anArray[9] = 1000;

           System.out.println("Element at index 0: "
                              + anArray[0]);
           System.out.println("Element at index 1: "
                              + anArray[1]);
           System.out.println("Element at index 2: "
                              + anArray[2]);
           System.out.println("Element at index 3: "
                              + anArray[3]);
           System.out.println("Element at index 4: "
                              + anArray[4]);
           System.out.println("Element at index 5: "
                              + anArray[5]);
           System.out.println("Element at index 6: "
                              + anArray[6]);
           System.out.println("Element at index 7: "
                              + anArray[7]);
           System.out.println("Element at index 8: "
                              + anArray[8]);
           System.out.println("Element at index 9: "
                              + anArray[9]);
       }
   }

多维数组：

.. code:: java

   class MultiDimArrayDemo {
       public static void main(String[] args) {
           String[][] names = {
               {"Mr. ", "Mrs. ", "Ms. "},
               {"Smith", "Jones"}
           };
           // Mr. Smith
           System.out.println(names[0][0] + names[1][0]);
           // Ms. Jones
           System.out.println(names[0][2] + names[1][1]);
       }
   }

使用\ ``System.arraycopy()``\ 复制数组：

.. code:: java

   class ArrayCopyDemo {
       public static void main(String[] args) {
           String[] copyFrom = {
               "Affogato", "Americano", "Cappuccino", "Corretto", "Cortado",
               "Doppio", "Espresso", "Frappucino", "Freddo", "Lungo", "Macchiato",
               "Marocchino", "Ristretto" };

           String[] copyTo = new String[7];
           System.arraycopy(copyFrom, 2, copyTo, 0, 7);
           for (String coffee : copyTo) {
               System.out.print(coffee + " ");
           }
       }
   }

使用\ ``java.util.Arrays.copyOfRange``\ 复制数组：

.. code:: java

   class ArrayCopyOfDemo {
       public static void main(String[] args) {
           String[] copyFrom = {
               "Affogato", "Americano", "Cappuccino", "Corretto", "Cortado",
               "Doppio", "Espresso", "Frappucino", "Freddo", "Lungo", "Macchiato",
               "Marocchino", "Ristretto" };

           String[] copyTo = java.util.Arrays.copyOfRange(copyFrom, 2, 9);
           for (String coffee : copyTo) {
               System.out.print(coffee + " ");
           }
       }
   }

操作符
^^^^^^

赋值：

.. code:: java

   int cadence = 0;
   int speed = 0;
   int gear = 1;

数学运算：

.. code:: java

   class ArithmeticDemo {

       public static void main (String[] args) {

           int result = 1 + 2;
           // result is now 3
           System.out.println("1 + 2 = " + result);
           int original_result = result;

           result = result - 1;
           // result is now 2
           System.out.println(original_result + " - 1 = " + result);
           original_result = result;

           result = result * 2;
           // result is now 4
           System.out.println(original_result + " * 2 = " + result);
           original_result = result;

           result = result / 2;
           // result is now 2
           System.out.println(original_result + " / 2 = " + result);
           original_result = result;

           result = result + 8;
           // result is now 10
           System.out.println(original_result + " + 8 = " + result);
           original_result = result;

           result = result % 7;
           // result is now 3
           System.out.println(original_result + " % 7 = " + result);
       }
   }

``x += 1;``\ 等同于\ ``x = x + 1;``

一元运算符：

.. code:: java

   class UnaryDemo {

       public static void main(String[] args) {

           int result = +1;
           // result is now 1
           System.out.println(result);

           result--;
           // result is now 0
           System.out.println(result);

           result++;
           // result is now 1
           System.out.println(result);

           result = -result;
           // result is now -1
           System.out.println(result);

           boolean success = false;
           // false
           System.out.println(success);
           // true
           System.out.println(!success);
       }
   }

``++i``\ 和\ ``i++``\ 都会加1，区别是\ ``++i``\ 的结果是递增后的值，\ ``i++``\ 的结果是原来的值：

.. code:: java

   class PrePostDemo {
       public static void main(String[] args){
           int i = 3;
           i++;
           // prints 4
           System.out.println(i);
           ++i;               
           // prints 5
           System.out.println(i);
           // prints 6
           System.out.println(++i);
           // prints 6
           System.out.println(i++);
           // prints 7
           System.out.println(i);
       }
   }

关系运算符：

.. code:: java

   class ComparisonDemo {

       public static void main(String[] args){
           int value1 = 1;
           int value2 = 2;
           if(value1 == value2)
               System.out.println("value1 == value2");
           if(value1 != value2)
               System.out.println("value1 != value2");
           if(value1 > value2)
               System.out.println("value1 > value2");
           if(value1 < value2)
               System.out.println("value1 < value2");
           if(value1 <= value2)
               System.out.println("value1 <= value2");
       }
   }

条件运算符：

.. code:: java

   class ConditionalDemo1 {

       public static void main(String[] args){
           int value1 = 1;
           int value2 = 2;
           if ((value1 == 1) && (value2 == 2))
               System.out.println("value1 is 1 AND value2 is 2");
           if ((value1 == 1) || (value2 == 1))
               System.out.println("value1 is 1 OR value2 is 1");
       }
   }

``?:``\ 等同于\ ``if-then-else``

.. code:: java

   class ConditionalDemo2 {

       public static void main(String[] args){
           int value1 = 1;
           int value2 = 2;
           int result;
           boolean someCondition = true;
           result = someCondition ? value1 : value2;

           System.out.println(result);
       }
   }

Instanceof判断：an object is an instance of a class, an instance of a
subclass, or an instance of a class that implements a particular
interface

.. code:: java

   class InstanceofDemo {
       public static void main(String[] args) {

           Parent obj1 = new Parent();
           Parent obj2 = new Child();

           System.out.println("obj1 instanceof Parent: "
               + (obj1 instanceof Parent));
           System.out.println("obj1 instanceof Child: "
               + (obj1 instanceof Child));
           System.out.println("obj1 instanceof MyInterface: "
               + (obj1 instanceof MyInterface));
           System.out.println("obj2 instanceof Parent: "
               + (obj2 instanceof Parent));
           System.out.println("obj2 instanceof Child: "
               + (obj2 instanceof Child));
           System.out.println("obj2 instanceof MyInterface: "
               + (obj2 instanceof MyInterface));
       }
   }

   class Parent {}
   class Child extends Parent implements MyInterface {}
   interface MyInterface {}

位运算符：

.. code:: java

   class BitDemo {
       public static void main(String[] args) {
           int bitmask = 0x000F;
           int val = 0x2222;
           // prints "2"
           System.out.println(val & bitmask);
       }
   }

语句
^^^^

**表达式**

.. code:: java

   int cadence = 0;
   anArray[0] = 100;
   System.out.println("Element 1 at index 0: " + anArray[0]);

   int result = 1 + 2; // result is now 3
   if (value1 == value2)
       System.out.println("value1 == value2");

**语句**

.. code:: java

   // assignment statement
   aValue = 8933.234;

   // increment statement
   aValue++;

   // method invocation statement
   System.out.println("Hello World!");

   // object creation statement
   Bicycle myBike = new Bicycle();

**块**

.. code:: java

   class BlockDemo {
        public static void main(String[] args) {
             boolean condition = true;
             if (condition) { // begin block 1
                  System.out.println("Condition is true.");
             } // end block one
             else { // begin block 2
                  System.out.println("Condition is false.");
             } // end block 2
        }
   }

控制语句
^^^^^^^^

``if-then``

.. code:: java

   void applyBrakes() {
       // the "if" clause: bicycle must be moving
       if (isMoving){
           // the "then" clause: decrease current speed
           currentSpeed--;
       }
   }

``if-then-else``

.. code:: java

   class IfElseDemo {
       public static void main(String[] args) {

           int testscore = 76;
           char grade;

           if (testscore >= 90) {
               grade = 'A';
           } else if (testscore >= 80) {
               grade = 'B';
           } else if (testscore >= 70) {
               grade = 'C';
           } else if (testscore >= 60) {
               grade = 'D';
           } else {
               grade = 'F';
           }
           System.out.println("Grade = " + grade);
       }
   }

``while``

.. code:: java

   class WhileDemo {
       public static void main(String[] args){
           int count = 1;
           while (count < 11) {
               System.out.println("Count is: " + count);
               count++;
           }
       }
   }

``do-while``

.. code:: java

   class DoWhileDemo {
       public static void main(String[] args){
           int count = 1;
           do {
               System.out.println("Count is: " + count);
               count++;
           } while (count < 11);
       }
   }

``for``

.. code:: java

   class ForDemo {
       public static void main(String[] args){
            for(int i = 1; i < 11; i++){
                 System.out.println("Count is: " + i);
            }
       }
   }

``enhanced for``

.. code:: java

   class EnhancedForDemo {
       public static void main(String[] args){
            int[] numbers =
                {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
            for (int item : numbers) {
                System.out.println("Count is: " + item);
            }
       }
   }

``break``

.. code:: java

   class BreakDemo {
       public static void main(String[] args) {

           int[] arrayOfInts =
               { 32, 87, 3, 589,
                 12, 1076, 2000,
                 8, 622, 127 };
           int searchfor = 12;

           int i;
           boolean foundIt = false;

           for (i = 0; i < arrayOfInts.length; i++) {
               if (arrayOfInts[i] == searchfor) {
                   foundIt = true;
                   break;
               }
           }

           if (foundIt) {
               System.out.println("Found " + searchfor + " at index " + i);
           } else {
               System.out.println(searchfor + " not in the array");
           }
       }
   }

``continue``

.. code:: java

   class ContinueDemo {
       public static void main(String[] args) {

           String searchMe = "peter piper picked a " + "peck of pickled peppers";
           int max = searchMe.length();
           int numPs = 0;

           for (int i = 0; i < max; i++) {
               // interested only in p's
               if (searchMe.charAt(i) != 'p')
                   continue;

               // process p's
               numPs++;
           }
           System.out.println("Found " + numPs + " p's in the string.");
       }
   }

``return``

.. code:: java

   return ++count;  // 返回value
   return;  // 返回void

Switch语句
^^^^^^^^^^

.. code:: java

   int quarter = ...; // any value

   String quarterLabel = null;
   switch (quarter) {
       case 0: quarterLabel = "Q1 - Winter"; 
               break;
       case 1: quarterLabel = "Q2 - Spring"; 
               break;
       case 2: quarterLabel = "Q3 - Summer"; 
               break;
       case 3: quarterLabel = "Q3 - Summer"; 
               break;
       default: quarterLabel = "Unknown quarter";
   };

selector的类型只能是：

-  byte short char int 基本数据类型

-  Byte Short Character Integer 包装类型

-  枚举类型

-  String类型

**不能是：boolean long float double**

不写break会全部case执行一遍：

.. code:: java

   int month = 8;
   List<String> futureMonths = new ArrayList<>();

   switch (month) {
       case 1:  futureMonths.add("January");
       case 2:  futureMonths.add("February");
       case 3:  futureMonths.add("March");
       case 4:  futureMonths.add("April");
       case 5:  futureMonths.add("May");
       case 6:  futureMonths.add("June");
       case 7:  futureMonths.add("July");
       case 8:  futureMonths.add("August");
       case 9:  futureMonths.add("September");
       case 10: futureMonths.add("October");
       case 11: futureMonths.add("November");
       case 12: futureMonths.add("December");
                break;
       default: break;
   }

多个case连写：

.. code:: java

   int month = 2;
   int year = 2021;
   int numDays = 0;

   switch (month) {
       case 1: case 3: case 5:   // January March May
       case 7: case 8: case 10:  // July August October
       case 12:
           numDays = 31;
           break;
       case 4: case 6:   // April June
       case 9: case 11:  // September November
           numDays = 30;
           break;
       case 2: // February
           if (((year % 4 == 0) && 
                !(year % 100 == 0))
                || (year % 400 == 0))
               numDays = 29;
           else
               numDays = 28;
           break;
       default:
           System.out.println("Invalid month.");
           break;
   }

如果selector是null，会报空指针异常：NullPointerException

   参考资料：

   Java Language Basics https://dev.java/learn/language-basics/

.. |image1| image:: ../wanggang.png
