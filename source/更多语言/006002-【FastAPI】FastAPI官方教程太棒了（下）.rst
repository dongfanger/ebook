【FastAPI】FastAPI官方教程太棒了（下）
======================================

|image1|

响应状态码
----------

在\ ``@app.post()``\ 方法中添加status_code参数：

.. code:: python

   from fastapi import FastAPI

   app = FastAPI()


   @app.post("/items/", status_code=201)
   async def create_item(name: str):
       return {"name": name}

status_code也可以是\ ``IntEnum``\ ，比如Python的\ ``http.HTTPStatus``\ 。

常见响应状态码：

-  100以上，信息；很少直接使用；

-  200以上，成功；200是OK，201是Created，204是No Content；

-  300以上，重定向；304是Not Modified；

-  400以上，客户端错误；404是Not Found；

-  500以上，服务器错误；

FastAPI引入了status，可以方便的录入这些状态：

.. code:: python

   from fastapi import FastAPI, status

   app = FastAPI()


   @app.post("/items/", status_code=status.HTTP_201_CREATED)
   async def create_item(name: str):
       return {"name": name}

表单数据
--------

为了使用表单，首先需要安装python-multipart：

.. code:: python

   pip install python-multipart

示例：

.. code:: python

   from fastapi import FastAPI, Form

   app = FastAPI()


   @app.post("/login/")
   async def login(username: str = Form(), password: str = Form()):
       return {"username": username}

表单由HTML中的\ ``<form></form>``\ 发送，请求头的content-type一般是\ ``application/x-www-form-urlencoded``\ ，当为文件时\ ``multipart/form-data``\ 。

请求文件
--------

示例：

.. code:: python

   from fastapi import FastAPI, File, UploadFile

   app = FastAPI()


   @app.post("/files/")
   async def create_file(file: bytes = File()):
       return {"file_size": len(file)}


   @app.post("/uploadfile/")
   async def create_upload_file(file: UploadFile):
       return {"filename": file.filename}

``create_file()``\ 的类型为bytes，接收到的文件内容也是bytes，数据都存在于内存中，适用于小文件。\ ``create_upload_file()``\ 的类型为UploadFile，它会在内存设置一个最大存储，超出最大存储，就会把数据转存到磁盘，适用于大文件。

UploadFile有以下属性：

-  filename，文件名，比如myimage.jpg；

-  content_type，文件类型，比如image/jpeg；

-  file，SpooledTemporaryFile实例，一个file-like对象。

UploadFile有以下方法：

-  write(data)：写数据(str或bytes)到文件；

-  read(size)：从文件读size(int)大小的bytes或character；

-  seek(offset)：定位到文件中offset(int)的位置，比如\ ``await myfile.seek(0)``\ 会定位到文件开始；

-  close()：关闭文件；

所有这些方法都是async的，需要await：

.. code:: python

   contents = await myfile.read()

不想await就使用其中的file对象：

.. code:: python

   contents = myfile.file.read()

文件可选非必传：

.. code:: python

   from typing import Union

   from fastapi import FastAPI, File, UploadFile

   app = FastAPI()


   @app.post("/files/")
   async def create_file(file: Union[bytes, None] = File(default=None)):
       if not file:
           return {"message": "No file sent"}
       else:
           return {"file_size": len(file)}


   @app.post("/uploadfile/")
   async def create_upload_file(file: Union[UploadFile, None] = None):
       if not file:
           return {"message": "No upload file sent"}
       else:
           return {"filename": file.filename}

UploadFile的metadata：

.. code:: python

   from fastapi import FastAPI, File, UploadFile

   app = FastAPI()


   @app.post("/files/")
   async def create_file(file: bytes = File(description="A file read as bytes")):
       return {"file_size": len(file)}


   @app.post("/uploadfile/")
   async def create_upload_file(
       file: UploadFile = File(description="A file read as UploadFile"),
   ):
       return {"filename": file.filename}

多文件上传：

.. code:: python

   from typing import List

   from fastapi import FastAPI, File, UploadFile
   from fastapi.responses import HTMLResponse

   app = FastAPI()


   @app.post("/files/")
   async def create_files(files: List[bytes] = File()):
       return {"file_sizes": [len(file) for file in files]}


   @app.post("/uploadfiles/")
   async def create_upload_files(files: List[UploadFile]):
       return {"filenames": [file.filename for file in files]}


   @app.get("/")
   async def main():
       content = """
   <body>
   <form action="/files/" enctype="multipart/form-data" method="post">
   <input name="files" type="file" multiple>
   <input type="submit">
   </form>
   <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
   <input name="files" type="file" multiple>
   <input type="submit">
   </form>
   </body>
       """
       return HTMLResponse(content=content)

同时请求表单和文件
------------------

示例：

.. code:: python

   from fastapi import FastAPI, File, Form, UploadFile

   app = FastAPI()


   @app.post("/files/")
   async def create_file(
       file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
   ):
       return {
           "file_size": len(file),
           "token": token,
           "fileb_content_type": fileb.content_type,
       }

错误处理
--------

FastAPI提供了HTTPException：

