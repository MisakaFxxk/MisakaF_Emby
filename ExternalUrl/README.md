# Emby客户端内插入第三方播放器跳转链接

### 一、环境配置

Nginx反向代理本地Emby服务端，Python3&Pip3。

```
安装Python第三方包：
pip3 install flask
pip3 install requests
pip3 install urllib3
```

### 二、Nginx配置

打开Nginx反向代理配置文件，在location / 下面的大括号**内**添加：

```
if ( $request_uri ~* /Users/(.*)/Items/\d\d\d+.\?X-Emby-Client )
{
	proxy_pass http://127.0.0.1:12345;
}
if ( $request_uri ~* redirect2player )
{
	return 301 $arg_infuseurl;
}
```

### 三、Python配置

将`ExternalUrl.py`下载到本地并打开，按照自己的情况修改第七、八行的变量。

**注意！`localhost`无需在URL后添加/，而`embyurl`需要在URL后添加/**

### 四、启动本地劫持服务器

```
screen -S player 
python3 ExternalUrl.py
或后台运行：
nohup python3 ExternalUrl.py  > ExternalUrl.log 2>&1 &
```

访问Emby，进入具体的影视页面，底部**链接**一栏应会出现跳转链接。

此方案应适配所有官方/魔改客户端，不适配Fileball，影音宝等第三方客户端。

![](http://tva1.sinaimg.cn/large/007dA9Degy1h885ff0i6hj31z40z1npd.jpg)

### 五、致谢

感谢@baipiaoking提供的第三方播放器URL生成思路，Emby资源技术共享交流群在Debug期间提供的大力帮助。