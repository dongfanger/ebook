# 【Golang】Dockerfile文件万字全面解析
![](../wanggang.png)

`Dockerfile`是一个文本文件，包含一些Docker指令。执行`docker build`，Docker就会执行`Dockerfile`里面的指令，来自动创建镜像。

## 用法

![](012003-【Golang】Dockerfile文件万字全面解析/image-20200822110105335_副本.png)

Dockerfile里面的指令可以访问context这些文件。

context是递归的，`PATH`包含所有子目录，`URL`包含所有子模块。

例子，把当前目录当做context，

```shell
$ docker build .

Sending build context to Docker daemon  6.51 MB
...
```

build是由Docker daemon(守护进程)来运行，而不是CLI。

build会把整个context发给daemon。所以最好把context设置为空目录，把Dockerfile放进去。只添加需要的文件，为了提高build性能，还可以添加`.dockerignore`来排除一些文件和目录。

Warning！不要用系统根目录`/`作为PATH，不然会把根目录下所有东西都传给Docker daemon。

一般会把Dockerfile放在context根目录下，也可以使用`-f`来指定其他路径，

```shell
$ docker build -f /path/to/a/Dockerfile .
```

指定镜像存放仓库可以使用`-t`，

```shell
$ docker build -t shykes/myapp .
```

支持多个，

```shell
$ docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .
```

Docker daemon在执行Dockfile的指令前，会做检查，如果有语法错误会报错，

```shell
$ docker build -t test/myapp .

Sending build context to Docker daemon 2.048 kB
Error response from daemon: Unknown instruction: RUNCMD
```

Docker daemon执行指令，是一个一个执行，一个一个提交的。执行结束会生成镜像ID。自动清理context。

`RUN cd /tmp`是无效的，因为daemon是独立执行每条指令的，不会作用到后面的指令。

为了加速build过程，Docker会重复使用中间镜像(缓存)，在console日志中可以看到`Using cache`，

```shell
$ docker build -t svendowideit/ambassador .

Sending build context to Docker daemon 15.36 kB
Step 1/4 : FROM alpine:3.2
 ---> 31f630c65071
Step 2/4 : MAINTAINER SvenDowideit@home.org.au
 ---> Using cache
 ---> 2a1c91448f5f
Step 3/4 : RUN apk update &&      apk add socat &&        rm -r /var/cache/
 ---> Using cache
 ---> 21ed6e7fbb73
Step 4/4 : CMD env | grep _TCP= | (sed 's/.*_PORT_\([0-9]*\)_TCP=tcp:\/\/\(.*\):\(.*\)/socat -t 100000000 TCP4-LISTEN:\1,fork,reuseaddr TCP4:\2:\3 \&/' && echo wait) | sh
 ---> Using cache
 ---> 7ea8aef582cc
Successfully built 7ea8aef582cc
```

cache来源于之前本地build过的镜像，或者使用`docker load`加载的镜像。

如果想直接指定一个镜像作为cache，可以使用`--cache-from`。

## 格式

'''
## Comment
INSTRUCTION arguments
```

`#`开头是注释或者parser directive（提示解析器做特殊处理）。

指令是忽略大小写的，不过为了和参数区分，一般全大写。

Dockerfile从上往下顺序执行指令，第一条指令必须是`FROM`，定义build的parent image（父镜像）。没有parent的镜像叫base image。

![](012003-【Golang】Dockerfile文件万字全面解析/2-3_副本.png)

参数里面的`#`就不是注释了，是参数的一部分，

'''
## Comment
RUN echo 'we are running some # of cool things'
```

注释在Dockerfile指令执行前，会被移除。以下是等价的，

'''
RUN echo hello \
## comment
world
```

'''
RUN echo hello \
world
```

注意，注释不支持换行符`\`。

注释和指令前面的空格会被忽略，以下是等价的，

'''
        # this is a comment-line
    RUN echo hello
RUN echo world
```

'''
## this is a comment-line
RUN echo hello
RUN echo world
```

但是参数里面的空格，是会被保留的，

'''
RUN echo "\
     hello\
     world"
```

## Parser directives

'''
## directive=value
```

Parser directives是一种特殊的注释，用来提示解析器做特殊处理。

但是Parser directives并不会添加layers到build中，也不会被识别为build step。

如果注释、空行、或者指令被运行后，Docker就不会再识别Parser directives了，所以必须把Parser directives放在Dockerfile的最前面的最前面。

Parser directives是忽略大小写的，不过一般约定为全小写。同时约定随后跟一个空行。

Parser directives不支持换行符。

以下是一些无效示例，

无效--换行符

'''
## direc \
tive=value
```

无效--出现了2次

'''
## directive=value1
## directive=value2

FROM ImageName
```

无效--在指令之后就是普通的注释

'''
FROM ImageName
## directive=value
```

无效--在普通注释之后也变成了普通注释

'''
## About my dockerfile
## directive=value
FROM ImageName
```

无效--未知命令会被视为普通注释，普通注释之后也是普通注释

'''
## unknowndirective=value
## knowndirective=value
```

Parser directives同一行的空格会被忽略，以下是等价的，

'''
#directive=value
## directive =value
#	directive= value
## directive = value
#	  dIrEcTiVe=value
```

目前支持2个Parser directives，

- `syntax`，依赖BuildKit
- `escape`

### escape

反斜杠（默认）

'''
## escape=\
```

或者反引号

```
## escape=`
```

用来指定转义符。这个在Windows系统很有用，因为`\`在Windows是路径分隔符。

比如，

```
FROM microsoft/nanoserver
COPY testfile.txt c:\\
RUN dir c:\
```

会执行失败，

```sh
PS C:\John> docker build -t cmd .
Sending build context to Docker daemon 3.072 kB
Step 1/2 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/2 : COPY testfile.txt c:\RUN dir c:
GetFileAttributesEx c:RUN: The system cannot find the file specified.
PS C:\John>
```

使用escape可以替换`\`为`

```
## escape=`

FROM microsoft/nanoserver
COPY testfile.txt c:\
RUN dir c:\
```

执行成功，

```shell
PS C:\John> docker build -t succeeds --no-cache=true .
Sending build context to Docker daemon 3.072 kB
Step 1/3 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/3 : COPY testfile.txt c:\
 ---> 96655de338de
