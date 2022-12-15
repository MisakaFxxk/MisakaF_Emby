## 1、说在前面

本代码的部分功能依赖Emby的Webhook实现，而Webhook是需要激活服务端的，如何激活请自行寻找。

本代码的部分功能需要使用post传送数据，请尽量保证两台服务器的连接稳定。若无法保证，可以将3.3中的api搭建放在Emby服务端本地。

这个功能实现起来比较复杂，涉及到了好几个脚本，绝大部分人应该会搭建失败，请不要因此而发issue或私聊我。只要我公益服的通知还在正常运行，代码本身就是没问题的。



## 2、功能实现

#### 2.1、收藏通知

`Webhook`插件post发送用户收藏剧集的信息，服务器B搭建api接收信息并提醒。

#### 2.2、更新通知

`Scripter-X → Actions`插件在有新媒体入库时运行bash脚本，调用本地python脚本，发送更新通知。



## 3、环境搭建

### 3.1、数据库

本次代码最好配合我写的注册机器人使用。若你使用的是其他公益服机器人，数据库结构不同，不用担心，只需修改一个子函数即可完美适配你的数据库。

在同一个数据库下创建名为`favorite`的表，表内结构如下，按图创建即可：

![](http://tva1.sinaimg.cn/large/007dA9Degy1h771lcytk8j30uv03zgnd.jpg)

#### 3.1.1、适配他人机器人数据库

如果你使用的是我写的机器人，那就不需要看这条，只要保证user表和favorite表在同一个数据库下即可。

如果你使用的是其他机器人，请确保你的用户表中记录了TG用户ID和Emby用户ID这两个字段，他们大概长这样

![](http://tva1.sinaimg.cn/large/007dA9Degy1h771phzvp9j30da02ddgo.jpg)

打开`/收藏通知/api_notify.py`，找到20行`idtochatid`这个子函数，修改22行`create_sqli = "SELECT 空1 FROM 空2 WHERE 空3 = "+'"'+ str(id)+'"'`，将空1替换为TG用户ID的字段名(chatid)，空2替换为用户表名(user)，空3替换为Emby用户ID的字段名(emby_userid)。



### 3.2、Emby

#### 3.2.1、Docker安装的Emby

注意，由于用官方镜像内缺失相关环境，请使用

[linuxserver/emby]: https://hub.docker.com/r/linuxserver/emby

提供的镜像，也算半个官方性质，与官方同步更新，启动命令无需修改。

将**服务端**文件夹内的两个文件上传到服务器内，修改update.py内的数据库连接信息与BOT API。本文假设在/mnt/notify文件夹下，需要将此文件夹映射到容器内。在docker run命令中加入`--volume /mnt/notify:/mnt/notify`，启动容器。

容器启动后，输入`docker exec -it 容器ID bash`进入容器。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h771ewl3q5j30ee01o0tl.jpg)

显示这样即进入容器成功，接下来开始搭建环境：

```
apt update
apt install python3
apt install python3-pip

pip3 install requests
pip3 install python-telegram-bot==13.11
pip3 install pymysql
```

没有任何报错即搭建完毕，进入Emby后台，在插件市场中安装`Scripter-X → Actions`插件，重启服务器，在后台左下角找到此插件的设置界面。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h7724vgxhij31z40z3wny.jpg)

在右侧找到**onMedialtemAdded**和**onMedialtemAddedComplete**选项，展开，点击加号添加一条命令，再点右侧笔图标，编辑此条命令。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h77279cxvhj31nj0hek82.jpg)

按上图进行设置，最后一行的触发条件是把上面这些属性拖下来，最后的**Episode**是拖个Text下来，双击编辑。

```
#供复制
/mnt/notify/notify.sh
%series.id% %series.name% %season.number% %episode.number%
```



#### 3.2.2 命令行安装的Emby

将**服务端**文件夹内的两个文件上传到服务器内，本文假设在/mnt/notify文件夹下。修改update.py内的数据库连接信息与BOT API

安装python环境

```
apt update
apt install python3
apt install python3-pip

pip3 install requests
pip3 install python-telegram-bot==13.11
pip3 install pymysql
```

没有任何报错即搭建完毕，进入Emby后台，在插件市场中安装`Scripter-X → Actions`插件，重启服务器，在后台左下角找到此插件的设置界面。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h7724vgxhij31z40z3wny.jpg)

在右侧找到**onMedialtemAdded**和**onMedialtemAddedComplete**选项，展开，点击加号添加一条命令，再点右侧笔图标，编辑此条命令。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h77279cxvhj31nj0hek82.jpg)

按上图进行设置，最后一行的触发条件是把上面这些属性拖下来，最后的**Episode**是拖个Text下来，双击编辑。

```
#供复制
/mnt/notify/notify.sh
%series.id% %series.name% %season.number% %episode.number%
```



### 3.3、 API搭建

找一个服务器B，开放12345端口，安装python等环境：

```
apt update
apt install python3
apt install python3-pip

pip3 install requests
pip3 install python-telegram-bot==13.11
pip3 install pymysql
pip3 install flask
```

将**收藏通知**文件夹内的文件上传到服务器内，本文假设路径为/root/api_notify.py，修改api_notify.py内的数据库连接信息与BOT API。

输入命令`python3 /root/api_notify.py`尝试启动，一切顺利应该没有什么报错。

进入Emby后台，安装Webhook插件(一般自带，服务端需要激活)。进入Webhook插件设置界面，点击**添加 Webhook**：

URL一栏输入：`http://IP:12345/update`，勾选**User**，储存即可，测试会报错，正常。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h772qezp4ej316u0s7n0c.jpg)

现在你可以去收藏一个电视剧，看看机器人是否会提示你收藏成功。若一切顺利，Ctrl+C结束前台运行，输入命令`nohup python3 /root/api_notify.py  > /root/api_notify.log 2>&1 &`后台运行。

