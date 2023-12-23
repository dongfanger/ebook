# 【Python】Python上下文管理器
![](../wanggang.png)

with语句会设置一个临时的上下文，交给上下文管理器对象控制，并且负责清理上下文。

比如在打开文件时通常都会使用with语句：

```python
with open("a.txt") as f:
    f.read()
```

with块执行完后会自动关闭文件。

**Python上下文管理器对象存在的目的就是管理with语句。**

## 实现一个上下文管理器

上下文管理器协议包含`__enter__`和`__exit__`两个方法，所以要实现一个上下文管理器，就得实现这两个方法，比如：

```python
class LookingGlass:

    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True
```

- `__enter__`是上下文管理器的入口，在with语句开始运行时调用。
- `__exit__`是上下文管理器的出口，在with语句运行结束后调用。

上下文管理器对象是在执行with后面的表达式得到的：

```python
with LookingGlass() as what:
    print(what)
```

as子句是可选的，在as执行前就已经得到了上下文管理器对象，在as执行时实际就已经调用`__enter__`了。

## 把生成器变为上下文管理器

使用`@contextmanager`装饰器能减少创建上下文管理器的样板代码量，只需要实现一个有yield语句的生成器，生成想让`__enter__`方法返回的值。

示例：

```python
import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
```

yield语句的作用是：

- 在yield语句前面的代码在with块开始时执行，相当于`__enter__`。
- 在yield语句后面的代码在with块结束时执行，相当于`__exit__`。

注意这里的yield与迭代没有任何关系，这其实引出了Python另一个重要技术点，协程：执行到某一点时暂停，让客户代码运行，直到客户让协程继续做事。下篇文章将展开对Python协程的学习。

> 参考资料：
>
> 《流畅的Python》第15章 上下文管理器和else块