Removing intermediate container 4db9acbb1682
Step 3/3 : RUN dir c:\
 ---> Running in a2c157f842f5
 Volume in drive C has no label.
 Volume Serial Number is 7E6D-E0F7

 Directory of c:\

10/05/2016  05:04 PM             1,894 License.txt
10/05/2016  02:22 PM    <DIR>          Program Files
10/05/2016  02:14 PM    <DIR>          Program Files (x86)
10/28/2016  11:18 AM                62 testfile.txt
10/28/2016  11:20 AM    <DIR>          Users
10/28/2016  11:20 AM    <DIR>          Windows
           2 File(s)          1,956 bytes
           4 Dir(s)  21,259,096,064 bytes free
 ---> 01c7f3bef04f
Removing intermediate container a2c157f842f5
Successfully built 01c7f3bef04f
PS C:\John>
```

## 环境替换

环境变量（使用`ENV`指令来定义环境变量）能够用在指令中作为变量，被`Dockerfile`解释。还可以处理转义符，以便在语句中照字面值地包含variable-like语法。

使用`$variable_name`或`${variable_name}`来引用环境变量。

可以使用双括弧和下划线来命名，如`${foo}_bar`。同时支持`bash`修饰符，

- `${variable:-word}` set `variable`后就是set的值，没有set `variable`值就是`word`
- `${variable:+word}` set `variable`后值就是`word`，没有set `variable`就是空字符串

word既可以是string，也可以是另外一个环境变量。

可以在变量前加转义符，比如`\$foo` ，`\${foo}`会被分别转义为`$foo` 和`${foo}`。

示例，

```
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```

Dockerfile的一下指令都支持环境变量

- `ADD`
- `COPY`
- `ENV`
- `EXPOSE`
- `FROM`
- `LABEL`
- `STOPSIGNAL`
- `USER`
- `VOLUME`
- `WORKDIR`
- `ONBUILD` (结合以上指令使用)

需要注意的是，变量替换是针对整条指令的，

```
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```

`def`的值是hello，而不是bye，因为上一条指令赋值的hello。

`ghi`的值才会是bye。

## .dockerignore file

`.dockerignore`文件位于context根目录，会把匹配到的文件和目录排除在context之外。

这样就可以在使用`ADD`和`COPY`命令时，避免把一些大文件或者敏感信息文件和目录，发送到Docker daemon。

context是由`PATH`和`URL`定义的，所以`.dockerignore`文件会匹配这2个路径。

`/foo/bar` == `foo/bar`

示例，

```
## comment
*/temp*
*/*/temp*
temp?
```

| Rule        | Behavior                                                     |
| :---------- | :----------------------------------------------------------- |
| `# comment` | 注释忽略                                                     |
| `*/temp*`   | 排除root的子目录下，`temp`开头的文件和目录。 <br />如`/somedir/temporary.txt` 和 `/somedir/temp` |
| `*/*/temp*` | 排除root的**二层**目录下，`temp`开头的文件和目录。<br />如 `/somedir/subdir/temporary.txt` |
| `temp?`     | 排除root下， `temp`+1个字符的文件和目录。<br />如 `/tempa` 和`/tempb` |

匹配遵循Go语言的[filepath.Match](http://golang.org/pkg/path/filepath#Match)规则。

Docker还支持`**`，匹配任意数量的目录（包括0）。如`**/*.go`排除`.go`结尾的，包括context root下所有目录。

如果排除了一堆文件后，想只包含其中几个文件，可以使用异常规则`!`。

示例，排除`.md`结尾的文件，包含`README.md`，

```
*.md
!README.md
```

`README-secret.md`不会被排除，因为`!README*.md`能匹配到`README-secret.md`，又把`README-secret.md`包含进来了。

`.dockerignore`文件甚至可以排除`Dockerfile` 和`.dockerignore`，然而并没有什么卵用，这些文件还是会被发送到Docker daemon，只是`ADD`和`COPY`命令不会把它们复制到镜像了。

## FROM

`FROM`指令初始化一个新的buid stage，为后面的指令设置Parent Image。

'''
FROM [--platform=<platform>] <image> [AS <name>]
```

或

'''
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```

或

'''
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

`--platform`，用来定义image的平台，如`linux/amd64`, `linux/arm64`, 或者`windows/amd64`，这样就能支持多平台镜像。

`tag` `digest`是可选的，都不填时，默认用最新的tag。如果找不到tag，builder就会报错。

`AS name`可以给image取个别名，在后续`FROM`和`COPY --from=<name|index>`指令中可以使用这个别名。

可以在一个Dockerfile文件中使用多个`FROM`。每个`FROM`都会把上个指令创建的状态清除。所以在每个新的`FROM`指令之前，记录commit输出的最后一个image ID。

`ARG`是唯一能在`FROM`之前的指令。

比如`--platform`，默认情况下，会使用build请求的默认平台。也可以使用全局build参数，通过`automatic platform ARGs`（依赖BuildKit）来强制把stage指定为本地build平台（`--platform=$BUILDPLATFORM`），然后用它来在stage中cross-compile目标平台。

`FROM`和`ARG`怎么结合使用呢？

`FROM`指令支持出现在第一个`FROM`之前的`ARG`声明的变量。

'''
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

`FROM`之前声明的`ARG`是在build stage之外的，所以它不能用在`FROM`后的任何指令中。如果要用，可以使用在build stage中的不带value的`ARG`指令，

'''
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```

## RUN

- `RUN <command>` (*shell* 格式，Linux `/bin/sh -c`  Windows`cmd /S /C`)
- `RUN ["executable", "param1", "param2"]` (*exec* 格式)

`RUN`指令会在当前镜像之上的新layer中执行命令，commit结果，commit后的镜像会在`Dockerfile`的下一个step中使用。

`RUN`指令的commits符合Docker理念，commit is cheap，containers可以从image历史中任何记录创建，就像source control。

可以使用不同的`SHELL`，

**shell格式**

'''
RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'
```

**exec格式**

'''
RUN ["/bin/bash", "-c", "echo hello"]
```

shell格式会调用command shell，而exec格式不会，所以exec中`$HOME`是没用的，要用的话直接执行shell `RUN [ "sh", "-c", "echo $HOME" ]`。

注意，exec格式被解析为JSON数组，所以只能用双引号。还需注意反斜杠，

错误

'''
RUN ["c:\windows\system32\tasklist.exe"]
```

正确

'''
RUN ["c:\\windows\\system32\\tasklist.exe"]
```

