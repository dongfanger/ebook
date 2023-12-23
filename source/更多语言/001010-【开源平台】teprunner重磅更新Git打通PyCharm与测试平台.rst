【开源平台】teprunner重磅更新Git打通PyCharm与测试平台
=====================================================

|image1|

经过Python测试交流群的小伙伴群策群力，teprunner添加了一个重要功能，把PyCharm中的代码，通过Git同步到测试平台中，生成测试用例。这样，teprunner就成了一个名副其实的\ **pytest脚本在线管理平台**\ 。

效果展示
--------

项目添加Git仓库和Git分支：

|image2|

点击同步按钮即可进行Git同步：

|image3|

同步说明
--------

|image4|

为什么要把平台用例和Git用例独立？如果平台上面的用例可以通过Git进行提交代码，那么代码冲突会很难解决，这是其一。其二是平台用例的好处就是规避了Git管理代码的冲突问题，一般测试人员代码能力没有开发人员那么强，代码冲突解决起来是真的费时费力。其三是如果用例在平台和Git中都有修改，那么同步时并不知道哪一份是最新的，无法判断。

前端开发内容
------------

router添加路由：

|image5|

|image6|

给项目增加两个输入框：

|image7|

|image8|

|image9|

表格增加两列：

|image10|

|image11|

给测试用例的描述添加一个链接，查看用例：

|image12|

接口响应添加来源字段：

|image13|

根据来源区分编辑和删除的操作权限：

|image14|

用例查看页面：

|image15|

Git同步菜单：

|image16|

Git同步页面及说明：

|image17|

请求后端gitSync接口：

|image18|

后端开发内容
------------

Project新增字段：

|image19|

Case新增字段：

|image20|

其中filename用于缓存在数据库中的用例代码对应的文件名（实际上是相对于tests目录的路径）。

数据迁移：

::

   python manage.py makemigrations
   python manage.py migrate

ProjectSerializer添加字段：

|image21|

CaseSerializer和CaseListSerializer添加字段：

|image22|

url添加路由：

|image23|

git_sync视图：

|image24|

Git同步后端配置：

|image25|

从Git拉代码：

|image26|

如果docker中没有就clone，如果已经存在就checkout到指定分支再git pull。

同步用例：

|image27|

根据数据库中的filenames和git的filenames进行集合化后求差集/交集，得出需要删除/添加/更新的用例集，然后分别操作数据库缓存。

读取git文件内容：

|image28|

从文件内容提取描述和创建人：

|image29|

小结
----

本文介绍了如何使用Git把PyCharm中的pytest脚本，同步到测试平台进行管理。至此，\ **teprunner测试平台V1.0.0**\ 正式完成。后续会逐渐完善部署文档和用户手册，欢迎持续关注。

.. |image1| image:: ../wanggang.png
.. |image2| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230038968.png
.. |image3| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230244021.png
.. |image4| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230356255.png
.. |image5| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231704773.png
.. |image6| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231720045.png
.. |image7| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231811870.png
.. |image8| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231831122.png
.. |image9| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231846686.png
.. |image10| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231928872.png
.. |image11| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231940304.png
.. |image12| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232040316.png
.. |image13| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232220248.png
.. |image14| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232141389.png
.. |image15| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232306059.png
.. |image16| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232338033.png
.. |image17| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232441527.png
.. |image18| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232427746.png
.. |image19| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232638405.png
.. |image20| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232710277.png
.. |image21| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232943327.png
.. |image22| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233026266.png
.. |image23| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233107573.png
.. |image24| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233731606.png
.. |image25| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233138299.png
.. |image26| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233302973.png
.. |image27| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233458789.png
.. |image28| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233250022.png
.. |image29| image:: 001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233214108.png