.. code:: python

   from fastapi import FastAPI, HTTPException

   app = FastAPI()

   items = {"foo": "The Foo Wrestlers"}


   @app.get("/items/{item_id}")
   async def read_item(item_id: str):
       if item_id not in items:
           raise HTTPException(status_code=404, detail="Item not found")
       return {"item": items[item_id]}

HTTPException不是return而是raise的，抛出异常。

对于抛出的异常，可以使用\ ``@app.exception_handler``\ 自定义handler进行处理：

.. code:: python

   from fastapi import FastAPI, Request
   from fastapi.responses import JSONResponse


   class UnicornException(Exception):
       def __init__(self, name: str):
           self.name = name


   app = FastAPI()


   @app.exception_handler(UnicornException)
   async def unicorn_exception_handler(request: Request, exc: UnicornException):
       return JSONResponse(
           status_code=418,
           content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
       )


   @app.get("/unicorns/{name}")
   async def read_unicorn(name: str):
       if name == "yolo":
           raise UnicornException(name=name)
       return {"unicorn_name": name}

在抛出HTTPException异常时，FastAPI有很多默认的handler，比如RequestValidationError，可以使用此方法重写默认的handler：

.. code:: python

   from fastapi import FastAPI, HTTPException
   from fastapi.exceptions import RequestValidationError
   from fastapi.responses import PlainTextResponse
   from starlette.exceptions import HTTPException as StarletteHTTPException

   app = FastAPI()


   @app.exception_handler(StarletteHTTPException)
   async def http_exception_handler(request, exc):
       return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


   @app.exception_handler(RequestValidationError)
   async def validation_exception_handler(request, exc):
       return PlainTextResponse(str(exc), status_code=400)


   @app.get("/items/{item_id}")
   async def read_item(item_id: int):
       if item_id == 3:
           raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
       return {"item_id": item_id}

默认handler会返回：

::

   {
   "detail": [
           {
               "loc": [
                   "path",
                   "item_id"
               ],
               "msg": "value is not a valid integer",
               "type": "type_error.integer"
           }
       ]
   }

而重写handler后会返回字符串：

::

   1 validation error
   path -> item_id
     value is not a valid integer (type=type_error.integer)

如果不想改动默认handler，只是补充点信息，可以导入http_exception_handler和request_validation_exception_handler：

.. code:: python

   from fastapi import FastAPI, HTTPException
   from fastapi.exception_handlers import (
       http_exception_handler,
       request_validation_exception_handler,
   )
   from fastapi.exceptions import RequestValidationError
   from starlette.exceptions import HTTPException as StarletteHTTPException

   app = FastAPI()


   @app.exception_handler(StarletteHTTPException)
   async def custom_http_exception_handler(request, exc):
       print(f"OMG! An HTTP error!: {repr(exc)}")
       return await http_exception_handler(request, exc)


   @app.exception_handler(RequestValidationError)
   async def validation_exception_handler(request, exc):
       print(f"OMG! The client sent invalid data!: {exc}")
       return await request_validation_exception_handler(request, exc)


   @app.get("/items/{item_id}")
   async def read_item(item_id: int):
       if item_id == 3:
           raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
       return {"item_id": item_id}

路径操作配置
------------

响应状态码：

.. code:: python

   from typing import Set, Union

   from fastapi import FastAPI, status
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: str
       description: Union[str, None] = None
       price: float
       tax: Union[float, None] = None
       tags: Set[str] = set()


   @app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
   async def create_item(item: Item):
       return item
       

标签：

.. code:: python

   from typing import Set, Union

   from fastapi import FastAPI
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: str
       description: Union[str, None] = None
       price: float
       tax: Union[float, None] = None
       tags: Set[str] = set()


   @app.post("/items/", response_model=Item, tags=["items"])
   async def create_item(item: Item):
       return item


   @app.get("/items/", tags=["items"])
   async def read_items():
       return [{"name": "Foo", "price": 42}]


   @app.get("/users/", tags=["users"])
   async def read_users():
       return [{"username": "johndoe"}]

标签枚举：

.. code:: python

   from enum import Enum

   from fastapi import FastAPI

   app = FastAPI()


   class Tags(Enum):
       items = "items"
       users = "users"


   @app.get("/items/", tags=[Tags.items])
   async def get_items():
       return ["Portal gun", "Plumbus"]


   @app.get("/users/", tags=[Tags.users])
   async def read_users():
       return ["Rick", "Morty"]

概要和描述：

.. code:: python

   from typing import Set, Union

   from fastapi import FastAPI
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: str
       description: Union[str, None] = None
       price: float
       tax: Union[float, None] = None
       tags: Set[str] = set()


   @app.post(
       "/items/",
       response_model=Item,
       summary="Create an item",
       description="Create an item with all the information, name, description, price, tax and a set of unique tags",
   )
   async def create_item(item: Item):
       return item

文档字符串：

.. code:: python

   from typing import Set, Union

   from fastapi import FastAPI
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: str
       description: Union[str, None] = None
       price: float
       tax: Union[float, None] = None
       tags: Set[str] = set()


   @app.post("/items/", response_model=Item, summary="Create an item")
   async def create_item(item: Item):
       """
       Create an item with all the information:

       - **name**: each item must have a name
       - **description**: a long description
       - **price**: required
       - **tax**: if the item doesn't have tax, you can omit this
       - **tags**: a set of unique tag strings for this item
       """
       return item