默认是会启动`RUN`的缓存的，比如`RUN apt-get dist-upgrade -y`会在下次build的时候复用。可以使用`docker build --no-cache`来禁用缓存。

使用`ADD`和`COPY`指令也可以禁用`RUN`缓存。

## CMD

`CMD`和`RUN`是不同的。`RUN`指令是在build过程中执行command和commit结果。`CMD`在build时不会执行任何command，而是为image定义command，在container（镜像创建的容器）启动的时候执行。

- `CMD ["executable","param1","param2"]` (*exec* 格式，首选)
- `CMD ["param1","param2"]` (*ENTRYPOINT*默认参数)
- `CMD command param1 param2` (*shell* 格式)

一个`Dockerfile`只能有一个`CMD`指令，如果有多个，只有最后一个生效。

shell格式会调用command shell，而exec格式不会，所以exec中`$HOME`是没用的，要用的话直接执行shell `RUN [ "sh", "-c", "echo $HOME" ]`。

注意，exec格式被解析为JSON数组，所以只能用双引号。还需注意反斜杠。

如果想要container每次运行相同的可执行文件，需要结合 `ENTRYPOINT`使用。

如果`docker run`定义了参数，那么会覆盖`CMD`定义。

## LABEL

'''
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

`LABEL`用来给image添加metadata，是key-value键值对的形式。

示例，

'''
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

一个image可以有多个label，一个label可以有多个键值对，以下是等价的，

'''
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

'''
LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```

label会随着image继承，从base image或parent image继承到当前image。

重复的label，会用最新的覆盖旧的。

可以使用命令查看image的labels，

```shell
docker image inspect --format='' myimage
```

```json
{
  "com.example.vendor": "ACME Incorporated",
  "com.example.label-with-value": "foo",
  "version": "1.0",
  "description": "This text illustrates that label-values can span multiple lines.",
  "multi.label1": "value1",
  "multi.label2": "value2",
  "other": "value3"
}
```

## MAINTAINER 

`MAINTAINER `已经弃用了，直接使用`LABLE`，

'''
LABEL maintainer="SvenDowideit@home.org.au"
```

## EXPOSE

'''
EXPOSE <port> [<port>/<protocol>...]
```

`EXPOSE`定义了container监听的网络端口，支持TCP和UDP，默认TCP。

`EXPOSE`并不真正的发布端口，而只是一种预定义。

真正发布是在`docker run`的时候，使用`-p`或`-P`来发布。

`-p`发布一个或多个端口，`-P`发布全部，并映射到高位端口。

示例，默认TCP，可以定义UDP，

'''
EXPOSE 80/udp
```

也可以同时定义TCP和UDP，

'''
EXPOSE 80/tcp
EXPOSE 80/udp
```

如果这里`docker run`使用了`-P`，将会暴露一次TCP端口和一次UDP端口，由于会映射到高位端口，它们的端口会不一样。

使用`-p`指定端口，

```shell
docker run -p 80:80/tcp -p 80:80/udp ...
```

也可以使用`docker network`来创建网络在container之间通信而不需要暴露任何端口。因为container可以使用任何端口通信。

## ENV

'''
ENV <key> <value>
ENV <key>=<value> ...
```

`ENV`用来设置环境变量。有2种形式，以下是等价的，

'''
ENV myName="John Doe" myDog=Rex\ The\ Dog \
    myCat=fluffy
```

'''
ENV myName John Doe
ENV myDog Rex The Dog
ENV myCat fluffy
```

可以使用`docker inspect`来查看环境变量。也可以使用`docker run --env <key>=<value>`来修改环境变量。

`ENV`的作用域除了build，还包括container running。有时候会有副作用，比如`ENV DEBIAN_FRONTEND noninteractive`，所有操作都是非交互式的，无需向用户请求输入，直接运行命令。可能会使apt-get用户误认为是一个Debian-based image。正确的做法是为command添加单独的环境变量，如`RUN apt-get install -y python3`。

## ADD

'''
ADD [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
```

`ADD`有2种形式，第2种是为了支持路径包含空格，所以加了双引号。

`--chown`只适用于Linux container，对Windows无效。

`ADD`的作用是从`<src>`复制新文件，目录或者远程文件URLs，然后添加到`<desc>`所在的image文件系统。

`src`如果是文件和目录，那么就是相对路径，相对于build的context。同时支持通配符，遵循Golang的filepath.Match规则。

示例，添加所有以"hom"开头的文件，

'''
ADD hom* /mydir/
```

用`?`匹配单个字符，

'''
ADD hom?.txt /mydir/
```

`<dest>`是绝对路径，或者`WORKDIR`的相对路径。

示例，绝对路径，

'''
ADD test.txt /absoluteDir/
```

相对路径，`<WORKDIR>/relativeDir/`，

'''
ADD test.txt relativeDir/
```

如果路径种包含特殊字符（如`[`和`]`），那么需要进行转义，

示例，添加一个文件`arr[0].txt`，

'''
ADD arr[[]0].txt /mydir/
```

针对Linux，可以使用`--chown`定义username、groupname或者UID/GID，默认新文件和目录会被设置为UID为0，GID为0。

如果只设置username不设置groupname，或只设置UID不设置GID，GID会使用和UID相同的数值。

username和groupname会被container's root filesystem `/etc/passwd` and `/etc/group` 转换为UID/GID。如果container没有这2个文件，在设置了username/groupname后，就会报错。可以通过设置UID/GID来避免。

示例，

