【HttpRunner】HttpRunner3的HTTP请求是怎么发出去的
=================================================

|image1|

在HttpRunner3的示例代码中，发送HTTP请求的代码是这样写的：

.. code:: python

   from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


   class TestCaseBasic(HttpRunner):

       config = Config("basic test with httpbin").base_url("https://httpbin.org/")

       teststeps = [
           Step(
               RunRequest("headers")
               .get("/headers")
               .validate()
               .assert_equal("status_code", 200)
               .assert_equal("body.headers.Host", "httpbin.org")
           ),
           # 省略
           Step(
               RunRequest("post data")
               .post("/post")
               .with_headers(**{"Content-Type": "application/json"})
               .with_data("abc")
               .validate()
               .assert_equal("status_code", 200)
           ),
           # 省略
       ]


   if __name__ == "__main__":
       TestCaseBasic().test_start()

-  类TestCaseBasic继承了类HttpRunner。
-  在类TestCaseBasic的内部定义了teststeps列表，由多个Step类的实例对象组成。
-  类Step初始化传入类RunRequest的方法get和post就把HTTP请求发出去了。

这到底是怎么实现的？

先看下RunRequest的源码：

.. code:: python

   class RunRequest(object):
       def __init__(self, name: Text):
           self.__step_context = TStep(name=name)

       def with_variables(self, **variables) -> "RunRequest":
           self.__step_context.variables.update(variables)
           return self

       def setup_hook(self, hook: Text, assign_var_name: Text = None) -> "RunRequest":
           if assign_var_name:
               self.__step_context.setup_hooks.append({assign_var_name: hook})
           else:
               self.__step_context.setup_hooks.append(hook)

           return self

       def get(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.GET, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def post(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.POST, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def put(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.PUT, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def head(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.HEAD, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def delete(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.DELETE, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def options(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.OPTIONS, url=url)
           return RequestWithOptionalArgs(self.__step_context)

       def patch(self, url: Text) -> RequestWithOptionalArgs:
           self.__step_context.request = TRequest(method=MethodEnum.PATCH, url=url)
           return RequestWithOptionalArgs(self.__step_context)

里面定义了get、post等HTTP请求的Method。方法内部：

.. code:: python

   self.__step_context.request = TRequest(method=MethodEnum.GET, url=url)

有个TRequest类：

.. code:: python

   class TRequest(BaseModel):
       """requests.Request model"""

       method: MethodEnum
       url: Url
       params: Dict[Text, Text] = {}
       headers: Headers = {}
       req_json: Union[Dict, List, Text] = Field(None, alias="json")
       data: Union[Text, Dict[Text, Any]] = None
       cookies: Cookies = {}
       timeout: float = 120
       allow_redirects: bool = True
       verify: Verify = False
       upload: Dict = {}  # used for upload files

它继承了\ **pydantic.BaseModel，是用来做数据验证的**\ ，比如这里的url指定了Url类型，如果传一个str类型，就会校验失败。简而言之，这是给代码规范用的，没有实际的业务功能。

下面有一行注释：requests.Request mode，看来这个跟requests有点关系。

回过头来看看\ ``self.__step_context.request``\ ，也就是\ ``self.__step_context``\ 对象有个request属性，它的定义是：

.. code:: python

   self.__step_context = TStep(name=name)

答案应该就在TStep中了：

.. code:: python

   class TStep(BaseModel):
       name: Name
       request: Union[TRequest, None] = None
       testcase: Union[Text, Callable, None] = None
       variables: VariablesMapping = {}
       setup_hooks: Hooks = []
       teardown_hooks: Hooks = []
       # used to extract request's response field
       extract: VariablesMapping = {}
       # used to export session variables from referenced testcase
       export: Export = []
       validators: Validators = Field([], alias="validate")
       validate_script: List[Text] = []

还是个Model，里面的request定义是：

.. code:: python

   request: Union[TRequest, None] = None

又绕回TRequest了。这个\ **Union是typing模块里面的：Union[X, Y] means
either X or Y.** 意思就是request的类型要么是TRequest要么是None。

在刚才get的方法中，还有一句\ ``return RequestWithOptionalArgs(self.__step_context)``\ ，RequestWithOptionalArgs的定义如下：

.. code:: python

   class RequestWithOptionalArgs(object):
       def __init__(self, step_context: TStep):
           self.__step_context = step_context

       def with_params(self, **params) -> "RequestWithOptionalArgs":
           self.__step_context.request.params.update(params)
           return self

       def with_headers(self, **headers) -> "RequestWithOptionalArgs":
           self.__step_context.request.headers.update(headers)
           return self

       def with_cookies(self, **cookies) -> "RequestWithOptionalArgs":
           self.__step_context.request.cookies.update(cookies)
           return self

       def with_data(self, data) -> "RequestWithOptionalArgs":
           self.__step_context.request.data = data
           return self

       def with_json(self, req_json) -> "RequestWithOptionalArgs":
           self.__step_context.request.req_json = req_json
           return self

       def set_timeout(self, timeout: float) -> "RequestWithOptionalArgs":
           self.__step_context.request.timeout = timeout
           return self

       def set_verify(self, verify: bool) -> "RequestWithOptionalArgs":
           self.__step_context.request.verify = verify
           return self

       def set_allow_redirects(self, allow_redirects: bool) -> "RequestWithOptionalArgs":
           self.__step_context.request.allow_redirects = allow_redirects
           return self

       def upload(self, **file_info) -> "RequestWithOptionalArgs":
           self.__step_context.request.upload.update(file_info)
           return self

       def teardown_hook(
           self, hook: Text, assign_var_name: Text = None
       ) -> "RequestWithOptionalArgs":
           if assign_var_name:
               self.__step_context.teardown_hooks.append({assign_var_name: hook})
           else:
               self.__step_context.teardown_hooks.append(hook)

           return self

       def extract(self) -> StepRequestExtraction:
           return StepRequestExtraction(self.__step_context)

       def validate(self) -> StepRequestValidation:
           return StepRequestValidation(self.__step_context)

       def perform(self) -> TStep:
           return self.__step_context

可以给HTTP请求添加params、headers等可选项。

看到这里，仍然不知道HTTP请求到底发出去的，因为没有调用呀。

只能往上层找，看调用RunRequest的Step类：

.. code:: python

   class Step(object):
       def __init__(
           self,
           step_context: Union[
               StepRequestValidation,
               StepRequestExtraction,
               RequestWithOptionalArgs,
               RunTestCase,
               StepRefCase,
           ],
       ):
           self.__step_context = step_context.perform()

       @property
       def request(self) -> TRequest:
           return self.__step_context.request

       @property
       def testcase(self) -> TestCase:
           return self.__step_context.testcase

       def perform(self) -> TStep:
           return self.__step_context

Step类的\ ``__init__``\ 方法也用Union做了类型校验，其中RequestWithOptionalArgs就是RunRequest的gei等方法会返回的，这倒是匹配上了。它还有个request属性。有点眉目了。

再往上层找，看HttpRunner类，有个\ ``__run_step_request``\ 的方法：

.. code:: python

   def __run_step_request(self, step: TStep) -> StepData:
       """run teststep: request"""
       step_data = StepData(name=step.name)

       # parse
       prepare_upload_step(step, self.__project_meta.functions)
       request_dict = step.request.dict()
       request_dict.pop("upload", None)
       parsed_request_dict = parse_data(
           request_dict, step.variables, self.__project_meta.functions
       )
       parsed_request_dict["headers"].setdefault(
           "HRUN-Request-ID",
           f"HRUN-{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
       )
       step.variables["request"] = parsed_request_dict

       # setup hooks
       if step.setup_hooks:
           self.__call_hooks(step.setup_hooks, step.variables, "setup request")

       # prepare arguments
       method = parsed_request_dict.pop("method")
       url_path = parsed_request_dict.pop("url")
       url = build_url(self.__config.base_url, url_path)
       parsed_request_dict["verify"] = self.__config.verify
       parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})

       # request
       resp = self.__session.request(method, url, **parsed_request_dict)
       resp_obj = ResponseObject(resp)
       step.variables["response"] = resp_obj

       # teardown hooks
       if step.teardown_hooks:
           self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

       def log_req_resp_details():
           err_msg = "\n{} DETAILED REQUEST & RESPONSE {}\n".format("*" * 32, "*" * 32)

           # log request
           err_msg += "====== request details ======\n"
           err_msg += f"url: {url}\n"
           err_msg += f"method: {method}\n"
           headers = parsed_request_dict.pop("headers", {})
           err_msg += f"headers: {headers}\n"
           for k, v in parsed_request_dict.items():
               v = utils.omit_long_data(v)
               err_msg += f"{k}: {repr(v)}\n"

           err_msg += "\n"

           # log response
           err_msg += "====== response details ======\n"
           err_msg += f"status_code: {resp.status_code}\n"
           err_msg += f"headers: {resp.headers}\n"
           err_msg += f"body: {repr(resp.text)}\n"
           logger.error(err_msg)

       # extract
       extractors = step.extract
       extract_mapping = resp_obj.extract(extractors)
       step_data.export_vars = extract_mapping

       variables_mapping = step.variables
       variables_mapping.update(extract_mapping)

       # validate
       validators = step.validators
       session_success = False
       try:
           resp_obj.validate(
               validators, variables_mapping, self.__project_meta.functions
           )
           session_success = True
       except ValidationFailure:
           session_success = False
           log_req_resp_details()
           # log testcase duration before raise ValidationFailure
           self.__duration = time.time() - self.__start_at
           raise
       finally:
           self.success = session_success
           step_data.success = session_success

           if hasattr(self.__session, "data"):
               # httprunner.client.HttpSession, not locust.clients.HttpSession
               # save request & response meta data
               self.__session.data.success = session_success
               self.__session.data.validators = resp_obj.validation_results

               # save step data
               step_data.data = self.__session.data

       return step_data

就是这里了，它的函数名用了双下划线开头：\ **双下划线前缀**\ 会让Python解释器重写属性名称，以避免子类中的命名冲突。
这也称为名称改写（name
mangling），即解释器会更改变量的名称，以便在稍后扩展这个类时避免命名冲突。说人话就是，\ **类的私有成员，只能在类的内部调用，不对外暴露**\ 。它只在\ ``__run_step()``\ 方法中调用了1次：\ ``step_data = self.__run_step_request(step)``\ 。

中间有一段：

.. code:: python

   ## request
   resp = self.__session.request(method, url, **parsed_request_dict)
   resp_obj = ResponseObject(resp)
   step.variables["response"] = resp_obj

好家伙，\ ``self.__session.request()``\ ，跟reqeusts那个有点像了。点进去。

一下就跳转到了\ ``httprunner.client.py``\ ，\ **众里寻他千百度，默然回首，它竟然就在client**\ 。

.. code:: python

   class HttpSession(requests.Session):
       """
       Class for performing HTTP requests and holding (session-) cookies between requests (in order
       to be able to log in and out of websites). Each request is logged so that HttpRunner can
       display statistics.

       This is a slightly extended version of `python-request <http://python-requests.org>`_'s
       :py:class:`requests.Session` class and mostly this class works exactly the same.
       """

       def __init__(self):
           super(HttpSession, self).__init__()
           self.data = SessionData()

       def update_last_req_resp_record(self, resp_obj):
           """
           update request and response info from Response() object.
           """
           # TODO: fix
           self.data.req_resps.pop()
           self.data.req_resps.append(get_req_resp_record(resp_obj))

       def request(self, method, url, name=None, **kwargs):

继承了requests.Session然后进行了重写。

**果然，还是用到了requests库。**

   参考资料：

   https://github.com/httprunner/httprunner

.. |image1| image:: ../wanggang.png
