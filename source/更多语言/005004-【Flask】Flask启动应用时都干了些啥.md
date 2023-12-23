# 【Flask】Flask启动应用时都干了些啥
![](../wanggang.png)

一个Flask应用（Flask Application）是Flask类（Flask Class）的实例。在前面的文章中，都是通过定义**全局Flask实例**的方式来编写的Flask应用代码，比如：

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"
```

**Python的模块（Module）天然就是单例的**，模块级别的对象自然而然也是单例的。这种方式在写简单的脚本时很方便，但如果是写项目，随着项目逐渐扩大，会出现越来越棘手的问题。

除了定义全局实例，还有一种方式叫做工厂函数（Factory Function），在Flask这，也能叫应用工厂（Application Factory），**Flask应用工厂函数**的返回是Flask类的实例对象。

典型的Flask应用工厂函数如下所示：

```python
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```

这段代码可以放到flaskr目录下面的`__init__.py`文件中：

```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
```

通过这段代码，我们可以看看Flask应用启动时，都干了些啥：

1. `app = Flask(__name__, instance_relative_config=True)`创建了Flask实例。`__name__`是指当前模块的名字，这样Flask就能找到应用启动的入口。`instance_relative_config=True`告诉Flask配置文件是用的实例文件夹的相对路径。

   > 所谓实例文件夹，是指和flaskr同级的一个名字为instance的文件夹，适合存放私有配置的秘钥或者本地数据库等不需要上传到Git的文件，可以通过`Flask.instance_path`获取完整路径。

2. `app.config.from_mapping()`设置了默认配置。`SECRET_KEY`是Flask用来给数据加密的私钥。`DATABASE`指定了数据库文件路径。

3. `app.config.from_pyfile()`用来覆盖默认配置，from_pyfile方法从文件获取配置，from_mapping通过键值对设定配置。

4. `os.makedirs(app.instance_path)`确保创建了实例文件夹。

5. `@app.route()`定义了路由和处理函数。

总的来说，**Flask可以通过应用工厂（Application Factory）函数，在Flask应用启动时干这些事**：实例化Flask对象→设定配置→创建实例文件夹→定义路由→定义处理函数。

Flask启动后能看到以下日志：

```
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

除了`python`命令启动Flask应用，也可以直接用`flask`命令，示例如下：

```shell
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```

> 参考资料：
>
> https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/