'''
ADD --chown=55:mygroup files* /somedir/
ADD --chown=bin files* /somedir/
ADD --chown=1 files* /somedir/
ADD --chown=10:11 files* /somedir/
```

如果build使用STDIN (`docker build - < somefile`)，就没有build context，就只能用`ADD`URL。也可以在使用STDIN时添加压缩包 (`docker build - < archive.tar.gz`)，压缩包根目录的`Dockerfile`和其他压缩包会当做build context。

如果`src`是一个远程文件URL，就会需要600权限(Linux)。如果远程文件有HTTP `Last-Modified` header，header的timestamp会用来设置到dest文件的`mtime`。但是`mtime`不会反映文件是否修改和缓存是否应该更新。

如果URL文件需要授权，`ADD`是不支持的，需要使用`RUN wget`, `RUN curl`，或者container里面的其他工具。

`ADD`遵循以下规则：

-  `<src>` 必须在build的*context* 中；不能 `ADD ../something /something`添加context父目录的东西。因为 `docker build `的第一步是把context，目录及其子目录发送到docker daemon。
- 如果`<src>` 是URL，`<dest>` 没有以斜杠结尾，那么文件从直接从URL下载后，然后直接复制到 `<dest>`。
- 如果 `<src>` 是URL，`<dest>` 是以斜杠结尾的，那么会从URL解析出文件名，下载到`<dest>/<filename>`。比如， `ADD http://example.com/foobar dest/` 会创建文件 `dest/foobar`。URL必须是明确的路径，以保证能找到合适的文件名(`http://example.com` 是无效的)。
- 如果 `<src>` 是目录，那么整个目录都会被复制，包括文件系统的metadata。（目录本身不复制，只是内容）
-  如果 `<src>`是本地压缩包（如gzip, bzip2 or xz），那么会被解压成目录。远程URL是**不会**解压的。解压相当于执行了 `tar -x`，如果dest路径下有文件冲突，会被重命名为“2”。（压缩包不是根据文件名判断的，而是根据内容，比如一个空文件命名为`.tar.gz`，是不会被解压复制的）
- 如果 `<src>` 是任何其他文件，就会随同它的metadata一起复制。此时 `<dest>` 以斜杠 `/`结尾的话，就会被认为是一个目录，`<src>`的内容会被写到`<dest>/base(<src>)`。
- 如果`<src>`定义的是多个资源，不论是直接还是通配符匹配到的， `<dest>` 必须是一个目录，且以斜杠`/`结尾。
- 如果 `<dest>` 不以斜杠结尾，那么就会被认为是一个普通文件，那么`<src>` 会被写到`<dest>`。
- 如果 `<dest>` 不存在，那么path中的所有未创建的目录都会自动创建。

如果`src`内容改变了，在第一次遇到`ADD`指令后，会禁用后续所有指令的缓存，包括`RUN`指令的缓存。

## COPY

`COPY`和`ADD`的**区别**在于`ADD`可以添加远程URLS，`COPY`不能。

'''
COPY [--chown=<user>:<group>] <src>... <dest>
COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]
```

`COPY`有2种形式，第2种是为了支持路径包含空格，所以加了双引号。

`--chown`只适用于Linux container，对Windows无效。

`COPY`的作用是从`<src>`复制新文件，目录，然后添加到`<desc>`所在的image文件系统。

`src`如果是文件和目录，那么就是相对路径，相对于build的context。同时支持通配符，遵循Golang的filepath.Match规则。

示例，添加所有以"hom"开头的文件，

'''
COPY hom* /mydir/
```

用`?`匹配单个字符，

'''
COPY hom?.txt /mydir/
```

`<dest>`是绝对路径，或者`WORKDIR`的相对路径。

示例，绝对路径，

'''
COPY test.txt /absoluteDir/
```

相对路径，`<WORKDIR>/relativeDir/`，

'''
COPY test.txt relativeDir/
```

如果路径种包含特殊字符（如`[`和`]`），那么需要进行转义，

示例，添加一个文件`arr[0].txt`，

'''
COPY arr[[]0].txt /mydir/
```

针对Linux，可以使用`--chown`定义username、groupname或者UID/GID，默认新文件和目录会被设置为UID为0，GID为0。

如果只设置username不设置groupname，或只设置UID不设置GID，GID会使用和UID相同的数值。

username和groupname会被container's root filesystem `/etc/passwd` and `/etc/group` 转换为UID/GID。如果container没有这2个文件，在设置了username/groupname后，就会报错。可以通过设置UID/GID来避免。

示例，

'''
COPY --chown=55:mygroup files* /somedir/
COPY --chown=bin files* /somedir/
COPY --chown=1 files* /somedir/
COPY --chown=10:11 files* /somedir/
```

如果build使用STDIN (`docker build - < somefile`)，就没有build context，就不能用`COPY`。

`COPY`支持`--from=<name|index>`，用来指定src为之前buid的image（通过`FROM .. AS <name>`创建的）来替换build context。既可以是name也可以是index数字（所有使用`FROM`指令建立的build stages）。如果通过name找不到build stage，就会去找同名的image。

`COPY`遵循以下规则：

-  `<src>` 必须在build的*context* 中；不能 `COPY ../something /something`添加context父目录的东西。因为 `docker build `的第一步是把context，目录及其子目录发送到docker daemon。
-  如果 `<src>` 是目录，那么整个目录都会被复制，包括文件系统的metadata。（目录本身不复制，只是内容）
-  如果 `<src>` 是任何其他文件，就会随同它的metadata一起复制。此时 `<dest>` 以斜杠 `/`结尾的话，就会被认为是一个目录，`<src>`的内容会被写到`<dest>/base(<src>)`。
-  如果`<src>`定义的是多个资源，不论是直接还是通配符匹配到的， `<dest>` 必须是一个目录，且以斜杠`/`结尾。
-  如果 `<dest>` 不以斜杠结尾，那么就会被认为是一个普通文件，那么`<src>` 会被写到`<dest>`。
-  如果 `<dest>` 不存在，那么path中的所有未创建的目录都会自动创建。

如果`src`内容改变了，在第一次遇到`COPY`指令后，会禁用后续所有指令的缓存，包括`RUN`指令的缓存。

## ENTRYPOINT

*exec* 格式

'''
ENTRYPOINT ["executable", "param1", "param2"]
```

*shell* 格式

'''
ENTRYPOINT command param1 param2
```

`ENTRYPOINT`用来配置container作为可执行文件来运行。

示例，使用默认内容启动nginx，监听80端口，

'''
$ docker run -i -t --rm -p 80:80 nginx
```

`docker run <image>`的命令行参数，会被添加到*exec*格式中的所有元素之后，并覆盖`CMD`指令定义的元素。这样就可以把参数传递给entry point，也就是`docker run <image> -d`会把`-d`传递给entry point。可以使用`docker run --entrypoint`来覆盖`ENTRYPOINT`指令（但是只能把binary设置为exec，不能用`sh -c`）。

`shell`格式会禁用掉`CMD`或者`run`命令行参数，但是有个缺点就是，`ENTRYPOINT`就不是作为`/bin/sh -c`的子命令来启动的了，也就是不能传递signals。也就意味着可执行文件，不是container的`PID 1`，也不会接收Unix signals（一种软件中断）。这样可执行文件就不会接收来自`docker stop <container>`的`SIGTERM`。

只有`Dockerfile`的最后一个`ENTRYPOINT`才会生效。

### ENTRYPOINT Exec示例

'''
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```

