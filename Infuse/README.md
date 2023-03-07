# Infuse扫库优化模块

### 一、原理实现

Infuse扫库时只需要接收固定的json数据，所以我们可以将这些数据保存到数据库内，如果有扫库请求，通过URL内的一些参数定位json，返回即可。

Nginx劫持Infuse扫库请求到本地搭建的扫库服务上，首先判断此条json数据库内是否存在，若存在则直接返回，若不存在则通过GET向Emby请求获取，先向Infuse客户端返回json，再保存到数据库内，以供下次直接使用。

### 二、环境配置

Nginx反向代理本地Emby服务端，Python3&Pip3。

```
安装Python第三方包：
pip3 install flask
pip3 install requests
pip3 install pymysql
pip3 install DBUtils==1.2
```

### 三、Nginx配置

打开Nginx反向代理配置文件，在location / 下面的大括号**内**添加：

I know, I know，这个实现方法相当蠢。如果有高人还望不吝赐教，但目前它至少能跑，反正代码和我有一个能跑就行。

```
if ($http_user_agent ~* "Infuse") {
	set $check yes;
}
if ( $request_uri ~* /Users/(.*)/Items\?ExcludeLocationTypes=Virtual )
{
  	set $check2 "${check}yes";
}
if ( $request_uri ~* Episode )
{
  	set $check3 "${check2}yes";
}
if ( $request_uri ~* Movie )
{
  	set $check3 "${check2}yes";
}
set $check4 yes;
if ( $request_uri ~* StartIndex=0 )
{
  	set $check4 no;
}
set $check3 "${check3}${check4}";
if ($check3 = "yesyesyesyes")
{
	proxy_pass http://127.0.0.1:60000;
}
```

### 三、数据库配置

在Emby本机上安装Mysql 8.0数据库。

首先创建一个名为`infuse`的数据库，然后创建一个名为`metadata`的表，表内结构如下，也可直接使用文件夹内的metadata.sql来导入表结构。

![image-20230307091348630](C:\Users\ChengYifei\AppData\Roaming\Typora\typora-user-images\image-20230307091348630.png)

### 四、Python配置

将`infuse.py`下载到本地并打开，修改第11行的Emby地址为未经过Nginx反向代理的Emby地址，修改14行开始的数据库配置内的user和password。

### 五、启动优化模块

```
screen -S infuse 
python3 infuse.py
或后台运行：
nohup python3 infuse.py  > infuse.log 2>&1 &
```