响应描述：

.. code:: python

   from typing import Set, Union

   from fastapi import FastAPI
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: str
       description: Union[str, None] = None
       price: float
       tax: Union[float, None] = None
       tags: Set[str] = set()


   @app.post(
       "/items/",
       response_model=Item,
       summary="Create an item",
       response_description="The created item",
   )
   async def create_item(item: Item):
       """
       Create an item with all the information:

       - **name**: each item must have a name
       - **description**: a long description
       - **price**: required
       - **tax**: if the item doesn't have tax, you can omit this
       - **tags**: a set of unique tag strings for this item
       """
       return item

标记为deprecated：

.. code:: python

   from fastapi import FastAPI

   app = FastAPI()


   @app.get("/items/", tags=["items"])
   async def read_items():
       return [{"name": "Foo", "price": 42}]


   @app.get("/users/", tags=["users"])
   async def read_users():
       return [{"username": "johndoe"}]


   @app.get("/elements/", tags=["items"], deprecated=True)
   async def read_elements():
       return [{"item_id": "Foo"}]

JSON兼容编码器
--------------

``jsonable_encoder()``\ 函数的作用是把Pydantic
model转换成JSON兼容的类型比如dict、list等。

.. code:: python

   from datetime import datetime
   from typing import Union

   from fastapi import FastAPI
   from fastapi.encoders import jsonable_encoder
   from pydantic import BaseModel

   fake_db = {}


   class Item(BaseModel):
       title: str
       timestamp: datetime
       description: Union[str, None] = None


   app = FastAPI()


   @app.put("/items/{id}")
   def update_item(id: str, item: Item):
       json_compatible_item_data = jsonable_encoder(item)
       fake_db[id] = json_compatible_item_data

Body-更新
---------

使用PUT：

.. code:: python

   from typing import List, Union

   from fastapi import FastAPI
   from fastapi.encoders import jsonable_encoder
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: Union[str, None] = None
       description: Union[str, None] = None
       price: Union[float, None] = None
       tax: float = 10.5
       tags: List[str] = []


   items = {
       "foo": {"name": "Foo", "price": 50.2},
       "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
       "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
   }


   @app.get("/items/{item_id}", response_model=Item)
   async def read_item(item_id: str):
       return items[item_id]


   @app.put("/items/{item_id}", response_model=Item)
   async def update_item(item_id: str, item: Item):
       update_item_encoded = jsonable_encoder(item)
       items[item_id] = update_item_encoded
       return update_item_encoded

输入数据使用了\ ``jsonable_encoder()``\ 函数转换为JSON兼容类型。

使用PATCH：

``exclude_unset=True``

.. code:: python

   from typing import List, Union

   from fastapi import FastAPI
   from fastapi.encoders import jsonable_encoder
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: Union[str, None] = None
       description: Union[str, None] = None
       price: Union[float, None] = None
       tax: float = 10.5
       tags: List[str] = []


   items = {
       "foo": {"name": "Foo", "price": 50.2},
       "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
       "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
   }


   @app.get("/items/{item_id}", response_model=Item)
   async def read_item(item_id: str):
       return items[item_id]


   @app.patch("/items/{item_id}", response_model=Item)
   async def update_item(item_id: str, item: Item):
       stored_item_data = items[item_id]
       stored_item_model = Item(**stored_item_data)
       update_data = item.dict(exclude_unset=True)
       updated_item = stored_item_model.copy(update=update_data)
       items[item_id] = jsonable_encoder(updated_item)
       return updated_item

``.copy(update=update_data)``

.. code:: python

   from typing import List, Union

   from fastapi import FastAPI
   from fastapi.encoders import jsonable_encoder
   from pydantic import BaseModel

   app = FastAPI()


   class Item(BaseModel):
       name: Union[str, None] = None
       description: Union[str, None] = None
       price: Union[float, None] = None
       tax: float = 10.5
       tags: List[str] = []


   items = {
       "foo": {"name": "Foo", "price": 50.2},
       "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
       "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
   }


   @app.get("/items/{item_id}", response_model=Item)
   async def read_item(item_id: str):
       return items[item_id]


   @app.patch("/items/{item_id}", response_model=Item)
   async def update_item(item_id: str, item: Item):
       stored_item_data = items[item_id]
       stored_item_model = Item(**stored_item_data)
       update_data = item.dict(exclude_unset=True)
       updated_item = stored_item_model.copy(update=update_data)
       items[item_id] = jsonable_encoder(updated_item)
       return updated_item

PUT和PATCH都可以用来部分更新，PUT用的更多。

依赖
----

什么是依赖注入？在FastAPI里面，你可以在路径操作函数中添加依赖的声明，然后FastAPI会自动加载这些依赖。

依赖注入的好处有：

-  复用代码；
-  复用数据库连接；
-  增强安全、认证、角色；
-  等等等；

依赖注入示例：