当运行container，`top`是唯一进程，

```shell
$ docker run -it --rm --name test  top -H

top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top
```

为了验证更多结果，使用`docker exec`，

```shell
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H
root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux
```

`top -b -H`，其中`top -b`是`ENTRYPOINT`设置的，`-H`是docker命令行参数，添加到了`ENTRYPOINT`后面，覆盖了`CMD`的`-c。`

然后可以优雅地使用`docker stop test`请求`top` shut down。

示例，使用`ENTRYPOINT`在前台运行Apache（也就是`PID 1`），

'''
FROM debian:stable
RUN apt-get update && apt-get install -y --force-yes apache2
EXPOSE 80 443
VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

如果想编写单个可执行文件的启动脚本，可以使用`exec`和`gosu`命令，来确保可执行文件能够接收到Unix signals。

```shell
#!/usr/bin/env bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

最后，如果在shutdown的时候需要做一些额外的清理（或者和其他containers交互），或者是多个协调而不是单个可执行文件，就可能需要确保`ENTRYPOINT`脚本能够接收Unix signals，传递，然后做更多工作，

```shell
#!/bin/sh
## Note: I've written this using sh so it works in the busybox container too

## USE the trap if you need to also do manual cleanup after the service is stopped,
##     or need to start multiple services in the one container
trap "echo TRAPed signal" HUP INT QUIT TERM

## start service in background here
/usr/sbin/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

## stop service and clean up here
echo "stopping apache"
/usr/sbin/apachectl stop

echo "exited $0"
```

如果使用`docker run -it --rm -p 80:80 --name test apache`来运行这个image，那么就可以使用`docker exec`或`docker top`来验证container处理，然后使用脚本停止Apache，

```shell
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0   4448   692 ?        Ss+  00:42   0:00 /bin/sh /run.sh 123 cmd cmd2
root        19  0.0  0.2  71304  4440 ?        Ss   00:42   0:00 /usr/sbin/apache2 -k start
www-data    20  0.2  0.2 360468  6004 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
www-data    21  0.2  0.2 360468  6000 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
root        81  0.0  0.1  15572  2140 ?        R+   00:44   0:00 ps aux

$ docker top test

PID                 USER                COMMAND
10035               root                {run.sh} /bin/sh /run.sh 123 cmd cmd2
10054               root                /usr/sbin/apache2 -k start
10055               33                  /usr/sbin/apache2 -k start
10056               33                  /usr/sbin/apache2 -k start

$ /usr/bin/time docker stop test

test
real	0m 0.27s
user	0m 0.03s
sys	0m 0.03s
```

shell格式会调用command shell，而exec格式不会，所以exec中`$HOME`是没用的，要用的话直接执行shell `RUN [ "sh", "-c", "echo $HOME" ]`。

注意，exec格式被解析为JSON数组，所以只能用双引号。还需注意反斜杠。

### ENTRYPOINT Shell示例

`ENTRYPOINT`定义一个简单的string，然后它就会在`/bin/sh -c`中执行。shell格式使用shell processing来替代shell environment variables，然后会忽略任何`CMD`或`docker run`命令行参数。为了确保`docker stop`能直接signal任何运行的`ENTRYPOINT`可执行文件，记住使用`exec`开始，

'''
FROM ubuntu
ENTRYPOINT exec top -b
```

运行这个image时，你会看到单个`PID 1`进程，

```shell
$ docker run -it --rm --name test top

Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
Load average: 0.08 0.03 0.05 2/98 6
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     R     3164   0%   0% top -b
```

执行`docker stop`，也会干净的退出，

```shell
$ /usr/bin/time docker stop test

test
real	0m 0.20s
user	0m 0.02s
sys	0m 0.04s
```

如果忘了在`ENTRYPOINT`前添加`exec`，

'''
FROM ubuntu
ENTRYPOINT top -b
CMD --ignored-param1
```

运行（为下一步设置一个name），

```shell
$ docker run -it --name test top --ignored-param2

Mem: 1704184K used, 352484K free, 0K shrd, 0K buff, 140621524238337K cached
CPU:   9% usr   2% sys   0% nic  88% idle   0% io   0% irq   0% sirq
Load average: 0.01 0.02 0.05 2/101 7
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     S     3168   0%   0% /bin/sh -c top -b cmd cmd2
    7     1 root     R     3164   0%   0% top -b
```

你就会看到`ENTRYPOINT`定义的`top`不是`PID 1`。

如果执行`docker stop test`，container就不会干净地退出。`stop`命令会在超时后被强制发送一个`SIGKILL`，

```shell
$ docker exec -it test ps aux

PID   USER     COMMAND
    1 root     /bin/sh -c top -b cmd cmd2
    7 root     top -b
    8 root     ps aux

$ /usr/bin/time docker stop test

test
real	0m 10.19s
user	0m 0.04s
sys	0m 0.03s
```

real 10.19s超时。

### CMD和ENTRYPOINT如何结合使用

`CMD`和`ENTRYPOINT`指令都定义了运行container时，哪些命令会执行。他们的结合有一些规则，

1. Dockerfile应该定义至少一个`CMD` 或`ENTRYPOINT` 。
2. 如果使用container作为可执行文件，应该定义`ENTRYPOINT` 。
3. 如果需要给`ENTRYPOINT` 定义默认参数，或者在container中执行ad-hoc（临时）命令，应该使用`CMD`。
4. 以可选参数运行container时会覆盖`CMD` 。

下面这个表格展示了`CMD`和`ENTRYPOINT`指令的不同组合

|                                | No ENTRYPOINT              | ENTRYPOINT exec_entry p1_entry | ENTRYPOINT [“exec_entry”, “p1_entry”]          |
| :----------------------------- | :------------------------- | :----------------------------- | :--------------------------------------------- |
| **No CMD**                     | *error, not allowed*       | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry                            |
| **CMD [“exec_cmd”, “p1_cmd”]** | exec_cmd p1_cmd            | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry exec_cmd p1_cmd            |
| **CMD [“p1_cmd”, “p2_cmd”]**   | p1_cmd p2_cmd              | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry p1_cmd p2_cmd              |
| **CMD exec_cmd p1_cmd**        | /bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd |

