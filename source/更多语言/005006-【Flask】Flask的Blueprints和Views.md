# 【Flask】Flask的Blueprints和Views
![](../wanggang.png)

Flask的view函数是用来对请求作出响应的。单个URL能匹配到单个View，那么多个类似的URL，比如：

```
/auth/register
/auth/login
/auth/logout
```

有没有什么比较优雅的写法呢？

## Blueprints

**Blueprints就是一个路由分组，可以把共同的路由前缀注册为一个Blueprint**，比如：

在`flaskr/auth.py`文件中先定义一个Blueprint：

```python
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
```

- `'auth'`是Blueprint的名字。
- `__name__`用来告诉Blueprint它的定义位置。
- `url_prefix`就是路由前缀。

接着在`flaskr/__init__.py`文件中注册：

```python
def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
```

## Views

定义和注册了Blueprints后就可以在view中使用了。比如：

①在`flaskr/auth.py`文件中添加一个注册view：

```python
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
```

- `@bp.route`就会把路由前缀加到`'/register'`上拼成`/auth/register`。
- `request.form`是一个字典，可以读取接口入参。
- `db.execute`执行SQL语句。`db.commit()`提交。
- `redirect`在注册成功后重定向到登录页面。
- `url_for`根据view名字来获取url，因为这里用到了Blueprint，所以入参是`"auth.login"`。如果没有用Blueprint，`url_for()`函数入参就写view函数名即可。

②在`flaskr/auth.py`文件中添加一个登录view：

```python
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
```

- `fetchone()`取一行数据，`fetchall()`取多行数据。

- 登录成功后会把user_id存入session中，session是一个字典，这样后续请求就可以用到这个数据。比如：

  ```python
  @bp.before_app_request
  def load_logged_in_user():
      user_id = session.get('user_id')
  
      if user_id is None:
          g.user = None
      else:
          g.user = get_db().execute(
              'SELECT * FROM user WHERE id = ?', (user_id,)
          ).fetchone()
  ```

  值得注意的是`@bp.before_app_request`有点像setup，就是在所有请求前先运行这一段代码。

③在`flaskr/auth.py`文件中添加一个登出view：

```python
flaskr/auth.py
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```

- `session.clear()`清除session。

④最后可以在在`flaskr/auth.py`文件中顺手写一个装饰器，用来做认证鉴权：

```python
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

```

在需要登录才能访问的view上，就可以加上这个`login_required`装饰器。

> 参考资料：
>
> https://flask.palletsprojects.com/en/2.0.x/tutorial/views/

