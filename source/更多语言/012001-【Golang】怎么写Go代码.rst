【Golang】怎么写Go代码
======================

|image1|

安装过程略过，网上搜一大把。

介绍
----

本文会在一个module中开发一个简单的Go package。

同时介绍go tool（也就是go命令行）。

以及如何fetch，build和install Go的modules，packages，commands。

代码组织
--------

Go是按packages来组织代码的。一个package == 一个目录。

同一个package中的functions，types，variables，和constants是共享的。也就是包访问权限，java默认也是包访问权限。

packages是放在module中的，module是通过\ ``go.mod``\ 文件来定义的。典型的，一个repository只有一个\ ``go.mod``\ ，放在根目录。

可以使用\ ``go mod init name``\ 来创建这个文件。在go
run后会生成\ ``go.sum``\ 文件，内容是\ ``go.mod``\ 的加密哈希。

repository也允许有多个module，module的packages是\ ``go.mod``\ 所在的目录，如果子目录也有\ ``go.mod``\ ，那么这个子目录的packages就属于子目录module。

第一个程序
----------

假设module path是\ *example.com/user/hello*\ ，

.. code:: shell

   $ mkdir hello # Alternatively, clone it if it already exists in version control.
   $ cd hello
   $ go mod init example.com/user/hello
   go: creating new go.mod: module example.com/user/hello
   $ cat go.mod
   module example.com/user/hello

   go 1.14
   $

Go源文件的第一个语句必须是package *name*\ 。程序入口必须是package
*main*\ 。

.. code:: go

   package main

   import "fmt"

   func main() {
       fmt.Println("Hello, world.")
   }

喜闻乐见Hello World。

现在可以build和install，

.. code:: shell

   $ go install example.com/user/hello
   $

这条命令会build然后生成可执行二进制文件（这是我比较喜欢Go的一个原因，直接生成可执行文件，省去了安装依赖的麻烦）。

``build``\ 和\ ``install``\ 命令都可以生成可执行文件。不同点在于

-  go build 不能生成包文件, go install 可以生成包文件
-  go build 生成可执行文件在当前目录下， go install
   生成可执行文件在bin目录下

install生成文件的bin目录是根据环境变量来的。按以下顺序检查

-  GOBIN
-  GOPATH

如果都没有设置，就会生成到默认GOPATH（Linux ``$HOME/go`` 或Windows
``%USERPROFILE%\go``\ ）。

示例的二进制文件会生成到\ ``$HOME/go/bin/hello``\ （Windows的话就是\ ``%USERPROFILE%\go\bin\hello.exe``\ ）。

可以查看环境变量GOBIN和GOPATH的值

.. code:: shell

   go env

也可以设置\ ``GOBIN``

.. code:: shell

   $ go env -w GOBIN=/somewhere/else/bin
   $

设置后可以重置

.. code:: shell

   $ go env -u GOBIN
   $

``GOPATH``\ 需要到系统环境变量进行修改。

install等命令需要在源文件目录下执行，准确点说是“当前工作目录”。否则会报错。

在当前目录执行，以下等价

.. code:: shell

   $ go install example.com/user/hello

.. code:: shell

   $ go install .

.. code:: shell

   $ go install

验证下结果，为了方便，添加install目录到\ ``PATH``

.. code:: shell

   ## Windows users should consult https://github.com/golang/go/wiki/SettingGOPATH
   ## for setting %PATH%.
   $ export PATH=$PATH:$(dirname $(go list -f '{{.Target}}' .))
   $ hello
   Hello, world.
   $

如果cd到了install的bin目录，也可以直接

.. code:: shell

   $ hello
   Hello, world.
   $

现阶段Go的很多库都是放在GitHub等代码托管网站上面的，使用Git进行提交

.. code:: shell

   $ git init
   Initialized empty Git repository in /home/user/hello/.git/
   $ git add go.mod hello.go
   $ git commit -m "initial commit"
   [master (root-commit) 0b4507d] initial commit
    1 file changed, 7 insertion(+)
    create mode 100644 go.mod hello.go
   $

Go命令通过请求相应的HTTPS
URL，并读取嵌入在HTML响应中的元数据<meta>标签，来定位包含给定module
path的repository

.. code:: go

   Bitbucket (Git, Mercurial)

       import "bitbucket.org/user/project"
       import "bitbucket.org/user/project/sub/directory"

   GitHub (Git)

       import "github.com/user/project"
       import "github.com/user/project/sub/directory"

   Launchpad (Bazaar)

       import "launchpad.net/project"
       import "launchpad.net/project/series"
       import "launchpad.net/project/series/sub/directory"

       import "launchpad.net/~user/project/branch"
       import "launchpad.net/~user/project/branch/sub/directory"

   IBM DevOps Services (Git)

       import "hub.jazz.net/git/user/project"
       import "hub.jazz.net/git/user/project/sub/directory"