注意，如果`CMD`是从base image定义的，那么设置`ENTRYPOINT`会重置`CMD`为空值。此时如果要使用`CMD`，必须在当前image重新定义。

## VOLUME

'''
VOLUME ["/data"]
```

`VOLUME`指令用来创建挂载点，把container挂载到native host（宿主机）或其他container。

![](012003-【Golang】Dockerfile文件万字全面解析/types-of-mounts-volume_副本.png)

value可以是JSON array，如`VOLUME ["/var/log/"]`，也可以是string，如`VOLUME /var/log`或`VOLUME /var/log /var/db`。

`docker run`命令会用base image中定义的location中存在的任何数据，来初始化新创建的volumn。

示例，

'''
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol
```

`docker run`会在`/myvol`创建一个挂载点，然后把`greeting`复制到新创建的volumn。

遵循规则，

- **基于Windows的containers **: volumn的目标路径必须是以下之一:
  - 不存在的或者空的目录
  - 除 `C:`以外的驱动
- **在Dockerfile里面修改volumn**: 在volumn已经被声明之后的任何build steps尝试修改volumn数据，都会被忽略。
- **JSON formatting**: 要用双引号，不要用单引号.
- **在container run-time才会声明主机目录（挂载点）**: 挂载点是依赖主机的。因为主机目录不能保证对所有主机都是有用的，为了保证image的可移植性，不能在Dockerfile中挂载主机目录，而是必须在创建或运行container的时候。`VOLUME`指令也不支持`host-dir`这样的参数。

## USER

'''
USER <user>[:<group>]
```

或

'''
USER <UID>[:<GID>]
```

`USER`指令用于`RUN`, `CMD` 和`ENTRYPOINT`指令执行时指定user name / group。`USER`指令可以设置user name（或UID），可选用user group（或GID）。

如果定义了user group，那么这个user就只有这个group的membership，任何其他配置的group memberships都会被忽略。

如果user没有primary group，那么image（或者下一条指令）就会以`root` group运行。

在Windows，如果不是内建账号，必须先创建。可以在Dockerfile中调用`net user`命令，

'''
FROM microsoft/windowsservercore
## Create Windows user in the container
RUN net user /add patrick
## Set it for subsequent commands
USER patrick
```

## WORKDIR

'''
WORKDIR /path/to/workdir
```

`WORKDIR`为`RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD`指令设置工作目录。

如果`WORKDIR`不存在，即使后面的Dockerfile不会用到，它仍然会被创建。

`WORKDIR`指令可以在Dockerfile中定义多次。如果是相对路径，那么就是相对于上一条`WORKDIR`指令的路径。

示例，

'''
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

`pwd`的结果是`/a/b/c`。

`WORKDIR`可以引用`ENV`定义的环境变量，示例，

'''
ENV DIRPATH /path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
```

`pwd`的结果是`/path/$DIRNAME`。

## ARG

'''
ARG <name>[=<default value>]
```

`ARG`指令定义变量，用户可以在使用`docker build`命令带参数`--build-arg <varname>=<value>`，在build-time传递这个变量给builder。如果用户指定了一个build参数而没有在Dockerfile中定义，build会报warning，

```shell
[Warning] One or more build-args [foo] were not consumed.
```

一个Dockerfile可以包含一个或多个`ARG`指令。

示例，

'''
FROM busybox
ARG user1
ARG buildno
## ...
```

警告！不建议使用build-time变量来传递私密数据，如github keys，用户认证信息等。因为image的任何用户都可以使用`docker history`查看build-time变量。

### 默认值

`ARG`指令可以设置默认值（可选），

'''
FROM busybox
ARG user1=someuser
ARG buildno=1
## ...
```

如果`ARG`指令有默认值，在build-time没有值传递，那么builder会用这个默认值。

### 范围

`ARG`指令是在它被定义那一行生效的，而不是命令行被使用的时候，或者其他地方。

示例，

'''
FROM busybox
USER ${user:-some_user}
ARG user
USER $user
## ...
```

用户build这个文件，调用，

```shell
$ docker build --build-arg user=what_user .
```

第2行的`USER`结果为`some_user`因为`user`变量是在第3行定义的。

第4行的`USER`结果为`what_user`，因为`user`变量已经被定义了，在命令行传递了`what_user`值。

在`ARG`指令定义之前，任何变量使用结果都是空string。

在`ARG`定义的build stage结束时，`ARG`指令就超出范围了。为了在多个stages使用同一个arg，每个stage都必须包括`ARG`指令，

'''
FROM busybox
ARG SETTINGS
RUN ./run/setup $SETTINGS

FROM busybox
ARG SETTINGS
RUN ./run/other $SETTINGS
```

### 使用ARG变量

可以使用`ARG`或`ENV`指令来为`RUN`指令定义变量。`ENV`定义的环境变量始终都会覆盖`ARG`定义的同名变量。

示例，

'''
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER v1.0.0
RUN echo $CONT_IMG_VER
```

假设使用这条命令build image，

```shell
$ docker build --build-arg CONT_IMG_VER=v2.0.1 .
```

`RUN`会使用`v1.0.0`而不是`ARG`传递的`v2.0.1`。这个行为有点类似于shell脚本，一个局部变量会覆盖通过参数传递的变量，或者从环境定义继承的变量。

还是上面的例子，定义不同的`ENV`会把`ARG`和`ENV`结合的更好用，

'''
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER ${CONT_IMG_VER:-v1.0.0}
RUN echo $CONT_IMG_VER
```

不像`ARG`，`ENV`的值会在build image中持久化。如果不用`--build-arg` build，

```shell
$ docker build .
```

用这个Dockerfile，`CONT_IMG_VER`仍然会持久化在这个image，它的值是`v1.0.0`，因为在第3行用`ENV`定义了默认值。

在这个示例中，通过`ENV`指令，可以把命令行参数传递进来，然后持久化到最终的image，实现了变量扩展。变量扩展只支持Dockerfile指令的一部分指令。

- `ADD`
- `COPY`
- `ENV`
- `EXPOSE`
- `FROM`
- `LABEL`
- `STOPSIGNAL`
- `USER`
- `VOLUME`
- `WORKDIR`
- `ONBUILD` (结合以上指令使用)