.. code:: python

   from typing import Union

   from fastapi import Depends, FastAPI

   app = FastAPI()


   async def common_parameters(
       q: Union[str, None] = None, skip: int = 0, limit: int = 100
   ):
       return {"q": q, "skip": skip, "limit": limit}


   @app.get("/items/")
   async def read_items(commons: dict = Depends(common_parameters)):
       return commons


   @app.get("/users/")
   async def read_users(commons: dict = Depends(common_parameters)):
       return commons

-  ``common_parameters()``\ 函数是个简单的依赖；
-  Depends引入依赖；

FastAPI就会自动调用\ ``common_parameters()``\ 函数并把结果返回给commons，而无需任何其他代码。

依赖也可以使用class，把\ ``common_parameters()``\ 函数改为\ ``CommonQueryParams``\ 类：

.. code:: python

   from typing import Union

   from fastapi import Depends, FastAPI

   app = FastAPI()


   fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


   class CommonQueryParams:
       def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
           self.q = q
           self.skip = skip
           self.limit = limit


   @app.get("/items/")
   async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
       response = {}
       if commons.q:
           response.update({"q": commons.q})
       items = fake_items_db[commons.skip : commons.skip + commons.limit]
       response.update({"items": items})
       return response

Depends会创建一个CommonQueryParams的实例然后赋值给commons。

更一步简化，只写1次CommonQueryParams：

.. code:: python

   commons: CommonQueryParams = Depends()

``Depends()``\ 里面的CommonQueryParams可以省略掉。

FastAPI支持子依赖，也就是Depends嵌套：

.. code:: python

   from typing import Union

   from fastapi import Cookie, Depends, FastAPI

   app = FastAPI()


   def query_extractor(q: Union[str, None] = None):
       return q


   def query_or_cookie_extractor(
       q: str = Depends(query_extractor),
       last_query: Union[str, None] = Cookie(default=None),
   ):
       if not q:
           return last_query
       return q


   @app.get("/items/")
   async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
       return {"q_or_cookie": query_or_default}

如果使用同一个依赖多次，FastAPI默认会只注入一次。可以按以下设置让FastAPI注入多次：

.. code:: python

   async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
       return {"fresh_value": fresh_value}

多个依赖可以用\ ``dependencies``\ 的list：

.. code:: python

   from fastapi import Depends, FastAPI, Header, HTTPException

   app = FastAPI()


   async def verify_token(x_token: str = Header()):
       if x_token != "fake-super-secret-token":
           raise HTTPException(status_code=400, detail="X-Token header invalid")


   async def verify_key(x_key: str = Header()):
       if x_key != "fake-super-secret-key":
           raise HTTPException(status_code=400, detail="X-Key header invalid")
       return x_key


   @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
   async def read_items():
       return [{"item": "Foo"}, {"item": "Bar"}]

如果给FastAPI的构造函数传入\ ``dependencies``\ ，那么就是全局依赖：

.. code:: python

   from fastapi import Depends, FastAPI, Header, HTTPException


   async def verify_token(x_token: str = Header()):
       if x_token != "fake-super-secret-token":
           raise HTTPException(status_code=400, detail="X-Token header invalid")


   async def verify_key(x_key: str = Header()):
       if x_key != "fake-super-secret-key":
           raise HTTPException(status_code=400, detail="X-Key header invalid")
       return x_key


   app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


   @app.get("/items/")
   async def read_items():
       return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


   @app.get("/users/")
   async def read_users():
       return [{"username": "Rick"}, {"username": "Morty"}]

如果在依赖函数中使用yield，它后面的代码就相当于teardown，这点用法跟pytest的fixture类似：

.. code:: python

   async def get_db():
       db = DBSession()
       try:
           yield db
       finally:
           db.close()

另外，借助yield和with可以创建一个上下文管理器（实现\ ``__enter__``\ 和\ ``__exit__``\ ）：

.. code:: python

   class MySuperContextManager:
       def __init__(self):
           self.db = DBSession()

       def __enter__(self):
           return self.db

       def __exit__(self, exc_type, exc_value, traceback):
           self.db.close()


   async def get_db():
       with MySuperContextManager() as db:
           yield db

安全
----

FastAPI支持OAuth2协议：

.. code:: python

   from fastapi import Depends, FastAPI
   from fastapi.security import OAuth2PasswordBearer

   app = FastAPI()

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


   @app.get("/items/")
   async def read_items(token: str = Depends(oauth2_scheme)):
       return {"token": token}

备注：需要提前安装
``pip install python-multipart``\ ，因为OAuth2使用表单来发送username和password。虽然这个接口已经加上鉴权了。但这些入参都没有生效，因为我们还没有添加相应的处理代码。为了让鉴权实际生效，我们继续添加代码：

.. code:: python

   from typing import Union

   from fastapi import Depends, FastAPI
   from fastapi.security import OAuth2PasswordBearer
   from pydantic import BaseModel

   app = FastAPI()

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


   class User(BaseModel):
       username: str
       email: Union[str, None] = None
       full_name: Union[str, None] = None
       disabled: Union[bool, None] = None


   def fake_decode_token(token):
       return User(
           username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
       )


   async def get_current_user(token: str = Depends(oauth2_scheme)):
       user = fake_decode_token(token)
       return user


   @app.get("/users/me")
   async def read_users_me(current_user: User = Depends(get_current_user)):
       return current_user

