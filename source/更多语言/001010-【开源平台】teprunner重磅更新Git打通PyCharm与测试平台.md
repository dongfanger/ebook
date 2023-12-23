# 【开源平台】teprunner重磅更新Git打通PyCharm与测试平台
![](../wanggang.png)

经过Python测试交流群的小伙伴群策群力，teprunner添加了一个重要功能，把PyCharm中的代码，通过Git同步到测试平台中，生成测试用例。这样，teprunner就成了一个名副其实的**pytest脚本在线管理平台**。

## 效果展示

项目添加Git仓库和Git分支：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230038968.png)

点击同步按钮即可进行Git同步：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230244021.png)

## 同步说明

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615230356255.png)

为什么要把平台用例和Git用例独立？如果平台上面的用例可以通过Git进行提交代码，那么代码冲突会很难解决，这是其一。其二是平台用例的好处就是规避了Git管理代码的冲突问题，一般测试人员代码能力没有开发人员那么强，代码冲突解决起来是真的费时费力。其三是如果用例在平台和Git中都有修改，那么同步时并不知道哪一份是最新的，无法判断。

## 前端开发内容

router添加路由：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231704773.png)

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231720045.png)

给项目增加两个输入框：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231811870.png)

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231831122.png)

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231846686.png)

表格增加两列：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231928872.png)

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615231940304.png)

给测试用例的描述添加一个链接，查看用例：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232040316.png)

接口响应添加来源字段：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232220248.png)

根据来源区分编辑和删除的操作权限：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232141389.png)

用例查看页面：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232306059.png)

Git同步菜单：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232338033.png)

Git同步页面及说明：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232441527.png)

请求后端gitSync接口：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232427746.png)

## 后端开发内容

Project新增字段：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232638405.png)

Case新增字段：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232710277.png)

其中filename用于缓存在数据库中的用例代码对应的文件名（实际上是相对于tests目录的路径）。

数据迁移：

```
python manage.py makemigrations
python manage.py migrate
```

ProjectSerializer添加字段：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615232943327.png)

CaseSerializer和CaseListSerializer添加字段：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233026266.png)

url添加路由：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233107573.png)

git_sync视图：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233731606.png)

Git同步后端配置：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233138299.png)

从Git拉代码：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233302973.png)

如果docker中没有就clone，如果已经存在就checkout到指定分支再git pull。

同步用例：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233458789.png)

根据数据库中的filenames和git的filenames进行集合化后求差集/交集，得出需要删除/添加/更新的用例集，然后分别操作数据库缓存。

读取git文件内容：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233250022.png)

从文件内容提取描述和创建人：

![](001010-【开源平台】teprunner重磅更新Git打通PyCharm与测试平台/image-20210615233214108.png)

## 小结

本文介绍了如何使用Git把PyCharm中的pytest脚本，同步到测试平台进行管理。至此，**teprunner测试平台V1.0.0**正式完成。后续会逐渐完善部署文档和用户手册，欢迎持续关注。