### 预定义ARGs

Docker有一些预定义的`ARG`变量，你可以不使用`ARG`指令，直接用这些变量。

- `HTTP_PROXY`
- `http_proxy`
- `HTTPS_PROXY`
- `https_proxy`
- `FTP_PROXY`
- `ftp_proxy`
- `NO_PROXY`
- `no_proxy`

直接在命令行使用，

```shell
--build-arg <varname>=<value>
```

默认这些预定义的变量是不会输出到`docker history`中的。这样可以降低在`HTTP_PROXY`变量中意外泄露敏感认证信息的风险。

示例，使用`--build-arg HTTP_PROXY=http://user:pass@proxy.lon.example.com`来build Dockerfile，

'''
FROM ubuntu
RUN echo "Hello World"
```

`HTTP_PROXY`变量不会输出到`docker history`，也不会被缓存。如果代理服务器变成了`http://user:pass@proxy.sfo.example.com`，后续的build不会导致cache miss。

可以使用`ARG`来覆盖这个默认行为，

'''
FROM ubuntu
ARG HTTP_PROXY
RUN echo "Hello World"
```

当build这个Dockerfile的时候，`HTTP_PROXY`会存到`docker history`中，如果它的值改变了，会把build缓存禁用掉。

### 对缓存的影响

`ARG`变量并不会像`ENV`持久化到image，但是会以类似的方式，影响到build缓存。如果Dockerfile定义了一个`ARG`变量，这个变量和前一个build不一样，那么在第一次用这个变量的时候会发生"cache miss"（不是定义的时候）。尤其是，所有`ARG`后面的`RUN`指令一般都会使用`ARG`变量，这样就会导致cache miss。但是所有预定义ARGs是没有影响cache的，除非是在Dockerfile中有一个同名的`ARG`指令。

示例，2个Dockerfile

'''
FROM ubuntu
ARG CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

'''
FROM ubuntu
ARG CONT_IMG_VER
RUN echo hello
```

如果在命令行指定`--build-arg CONT_IMG_VER=<value>`，以上2个示例在第2行都不会cache miss，第3行会cache miss。`ARG CONT_IMG_VER`会导致RUN那一行被认为是执行了`CONT_IMG_VER=<value>` echo hello，所以如果`<value>`改变了，就cache miss了。

另外一个示例，

'''
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER $CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

第3行会发生cache miss。因为`ENV`引用的`ARG`变量通过命令行改变了。另外，在这个示例中，`ENV`会导致image包含这个value（`ENV`会持久化到image中）。

如果`ENV`和`ARG`指令重复，

'''
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER hello
RUN echo $CONT_IMG_VER
```

第3行就不会发生cache miss，因为`CONT_IMG_VER`的值是常量（`hello`）。因此第4行`RUN`指令用到的环境变量和值在build之间不会改变。

## ONBUILD

```
ONBUILD <INSTRUCTION>
```

`ONBUILD`指令会在image中添加一个*trigger*，这个trigger会在image作为base的时候触发。trigger会在下游的 build context中执行，就像在下游的`Dockerfile` 中，在  `FROM`指令之后，它就已经被立即嵌入了。

任何build指令都可以注册为trigger。

如果你build一个image，这个image会作为base来build其他images，这就很有用。比如，一个应用build环境或者一个deamon自定义配置。

示例，如果一个image是可复用的Python应用builder（用来build新的应用image），那么它需要把应用源码添加到一个特定目录，然后调用build脚本。此时`ADD`和`RUN`指令是无法访问应用源码的，每个应用build的源码也可能不一样。你可以简单地，给应用开发者提供`Dockerfile`样本文件来复制粘贴到他们的应用中，但这是低效、易出错和困难去做更新的，因为这个和“应用定义”代码混淆了。

可以使用`ONBUILD`指令来提前注册指令，在下个build stage再运行。

过程如下，

1. 当碰到`ONBUILD` 指令，builder就会添加trigger到正在build的image的metadata。这条指令不会影响当前build。
2. 在build的最后，所有的triggers都会被存储到image的manifest，在key `OnBuild`下面。可以用 `docker inspect` 命令查看。
3. 然后image可能会被用来作为新build的base，使用 `FROM` 指令。 `FROM` 指令在处理时，下游builder会查找 `ONBUILD` triggers，然后按它们注册的顺序执行。如果有trigger失败了，`FROM`指令就会中断，build失败。如果triggers都成功了，那么`FROM`会完成，build成功。
4. Triggers会在执行后，从最后一个image中清除。也就是说，它们是不会随着“父子”build继承的。

比如你可能会添加这样的内容，

'''
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
```

注意，1.链式`ONBUILD ONBUILD`是不允许的。2.`ONBUILD`可能不会trigger `FROM` 或 `MAINTAINER`指令。

## STOPSIGNAL

'''
STOPSIGNAL signal
```

`STOPSIGNAL`指令设置system call signal，发送到container退出。signal可以是有效的unsigned number（匹配kernel’s syscall table里的position，比如9），也可以是SIGNAME（比如SIGKILL）。

## HEALTHCHECK

2种格式，

- `HEALTHCHECK [OPTIONS] CMD command` (通过运行container里面的命令来检查container)
- `HEALTHCHECK NONE` (禁用健康检查，从base image继承)

`HEALTHCHECK `指令用来告诉Docker怎样测试container是否还在工作。比如虽然server一直在运行，但是实际上已经死循环了，无法处理新连接了。

当container定义了健康检查，就会把健康状态添加到status中。status初始化是`starting`。无论健康检查什么时候通过，它都会变为`healthy`（无论之前是什么状态）。在一定数量的连续失败后，它会变为`unhealthy`。

第一种格式的`OPTION`可以是，

- `--interval=DURATION` (default: `30s`)
- `--timeout=DURATION` (default: `30s`)
- `--start-period=DURATION` (default: `0s`)
- `--retries=N` (default: `3`)

在container开始后的**interval** seconds ，会运行健康检查。每个健康检查完成后，等待**interval** seconds再次运行。

如果健康检查运行的时候超过了**timeout** seconds，就认为失败。

失败的次数如果达到了**retries**的值，就认为`unhealthy`。

**start period**指定了container需要启动的时间。在这期间探针失败（Probe failure）不会记作重试次数。但是，如果在这期间健康检查通过了，那么container就认为已经启动了，这之后的失败（all consecutive failures）就会记作重试次数。

一个Dockerfile只能有一个`HEALTHCHECK `指令。如果有多个，那么只有最后一个`HEALTHCHECK `生效。

第1种格式的`command`既可以是*shell*命令（如，`HEALTHCHECK CMD /bin/check-running`），也可以是`exec`数组。

command的退出状态反应了container的健康状态，

- 0: success - the container is healthy and ready for use
- 1: unhealthy - the container is not working correctly
- 2: reserved - do not use this exit code

示例，每5分钟检查1次，以确保web服务器能在3秒内为网站首页提供服务，

'''
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