很多托管网站已经为Go的repository提供了元数据，为了共享module，最简单的办法就是让module
path匹配repository的URL。

从module import packages
------------------------

先在名字为morestrings的package中创建一个\ ``reverse.go``\ 文件，实现字符串反转

.. code:: go

   // Package morestrings implements additional functions to manipulate UTF-8
   // encoded strings, beyond what is provided in the standard "strings" package.
   package morestrings

   // ReverseRunes returns its argument string reversed rune-wise left to right.
   func ReverseRunes(s string) string {
       r := []rune(s)
       for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r)
   }

由于ReverseRunes函数是大写的，所以是公有的，可以被其他packages import。

先build测试下编译成功

.. code:: shell

   $ cd $HOME/hello/morestrings
   $ go build
   $

因为只是在package中，不是在module根目录，\ ``go build``\ 不会生成文件，而是会把compile后的package保存到local
build cache中。

接着在hello.go中import

.. code:: go

   package main

   import (
       "fmt"

       "example.com/user/hello/morestrings"
   )

   func main() {
       fmt.Println(morestrings.ReverseRunes("!oG ,olleH"))
   }

然后install hello

.. code:: shell

   $ go install example.com/user/hello

验证，import成功，字符串反转

.. code:: shell

   $ hello
   Hello, Go!

从远程remore modules import packages
------------------------------------

可以用import path通过版本控制系统来获取package源码，如Git或Mercurial。

示例，使用\ ``github.com/google/go-cmp/cmp``

.. code:: go

   package main

   import (
       "fmt"

       "example.com/user/hello/morestrings"
       "github.com/google/go-cmp/cmp"
   )

   func main() {
       fmt.Println(morestrings.ReverseRunes("!oG ,olleH"))
       fmt.Println(cmp.Diff("Hello World", "Hello Go"))
   }

当运行命令\ ``go install`` ``go build``
``go run``\ 的时候，go命令会自动下载远程module，然后写到\ ``go.mod``\ 文件中

.. code:: shell

   $ go install example.com/user/hello
   go: finding module for package github.com/google/go-cmp/cmp
   go: downloading github.com/google/go-cmp v0.4.0
   go: found github.com/google/go-cmp/cmp in github.com/google/go-cmp v0.4.0
   $ hello
   Hello, Go!
     string(
   -   "Hello World",
   +   "Hello Go",
     )
   $ cat go.mod
   module example.com/user/hello

   go 1.14

   require github.com/google/go-cmp v0.4.0
   $

国内容易超时，可以使用代理走国内镜像

七牛云

.. code:: shell

   go env -w GO111MODULE=on
   go env -w GOPROXY=https://goproxy.cn,direct

阿里云

.. code:: shell

   go env -w GO111MODULE=on
   go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct

module依赖会自动下载到\ ``GOPATH``\ 指定目录的\ *pkg/mod*\ 子目录。

module指定版本的下载内容，是在所有其他require这个版本的modules中共享的，所以go命令会标记这些文件和目录为只读的。

可以使用命令删除所有下载的modules

.. code:: shell

   $ go clean -modcache
   $

测试
----

Go有个轻量的测试框架，\ ``go test``\ 和\ *testing package*\ 。

测试框架识别以\ ``_test.go``\ 结尾的文件，包含\ *TestXXX*\ 命名的函数，函数签名\ ``func (t *testing.T)``\ 。如果函数调用失败如\ ``t.Error``
或 ``t.Fail``\ ，那么test就会失败。

示例，新建\ *$HOME/hello/morestrings/reverse_test.go*\ 文件，添加\ ``morestrings``
package的测试代码

.. code:: go

   package morestrings

   import "testing"

   func TestReverseRunes(t *testing.T) {
       cases := []struct {
           in, want string
       }{
           {"Hello, world", "dlrow ,olleH"},
           {"Hello, 世界", "界世 ,olleH"},
           {"", ""},
       }
       for _, c := range cases {
           got := ReverseRunes(c.in)
           if got != c.want {
               t.Errorf("ReverseRunes(%q) == %q, want %q", c.in, got, c.want)
           }
       }
   }

运行测试

.. code:: shell

   $ go test
   PASS
   ok      example.com/user/morestrings 0.165s
   $

.. |image1| image:: ../wanggang.png
