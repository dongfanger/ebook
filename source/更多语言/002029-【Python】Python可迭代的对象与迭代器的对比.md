# 【Python】Python可迭代的对象与迭代器的对比
![](../wanggang.png)

什么是迭代？迭代是指按需一次获取一个数据。是否可以迭代，可以通过是否可以使用for循环取值来进行简单的判断。更准确的判断是使用`iter()`函数，这是一个Python内置函数。

## 可迭代的对象

`iter()`函数的作用如下：

1. 如果对象实现了`__iter__`方法，那么就调用它，**获取一个迭代器**。比如：

   ```python
   def __iter__(self):
       return SentenceIterator(self.words)
   ```

2. 如果对象没有实现`__iter__`但是实现了`__getitem__`方法，那么就**创建一个迭代器**，尝试从索引0开始获取元素。

3. 如果尝试获取元素失败，就会抛出TypeError异常。

可迭代的对象，就是使用`iter()`函数判断，满足前面2点的对象。

任何Python序列都是可以迭代的，因为它们都实现了`__getitem__`方法。

## 迭代器

从前面`iter()`函数的作用可以发现，**迭代器是从可迭代的对象中获取的**。

1. 如果对象本身是可迭代的，就调用`__iter__`方法获取一个迭代器。
2. 如果对象不可迭代但是实现了`__getitem__`方法，那么就会创建一个迭代器。

比如可以使用`iter()`函数把列表转换为迭代器：

```python
>>> test_list = [1, 2, 3]
>>> print(type(test_list))
<class 'list'>

>>> test_iter = iter(test_list)
>>> print(type(test_iter))
<class 'list_iterator'>
```

迭代器可以使用for循环遍历：

```python
for x in test_iter:
    print(x)
```

也可以使用while循环遍历：

```python
while True:
    try:
        print(next(test_iter))
    except StopIteration:
        del test_iter
        break
```

- `next()`函数用于获取迭代器下一个元素。
- 没有元素了，迭代器会抛出StopIteration异常。

标准的迭代器接口有两个方法：

- `__next__`返回下一个元素。

- `__iter__`返回self，以便在应该使用可迭代对象的地方使用迭代器，比如for循环中。

  ```python
  def __iter__(self):
      return self
  ```

**迭代器的准确定义是**：迭代器是这样的对象，它实现了无参数的`__next__`方法，返回序列中的下一个元素；如果没有元素了，那么抛出StopIteration异常。Python中的迭代器还实现了`__iter__`方法，因此迭代器也是可以迭代的。

最后，通过对比可以发现，**可迭代对象**的`__iter__`返回的是迭代器：

```python
def __iter__(self):
    return SentenceIterator(self.words)
```

**迭代器**的`__iter__`返回的是self：

```python
class SentenceIterator:
    def __iter__(self):
        return self
```

而且迭代器还需要有`__next__`方法。

**从这一点就能清楚看出它们的区别了。**

需要特别注意的是，可迭代的对象一定不能是自身的迭代器，也就是说，可迭代对象必须实现`__iter__`方法，但是不能实现`__next__`方法。否则会让设计模式变得混乱不堪。

> 参考资料：
>
> 《流畅的Python》第14章 可迭代的对象、迭代器和生成器
>
> https://www.runoob.com/python3/python3-iterator-generator.html