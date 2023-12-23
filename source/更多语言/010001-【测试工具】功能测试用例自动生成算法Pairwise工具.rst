【测试工具】功能测试用例自动生成算法Pairwise工具
================================================

|image1|

功能测试用例自动生成算法Pairwise工具
------------------------------------

|image2|

Pairwise算法是什么
~~~~~~~~~~~~~~~~~~

对于以下测试场景：

-  浏览器：M，O，P
-  操作平台：W（windows），L（linux），i（ios）
-  语言：C（chinese），E（english）

该如何设计功能测试用例呢？

根据数学统计分析，73%的缺陷（单因子是35%，双因子是38%）是由单因子或2个因子相互作用产生的。19%的缺陷是由3个因子相互作用产生的。也就是说，\ **大多数的bug都是条件的两两组合造成的**\ 。

Pairwise算法是L. L.
Thurstone在1927年首先提出来的，他是美国的一位心理统计学家。Pairwise算法基于两两组合，过滤出性价比高的用例集。它的思路是：\ **如果某一组用例的两两组合结果，在其他组合中均出现，就删除该组用例，从而精简用例**\ 。

对于上述测试场景，可以通过笛卡尔积设计18条两两组合的测试用例：

::

   1，M W C
   2，M W E
   3，M L C
   4，M L E
   5，M I C
   6，M I E
   7，O W C
   8，O W E
   9，O L C
   10，O L E
   11，O I C
   12，O I E
   13，P W C
   14，P W E
   15，P L C
   16，P L E
   17，P I C
   18，P I E

对于第18条用例\ ``P I E``\ 来说，两两组合是\ ``PI ，PE ，IE``\ ，\ ``PI``\ 在17号，\ ``PE``\ 在16号，\ ``IE``\ 在12号出现过，所以第18条用例可以过滤掉。按照这个算法继续过滤，最终剩下9条用例：

::

   1，M W C
   4，M L E
   6，M I E
   7，O W E
   9，O L C
   11，O I C
   14，P W E
   15，P L C
   17，P I C

**用例减少了50%！**\ 而且维度越多越明显，当有10个维度的时候\ ``4*4*4*4*3*3*3*2*2*2``\ =55296个测试case，pairwise为24个，是原始测试用例规模的0.04%。

Python实现
~~~~~~~~~~

源码已上传：https://github.com/dongfanger/python-tools/blob/main/pairwise.py

.. code:: python

   #!/usr/bin/python
   ### encoding=utf-8

   """
   @Author  :  Don
   @Date    :  2021/11/03 20:34
   @Desc    :  
   """

   import copy
   import itertools
   from sys import stdout

   from loguru import logger


   def parewise(option):
       """pairwise算法"""
       cp = []  # 笛卡尔积
       s = []  # 两两拆分
       for x in eval('itertools.product' + str(tuple(option))):
           cp.append(x)
           s.append([i for i in itertools.combinations(x, 2)])
       logger.info('笛卡尔积:%s' % len(cp))
       del_row = []
       bar(0)
       s2 = copy.deepcopy(s)
       for i in range(len(s)):  # 对每行用例进行匹配
           if (i % 100) == 0 or i == len(s) - 1:
               bar(int(100 * i / (len(s) - 1)))
           t = 0
           for j in range(len(s[i])):  # 对每行用例的两两拆分进行判断，是否出现在其他行
               flag = False
               for i2 in [x for x in range(len(s2)) if s2[x] != s[i]]:  # 找同一列
                   if s[i][j] == s2[i2][j]:
                       t = t + 1
                       flag = True
                       break
               if not flag:  # 同一列没找到，不用找剩余列了
                   break
           if t == len(s[i]):
               del_row.append(i)
               s2.remove(s[i])
       res = [cp[i] for i in range(len(cp)) if i not in del_row]
       logger.info('过滤后:%s' % len(res))
       return res


   def bar(i):
       """进度条"""
       c = int(i / 10)
       jd = '\r %2d%% [%s%s]'
       a = '■' * c
       b = '□' * (10 - c)
       msg = jd % (i, a, b)
       stdout.write(msg)
       stdout.flush()


   if __name__ == '__main__':
       pl = [['M', 'O', 'P'], ['W', 'L', 'I'], ['C', 'E']]
       a = parewise(pl)
       print()
       for i in a:
           print(i)

输出结果：

::

    100% [■■■■■■■■■■]
   ('M', 'W', 'E')
   ('M', 'L', 'E')
   ('M', 'I', 'C')
   ('O', 'W', 'E')
   ('O', 'L', 'E')
   ('O', 'I', 'C')
   ('P', 'W', 'C')
   ('P', 'L', 'C')
   ('P', 'I', 'E')
   2021-11-07 11:38:56.850 | INFO     | __main__:parewise:24 - 笛卡尔积:18
   2021-11-07 11:38:56.850 | INFO     | __main__:parewise:45 - 过滤后:9

参考资料：

https://blog.csdn.net/ztf312/article/details/78792906

https://www.cnblogs.com/df888/p/11747616.html

.. |image1| image:: ../wanggang.png
.. |image2| image:: ../wanggang.png