1. 定义模型User；
2. 创建依赖get_current_user；
3. fake_decode_token接收token，返回模拟的假用户；
4. read_users_me注入依赖；

然后实现username和password：

.. code:: python

   from typing import Union

   from fastapi import Depends, FastAPI, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
   from pydantic import BaseModel

   fake_users_db = {
       "johndoe": {
           "username": "johndoe",
           "full_name": "John Doe",
           "email": "johndoe@example.com",
           "hashed_password": "fakehashedsecret",
           "disabled": False,
       },
       "alice": {
           "username": "alice",
           "full_name": "Alice Wonderson",
           "email": "alice@example.com",
           "hashed_password": "fakehashedsecret2",
           "disabled": True,
       },
   }

   app = FastAPI()


   def fake_hash_password(password: str):
       return "fakehashed" + password


   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


   class User(BaseModel):
       username: str
       email: Union[str, None] = None
       full_name: Union[str, None] = None
       disabled: Union[bool, None] = None


   class UserInDB(User):
       hashed_password: str


   def get_user(db, username: str):
       if username in db:
           user_dict = db[username]
           return UserInDB(**user_dict)


   def fake_decode_token(token):
       # This doesn't provide any security at all
       # Check the next version
       user = get_user(fake_users_db, token)
       return user


   async def get_current_user(token: str = Depends(oauth2_scheme)):
       user = fake_decode_token(token)
       if not user:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid authentication credentials",
               headers={"WWW-Authenticate": "Bearer"},
           )
       return user


   async def get_current_active_user(current_user: User = Depends(get_current_user)):
       if current_user.disabled:
           raise HTTPException(status_code=400, detail="Inactive user")
       return current_user


   @app.post("/token")
   async def login(form_data: OAuth2PasswordRequestForm = Depends()):
       user_dict = fake_users_db.get(form_data.username)
       if not user_dict:
           raise HTTPException(status_code=400, detail="Incorrect username or password")
       user = UserInDB(**user_dict)
       hashed_password = fake_hash_password(form_data.password)
       if not hashed_password == user.hashed_password:
           raise HTTPException(status_code=400, detail="Incorrect username or password")

       return {"access_token": user.username, "token_type": "bearer"}


   @app.get("/users/me")
   async def read_users_me(current_user: User = Depends(get_current_active_user)):
       return current_user

现在就可以测试一下了http://127.0.0.1:8000/docs：

|image2|

授权以后：

|image3|

访问\ ``/users/me``\ 会返回：

::

   {
     "username": "johndoe",
     "email": "johndoe@example.com",
     "full_name": "John Doe",
     "disabled": false,
     "hashed_password": "fakehashedsecret"
   }

如果logout再访问会出现：

::

   {
     "detail": "Not authenticated"
   }

输入错误的用户会出现：

::

   {
     "detail": "Inactive user"
   }

如果想使用JWT，那么先安装\ ``python-jose``\ 。为了给密码加密，需要安装\ ``passlib``\ 。

示例代码：

.. code:: python

   from datetime import datetime, timedelta
   from typing import Union

   from fastapi import Depends, FastAPI, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
   from jose import JWTError, jwt
   from passlib.context import CryptContext
   from pydantic import BaseModel

   ## to get a string like this run:
   ## openssl rand -hex 32
   SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 30


   fake_users_db = {
       "johndoe": {
           "username": "johndoe",
           "full_name": "John Doe",
           "email": "johndoe@example.com",
           "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
           "disabled": False,
       }
   }


   class Token(BaseModel):
       access_token: str
       token_type: str


   class TokenData(BaseModel):
       username: Union[str, None] = None


   class User(BaseModel):
       username: str
       email: Union[str, None] = None
       full_name: Union[str, None] = None
       disabled: Union[bool, None] = None


   class UserInDB(User):
       hashed_password: str


   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

   app = FastAPI()


   def verify_password(plain_password, hashed_password):
       return pwd_context.verify(plain_password, hashed_password)


   def get_password_hash(password):
       return pwd_context.hash(password)


   def get_user(db, username: str):
       if username in db:
           user_dict = db[username]
           return UserInDB(**user_dict)


   def authenticate_user(fake_db, username: str, password: str):
       user = get_user(fake_db, username)
       if not user:
           return False
       if not verify_password(password, user.hashed_password):
           return False
       return user


   def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
       to_encode = data.copy()
       if expires_delta:
           expire = datetime.utcnow() + expires_delta
       else:
           expire = datetime.utcnow() + timedelta(minutes=15)
       to_encode.update({"exp": expire})
       encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
       return encoded_jwt


   async def get_current_user(token: str = Depends(oauth2_scheme)):
       credentials_exception = HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Could not validate credentials",
           headers={"WWW-Authenticate": "Bearer"},
       )
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           username: str = payload.get("sub")
           if username is None:
               raise credentials_exception
           token_data = TokenData(username=username)
       except JWTError:
           raise credentials_exception
       user = get_user(fake_users_db, username=token_data.username)
       if user is None:
           raise credentials_exception
       return user


   async def get_current_active_user(current_user: User = Depends(get_current_user)):
       if current_user.disabled:
           raise HTTPException(status_code=400, detail="Inactive user")
       return current_user


   @app.post("/token", response_model=Token)
   async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
       user = authenticate_user(fake_users_db, form_data.username, form_data.password)
       if not user:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Incorrect username or password",
               headers={"WWW-Authenticate": "Bearer"},
           )
       access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       access_token = create_access_token(
           data={"sub": user.username}, expires_delta=access_token_expires
       )
       return {"access_token": access_token, "token_type": "bearer"}


   @app.get("/users/me/", response_model=User)
   async def read_users_me(current_user: User = Depends(get_current_active_user)):
       return current_user


   @app.get("/users/me/items/")
   async def read_own_items(current_user: User = Depends(get_current_active_user)):
       return [{"item_id": "Foo", "owner": current_user.username}]