为了帮助debug失败探针（failing probes），任何写到stdout或stderr输出文本（UTF-8编码）都会被存储到健康状态，并且可以使用`docker inspect`查询。而且输出应该简短（目前只有最开始的4096 bytes会被存储）。

当container的健康状态改变了，会用新的状态生成一个`health_status`事件。

## SHELL

'''
SHELL ["executable", "parameters"]
```

`SHELL`指令允许重写*shell*格式命令的默认shell。Linux的默认shell是`["/bin/sh", "-c"]`，Windows的默认shell是`["cmd", "/S", "/C"]`。`SHELL`指令必须在Dockfile中写成JSON格式。

`SHELL`指令在Windows特别有用，因为Windows有2个常用的不同的原生shell，`cmd`和`powershell`，也有可选用的shell，包括`sh`。

`SHELL`指令可以出现多次。每个`SHELL`指令会覆盖所有之前的`SHELL`指令，影响随后的指令。

示例，

'''
FROM microsoft/windowsservercore

## Executed as cmd /S /C echo default
RUN echo default

## Executed as cmd /S /C powershell -command Write-Host default
RUN powershell -command Write-Host default

## Executed as powershell -command Write-Host hello
SHELL ["powershell", "-command"]
RUN Write-Host hello

## Executed as cmd /S /C echo hello
SHELL ["cmd", "/S", "/C"]
RUN echo hello
```

当*shell*格式的`RUN`，`	CMD`，`ENTRYPOINT`出现在Dcokerfile中时，`SHELL`指令能影响这些指令。

示例，Windows上常见的模式，可以通过使用SHELL指令进行简化，

'''
RUN powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

docker调用的命令，

```shell
cmd /S /C powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

这个有点低效，有2个原因。首先，有一个不必要的cmd.exe命令行处理器（aka shell）被调用了。其次，*shell*格式的`RUN`指令需要额外的前缀命令`powershell -command`。

为了更高效，有2种机制。其一是使用JSON格式，

'''
RUN ["powershell", "-command", "Execute-MyCmdlet", "-param1 \"c:\\foo.txt\""]
```

JSON格式是清晰的，不会使用不必要的cmd.exe。但是需要双引号和转义符，显得有点冗余。

。其二是用`SHELL`指令和`shell`格式，这样可以给Windows用户更自然的语法，特别是和`escape` parser directive结合使用的时候，

'''
## escape=`

FROM microsoft/nanoserver
SHELL ["powershell","-command"]
RUN New-Item -ItemType Directory C:\Example
ADD Execute-MyCmdlet.ps1 c:\example\
RUN c:\example\Execute-MyCmdlet -sample 'hello world'
```

结果是，

```shell
PS E:\docker\build\shell> docker build -t shell .
Sending build context to Docker daemon 4.096 kB
Step 1/5 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/5 : SHELL powershell -command
 ---> Running in 6fcdb6855ae2
 ---> 6331462d4300
Removing intermediate container 6fcdb6855ae2
Step 3/5 : RUN New-Item -ItemType Directory C:\Example
 ---> Running in d0eef8386e97


    Directory: C:\


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/28/2016  11:26 AM                Example


 ---> 3f2fbf1395d9
Removing intermediate container d0eef8386e97
Step 4/5 : ADD Execute-MyCmdlet.ps1 c:\example\
 ---> a955b2621c31
Removing intermediate container b825593d39fc
Step 5/5 : RUN c:\example\Execute-MyCmdlet 'hello world'
 ---> Running in be6d8e63fe75
hello world
 ---> 8e559e9bf424
Removing intermediate container be6d8e63fe75
Successfully built 8e559e9bf424
PS E:\docker\build\shell>
```

`SHELL`指令也能被用来修改shell操作方式。比如在Windows用`SHELL cmd /S /C /V:ON|OFF`，可以修改[延迟环境变量扩展]([https://baike.baidu.com/item/%E5%BB%B6%E8%BF%9F%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E6%89%A9%E5%B1%95/2259702](https://baike.baidu.com/item/延迟环境变量扩展/2259702))语义。

`SHELL`指令也可以用在Linux上，可选的shell有`zsh`, `csh`, `tcsh`等。

## Dockerfile示例

'''
## Nginx
#
## VERSION               0.0.1

FROM      ubuntu
LABEL Description="This image is used to start the foobar executable" Vendor="ACME Products" Version="1.0"
RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server
```

'''
## Firefox over VNC
#
## VERSION               0.3

FROM ubuntu

## Install vnc, xvfb in order to create a 'fake' display and firefox
RUN apt-get update && apt-get install -y x11vnc xvfb firefox
RUN mkdir ~/.vnc
## Setup a password
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
## Autostart firefox (might not be the best way, but it does the trick)
RUN bash -c 'echo "firefox" >> /.bashrc'

EXPOSE 5900
CMD    ["x11vnc", "-forever", "-usepw", "-create"]
```

'''
## Multiple images example
#
## VERSION               0.1

FROM ubuntu
RUN echo foo > bar
## Will output something like ===> 907ad6c2736f

FROM ubuntu
RUN echo moo > oink
## Will output something like ===> 695d7793cbe4

## You'll now have two images, 907ad6c2736f with /bar, and 695d7793cbe4 with
## /oink.
```

以下内容可查看参考资料进一步阅读。

- BuildKit（第三方工具）
- Parser directives的命令syntax（依赖BuildKit）
- RUN已知bug（[Issue 783](https://github.com/docker/docker/issues/783)）
- External implementation features（依赖BuildKit）
- Automatic platform ARGs in the global scope（依赖BuildKit）

> 参考资料
>
> https://docs.docker.com/engine/reference/builder/
>