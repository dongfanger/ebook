# 【Flask】Flask使用SQLite数据库
![](../wanggang.png)

SQLite是一个小型的轻量数据库，特别适合个人学习使用。因为SQLite不需要额外的数据库服务器，同时它也是内嵌在Python中的。缺点就是如果有大量的写请求过来，它是串行处理的，速度很慢。

## 连接数据库

新建`flaskr/db.py`文件：

```python
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

`g`是flask给每个请求创建的独立的对象，用来存储全局数据。通过`g`实现了同一个请求多次调用`get_db`时，不会创建新连接而是会复用已建立的连接。

`get_db`会在flask应用创建后，处理数据库连接时被调用。

`sqlite3.connect()`用来建立数据库连接，它指定了配置文件的Key `DATABASE`。

`sqlite3.Row`让数据库以字典的形式返回行，这样就能通过列名进行取值。

`close_db`关闭数据库连接，它先检查`g.db`有没有设置，如果设置了就关闭db。

## 创建表

新建`flaskr/schema.sql`文件：

```sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

在`flaskr/db.py`文件中添加以下代码：

```python
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
```

`open_resource()`打开刚才创建的数据库脚本文件。

`@click.command()`定义了命令行命令`init-db`。

## 注册到应用

`close_db`和`init_db_command`函数Flask不会自动触发，需要手动注册到应用上。

编辑`flaskr/db.py`文件：

```python
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

`app.teardown_appcontext`指定响应结束后清理时的函数。

`app.cli.add_command`定义了可以被`flask`命令使用的命令。

再把`init_app`手动添加到创建应用函数中，编辑`flaskr/__init__.py`文件：

```python
def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app
```

## 执行命令

至此，准备工作已就绪，打开命令行执行：

```
$ flask init-db
Initialized the database.
```

在项目目录下，就会生成一个`flaskr.sqlite`，这就是SQLite数据库。

> 参考资料：
>
> https://flask.palletsprojects.com/en/2.0.x/tutorial/database/