其中的SECRET_KEY通过openssl生成：

::

   openssl rand -hex 32

中间件
------

FastAPI这里的中间件，指的是一个函数，它在请求处理前被调用，在响应返回前调用。有点类似于Spring的过滤器filter。

创建中间件：

.. code:: python

   import time

   from fastapi import FastAPI, Request

   app = FastAPI()


   @app.middleware("http")
   async def add_process_time_header(request: Request, call_next):
       start_time = time.time()
       response = await call_next(request)
       process_time = time.time() - start_time
       response.headers["X-Process-Time"] = str(process_time)
       return response

CORS
----

Cross-Origin Resource Sharing，跨域访问。

同域包括协议、域名、端口，以下均是不同域：

-  ``http://localhost``
-  ``https://localhost``
-  ``http://localhost:8080``

使用CORSMiddleware可以实现跨域访问：

.. code:: python

   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware

   app = FastAPI()

   origins = [
       "http://localhost.tiangolo.com",
       "https://localhost.tiangolo.com",
       "http://localhost",
       "http://localhost:8080",
   ]

   app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )


   @app.get("/")
   async def main():
       return {"message": "Hello World"}

-  allow_origins，允许域名，\ ``[*]``\ 代表所有；
-  allow_origin_regex，允许域名的正则匹配；
-  allow_methods，允许请求方法，\ ``[*]``\ 代表所有；
-  allow_headers，允许请求头，\ ``[*]``\ 代表所有；
-  allow_credentials，跨域访问时是否需要cookie，默认False，设置为True时allow_origins不能设置为\ ``[*]``\ ；
-  expose_headers，暴露给浏览器的响应头，默认\ ``[]``\ ；
-  max_age，浏览器最大缓存CORS 响应的时间，默认60s；

SQL关系型数据库
---------------

官方教程使用的是SQLAlchemy。

示例：

::

   .
   └── sql_app
       ├── __init__.py
       ├── crud.py
       ├── database.py
       ├── main.py
       ├── models.py
       └── schemas.py

安装：

::

   pip install sqlalchemy

创建数据库：

.. code:: python

   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
   ## SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

   engine = create_engine(
       SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
   )
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

   Base = declarative_base()

创建数据库模型：

.. code:: python

   from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
   from sqlalchemy.orm import relationship

   from .database import Base


   class User(Base):
       __tablename__ = "users"

       id = Column(Integer, primary_key=True, index=True)
       email = Column(String, unique=True, index=True)
       hashed_password = Column(String)
       is_active = Column(Boolean, default=True)

       items = relationship("Item", back_populates="owner")


   class Item(Base):
       __tablename__ = "items"

       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       description = Column(String, index=True)
       owner_id = Column(Integer, ForeignKey("users.id"))

       owner = relationship("User", back_populates="items")

创建Pydantic模型：

.. code:: python

   from typing import List, Union

   from pydantic import BaseModel


   class ItemBase(BaseModel):
       title: str
       description: Union[str, None] = None


   class ItemCreate(ItemBase):
       pass


   class Item(ItemBase):
       id: int
       owner_id: int

       class Config:
           orm_mode = True


   class UserBase(BaseModel):
       email: str


   class UserCreate(UserBase):
       password: str


   class User(UserBase):
       id: int
       is_active: bool
       items: List[Item] = []

       class Config:
           orm_mode = True

注意，SQLAlchemy使用\ ``=``\ 赋值，Pydantic使用\ ``:``\ 赋值。

增删改查：

.. code:: python

   from sqlalchemy.orm import Session

   from . import models, schemas


   def get_user(db: Session, user_id: int):
       return db.query(models.User).filter(models.User.id == user_id).first()


   def get_user_by_email(db: Session, email: str):
       return db.query(models.User).filter(models.User.email == email).first()


   def get_users(db: Session, skip: int = 0, limit: int = 100):
       return db.query(models.User).offset(skip).limit(limit).all()


   def create_user(db: Session, user: schemas.UserCreate):
       fake_hashed_password = user.password + "notreallyhashed"
       db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
       db.add(db_user)
       db.commit()
       db.refresh(db_user)
       return db_user


   def get_items(db: Session, skip: int = 0, limit: int = 100):
       return db.query(models.Item).offset(skip).limit(limit).all()


   def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
       db_item = models.Item(**item.dict(), owner_id=user_id)
       db.add(db_item)
       db.commit()
       db.refresh(db_item)
       return db_item

