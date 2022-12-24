# 账号注册机器人 v2.0

​		一个简陋但实用的机器人脚本，并不会对代码逻辑进行解释，看得懂的看，看不懂的直接用。新版本转向使用数据库，并加入注册前入群检测。

## 功能简介

提供以下功能： /start	   	开始对话

​							/help	   	指令帮助

​							/create		注册账号

​							/bind		   绑定账号（正常情况下无需使用本功能，注册后可自动绑定）

​							/reset		  重置密码

​							/info	    	查询信息



## 启动前准备工作

1、将项目克隆到本地

```
git clone https://github.com/MisakaFxxk/MisakaF_Emby.git && cd MisakaF_Emby/create && pip3 install -r requirements.txt
```

1、找[BOTfather](https://t.me/BotFather)申请一个API。进入Emby后台，找到高级-API密钥，生成一个API。

2、创建一个MySQL 8.0+数据库，设计一个名为`user`的表，添加两个字段：chatid(类型：varchar，长度255，设为主键，非空)、emby_userid(类型：varchar，长度255)。

3、打开`bot.py`，填写12-22行中的内容。



## 启动机器人

前台启动机器人

```
python3 bot.py
```

后台启动机器人

```
nohup python3 bot.py > botlog.log 2>&1 &
```



## 旧版本数据导入数据库

从服务器中下载`accounts.txt`到本地，例如路径为`C:/Users/Admin/Desktop/fsdownload/accounts.txt`

连接上数据库，新建查询，输入以下代码后回车。**自行修改代码内accounts.txt文件的路径**

```
load data local infile "C:/Users/Admin/Desktop/fsdownload/accounts.txt" into table user fields terminated by" " lines terminated by "\n" (chatid,emby_userid);
```

未报错则成功导入，可以使用新版本机器人连接数据库。









​		