主程序：

.. code:: python

   from typing import List

   from fastapi import Depends, FastAPI, HTTPException
   from sqlalchemy.orm import Session

   from . import crud, models, schemas
   from .database import SessionLocal, engine

   models.Base.metadata.create_all(bind=engine)

   app = FastAPI()


   ## Dependency
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()


   @app.post("/users/", response_model=schemas.User)
   def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
       db_user = crud.get_user_by_email(db, email=user.email)
       if db_user:
           raise HTTPException(status_code=400, detail="Email already registered")
       return crud.create_user(db=db, user=user)


   @app.get("/users/", response_model=List[schemas.User])
   def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
       users = crud.get_users(db, skip=skip, limit=limit)
       return users


   @app.get("/users/{user_id}", response_model=schemas.User)
   def read_user(user_id: int, db: Session = Depends(get_db)):
       db_user = crud.get_user(db, user_id=user_id)
       if db_user is None:
           raise HTTPException(status_code=404, detail="User not found")
       return db_user


   @app.post("/users/{user_id}/items/", response_model=schemas.Item)
   def create_item_for_user(
       user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
   ):
       return crud.create_user_item(db=db, item=item, user_id=user_id)


   @app.get("/items/", response_model=List[schemas.Item])
   def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
       items = crud.get_items(db, skip=skip, limit=limit)
       return items

大应用-多文件
-------------

示例目录结构：

::

   .
   ├── app                  # "app" is a Python package
   │   ├── __init__.py      # this file makes "app" a "Python package"
   │   ├── main.py          # "main" module, e.g. import app.main
   │   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
   │   └── routers          # "routers" is a "Python subpackage"
   │   │   ├── __init__.py  # makes "routers" a "Python subpackage"
   │   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
   │   │   └── users.py     # "users" submodule, e.g. import app.routers.users
   │   └── internal         # "internal" is a "Python subpackage"
   │       ├── __init__.py  # makes "internal" a "Python subpackage"
   │       └── admin.py     # "admin" submodule, e.g. import app.internal.admin

APIRouter用于定义子模块的路由：

.. code:: python

   from fastapi import APIRouter

   router = APIRouter()


   @router.get("/users/", tags=["users"])
   async def read_users():
       return [{"username": "Rick"}, {"username": "Morty"}]


   @router.get("/users/me", tags=["users"])
   async def read_user_me():
       return {"username": "fakecurrentuser"}


   @router.get("/users/{username}", tags=["users"])
   async def read_user(username: str):
       return {"username": username}

.. code:: python

   from fastapi import APIRouter, Depends, HTTPException

   from ..dependencies import get_token_header

   router = APIRouter(
       prefix="/items",
       tags=["items"],
       dependencies=[Depends(get_token_header)],
       responses={404: {"description": "Not found"}},
   )


   fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


   @router.get("/")
   async def read_items():
       return fake_items_db


   @router.get("/{item_id}")
   async def read_item(item_id: str):
       if item_id not in fake_items_db:
           raise HTTPException(status_code=404, detail="Item not found")
       return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


   @router.put(
       "/{item_id}",
       tags=["custom"],
       responses={403: {"description": "Operation forbidden"}},
   )
   async def update_item(item_id: str):
       if item_id != "plumbus":
           raise HTTPException(
               status_code=403, detail="You can only update the item: plumbus"
           )
       return {"item_id": item_id, "name": "The great Plumbus"}

在主程序中引入子模块路由：

.. code:: python

   from fastapi import Depends, FastAPI

   from .dependencies import get_query_token, get_token_header
   from .internal import admin
   from .routers import items, users

   app = FastAPI(dependencies=[Depends(get_query_token)])


   app.include_router(users.router)
   app.include_router(items.router)
   app.include_router(
       admin.router,
       prefix="/admin",
       tags=["admin"],
       dependencies=[Depends(get_token_header)],
       responses={418: {"description": "I'm a teapot"}},
   )


   @app.get("/")
   async def root():
       return {"message": "Hello Bigger Applications!"}

后台任务
--------

使用BackgroundTasks定义后台任务：

.. code:: python

   from fastapi import BackgroundTasks, FastAPI

   app = FastAPI()


   def write_notification(email: str, message=""):
       with open("log.txt", mode="w") as email_file:
           content = f"notification for {email}: {message}"
           email_file.write(content)


   @app.post("/send-notification/{email}")
   async def send_notification(email: str, background_tasks: BackgroundTasks):
       background_tasks.add_task(write_notification, email, message="some notification")
       return {"message": "Notification sent in the background"}

BackgroundTasks也能支持依赖注入：

.. code:: python

   from typing import Union

   from fastapi import BackgroundTasks, Depends, FastAPI

   app = FastAPI()


   def write_log(message: str):
       with open("log.txt", mode="a") as log:
           log.write(message)


   def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
       if q:
           message = f"found query: {q}\n"
           background_tasks.add_task(write_log, message)
       return q


   @app.post("/send-notification/{email}")
   async def send_notification(
       email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
   ):
       message = f"message to {email}\n"
       background_tasks.add_task(write_log, message)
       return {"message": "Message sent"}

元数据和文档URL
---------------

设置应用元数据：

.. code:: python

   from fastapi import FastAPI

   description = """
   ChimichangApp API helps you do awesome stuff. 🚀

   ### Items

   You can **read items**.

   ### Users

   You will be able to:

   * **Create users** (_not implemented_).
   * **Read users** (_not implemented_).
   """

   app = FastAPI(
       title="ChimichangApp",
       description=description,
       version="0.0.1",
       terms_of_service="http://example.com/terms/",
       contact={
           "name": "Deadpoolio the Amazing",
           "url": "http://x-force.example.com/contact/",
           "email": "dp@x-force.example.com",
       },
       license_info={
           "name": "Apache 2.0",
           "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
       },
   )


   @app.get("/items/")
   async def read_items():
       return [{"name": "Katana"}]

效果：

|image4|

设置tag元数据：

.. code:: python

   from fastapi import FastAPI

   tags_metadata = [
       {
           "name": "users",
           "description": "Operations with users. The **login** logic is also here.",
       },
       {
           "name": "items",
           "description": "Manage items. So _fancy_ they have their own docs.",
           "externalDocs": {
               "description": "Items external docs",
               "url": "https://fastapi.tiangolo.com/",
           },
       },
   ]

   app = FastAPI(openapi_tags=tags_metadata)


   @app.get("/users/", tags=["users"])
   async def get_users():
       return [{"name": "Harry"}, {"name": "Ron"}]


   @app.get("/items/", tags=["items"])
   async def get_items():
       return [{"name": "wand"}, {"name": "flying broom"}]

添加tag：

.. code:: python

   from fastapi import FastAPI

   tags_metadata = [
       {
           "name": "users",
           "description": "Operations with users. The **login** logic is also here.",
       },
       {
           "name": "items",
           "description": "Manage items. So _fancy_ they have their own docs.",
           "externalDocs": {
               "description": "Items external docs",
               "url": "https://fastapi.tiangolo.com/",
           },
       },
   ]

   app = FastAPI(openapi_tags=tags_metadata)


   @app.get("/users/", tags=["users"])
   async def get_users():
       return [{"name": "Harry"}, {"name": "Ron"}]


   @app.get("/items/", tags=["items"])
   async def get_items():
       return [{"name": "wand"}, {"name": "flying broom"}]

效果：

|image5|

OpenAPI的URL默认是\ ``/openapi.json``\ ，设置\ ``/api/v1/openapi.json``\ ：

::

   from fastapi import FastAPI

   app = FastAPI(openapi_url="/api/v1/openapi.json")


   @app.get("/items/")
   async def read_items():
       return [{"name": "Foo"}]

文档的URL默认是\ ``/docs``\ ，设置为\ ``/documentation``\ ：

.. code:: python

   from fastapi import FastAPI

   app = FastAPI(docs_url="/documentation", redoc_url=None)


   @app.get("/items/")
   async def read_items():
       return [{"name": "Foo"}]

静态文件
--------

使用\ ``StaticFiles``\ ：

.. code:: python

   from fastapi import FastAPI
   from fastapi.staticfiles import StaticFiles

   app = FastAPI()

   app.mount("/static", StaticFiles(directory="static"), name="static")

FastAPI会自动挂载静态文件。

单元测试
--------

使用pytest和TestClient：

.. code:: python

   from fastapi import FastAPI
   from fastapi.testclient import TestClient

   app = FastAPI()


   @app.get("/")
   async def read_main():
       return {"msg": "Hello World"}


   client = TestClient(app)


   def test_read_main():
       response = client.get("/")
       assert response.status_code == 200
       assert response.json() == {"msg": "Hello World"}

单元测试文件拆出来：

::

   .
   ├── app
   │   ├── __init__.py
   │   ├── main.py
   │   └── test_main.py

.. code:: python

   from fastapi import FastAPI

   app = FastAPI()


   @app.get("/")
   async def read_main():
       return {"msg": "Hello World"}

.. code:: python

   from fastapi.testclient import TestClient

   from .main import app

   client = TestClient(app)


   def test_read_main():
       response = client.get("/")
       assert response.status_code == 200
       assert response.json() == {"msg": "Hello World"}

调试
----

通常借助PyCharm打断点调试：

|image6|

   参考资料：

   官方教程 https://fastapi.tiangolo.com/tutorial/

   示例项目 https://fastapi.tiangolo.com/project-generation/

.. |image1| image:: ../wanggang.png
.. |image2| image:: 006002-【FastAPI】FastAPI官方教程太棒了（下）/image04.png
.. |image3| image:: 006002-【FastAPI】FastAPI官方教程太棒了（下）/image05.png
.. |image4| image:: 006002-【FastAPI】FastAPI官方教程太棒了（下）/image01.png
.. |image5| image:: 006002-【FastAPI】FastAPI官方教程太棒了（下）/image02.png
.. |image6| image:: 006002-【FastAPI】FastAPI官方教程太棒了（下）/image02.png
