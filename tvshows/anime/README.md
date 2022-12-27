# Emby自动追剧系统 —— 动漫篇

本文所有教程基于root用户，默认git clone后文件夹地址为：/root/MisakaF_Emby

自动重命名支持所有字幕组。自动重命名部分，调用了[Rename](https://github.com/Nriver/Episode-ReName)项目，如有不适，还请邮件通知到：admin@misakaf.org。

### 环境准备

qBittorrent、rclone、Python3 & Pip3、已经搭建好的Emby

#### qBittorrent

```
wget "https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.2_v2.0.6/x86_64-qbittorrent-nox"
chmod +x ./x86_64-qbittorrent-nox
./x86_64-qbittorrent-nox -d
```

此时，qBittorrent已经成功在后台运行。浏览器输入http://IP:8080，默认用户名：admin，默认密码：adminadmin。登入后，点击左上方设置图标的按钮，选择Web UI标签页，第一个选项可以更改页面语言，下方可以修改登录密码，改完了别忘了点击最下方的保存(Save)

#### rclone

```
需要在VPS和自己电脑上都安装rclone，用于认证。

在VPS上安装rclone：
curl https://rclone.org/install.sh | sudo bash
在自己电脑上安装rclone：
https://downloads.rclone.org/v1.58.1/rclone-v1.58.1-windows-amd64.zip
下载后解压
```

VPS操作：

```
rclone config
```

选择 【n】(新建)，然后回车输入名称，例如：GoogleDrive

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ijm2n7hnj30ct06vwf9.jpg)

这里选择你需要配置的存储类型，我这里选择 【17】（Google Drive），根据版本变化选择的序号会不同看清楚Google Drive再选择，如果要挂载其他的选填数字即可：

![](https://tva4.sinaimg.cn/large/007dA9Dely8h2ijp1yzifj308r01ldfq.jpg)

接下来连续回车两次后，这里选 【1】即可：

![](https://tva3.sinaimg.cn/large/007dA9Dely8h2ijqihk5ij30k90cewhm.jpg)

再次两个回车，选择【n】：

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2ijwr5ftyj309g037glo.jpg)

选择【n】：

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2ijwr5ftyj309g037glo.jpg)

来到这界面，复制红框内语句，转到你自己的电脑上开始操作：

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ik1or4eqj30ld07uq4w.jpg)



——————————————————————————————————————————————————



鼠标点击图中位置，输入【cmd】回车。

![](https://tva4.sinaimg.cn/large/007dA9Dely8h2ijfpdie4j313t0ml77t.jpg)

得到如下界面。

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ik0zbjz8j30xz0hrq3z.jpg)

粘贴刚刚复制的语句，回车：

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ik2xj7zfj30xz0hrab9.jpg)

会自动拉起浏览器，登录你的谷歌账号后回到黑框框。

复制红框内的字符串，如果无法选中，先鼠标右键-标记，然后就可以了：

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ik653oifj30xz0hr0xj.jpg)

回到VPS，粘贴你刚刚在自己电脑里复制的字符串，回车。

——————————————————————————————————————————————————

这一步看你需不需要挂载共享硬盘，需要就选【y】，不需要就选【n】

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2ik82q182j30fm03774h.jpg)

![](https://tva1.sinaimg.cn/large/007dA9Dely8h2ik903oqqj30j308oq3o.jpg)

接下来一路回车，最后按【q】退出rclone配置即可。

##### rclone挂载谷歌云盘

```
安装fuse
ubuntu:
apt-get install fuse -y 
centos:
yum install fuse -y


mkdir /mnt/googledrive
rclone mount googledrive: /mnt/googledrive --allow-other --allow-non-empty --cache-dir=/home/cache --vfs-cache-mode full &
```

#### Python3 & Pip3

自己上网查找安装，教程太多不再赘述

```
git clone https://github.com/MisakaFxxk/MisakaF_Emby.git && cd MisakaF_Emby/tvshows/anime && pip3 install -r requirements.txt
```



### 自动更新

进入qBittorrent，点击【设置】，做如下修改：

![](https://tva4.sinaimg.cn/large/007dA9Dely8h2iks6781xj31ov0u00vm.jpg)

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2iksmik7jj31ot0u0djt.jpg)

![](https://link.jscdn.cn/sharepoint/aHR0cHM6Ly8xZHJpdi1teS5zaGFyZXBvaW50LmNvbS86aTovZy9wZXJzb25hbC9zdG9yXzFkcml2X29ubWljcm9zb2Z0X2NvbS9FVUZYVFBneENuOUVqTE1VUGhTb3lQWUJQZHZfY0VQLTZLY1NGTjZ5RXNHZ053.png)

```
python3 -X utf8 /root/MisakaF_Emby/tvshows/anime/update.py "%F"
```

然后点击右上角【RSS】，进入RSS配置页面：

![](https://tva4.sinaimg.cn/large/007dA9Dely8h2iktqgb0oj31ot0u0aby.jpg)

首先，点击【新RSS订阅】，输入动漫订阅地址：https://bangumi.moe/rss/latest，或用其他你自己找的也行

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2ikvdlgwyj31or0u0tau.jpg)

再点击【RSS下载器】，这里示范添加一个新番【间谍过家家】

![](https://tva3.sinaimg.cn/large/007dA9Dely8h2iky1jzhvj31ox0u00xh.jpg)

里面这样设置，红框标出三个需要修改的地方：

![](https://tva4.sinaimg.cn/large/007dA9Dely8h2ikz3ua0lj30va0p7aes.jpg)

具体这个【必须包含】里面该填什么，需要你去RSS订阅源里自己找，然后提取一个独一无二，只属于这个资源的标识。比如图中的【间谍过家家 NC B-Global】，NC代表NC-RAWS的资源，这样就不会抓取到别的字幕组；B-Global是NC-RAWS为了区分Baha源和港澳台源所加的标识，我们这里需要港澳台源，所以加B-Global；间谍过家家为番剧名，这个具体是什么要去看字幕组发布的资源叫什么，同一个番，有些字幕组会按繁体来，叫做间谍家家酒。有时你还可以加上清晰度，比如1080。

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2il447d3tj31ov0u07gy.jpg)

【保存到指定目录】必须要像我这样写，格式为/***/间谍过家家/Season 1，因为重命名脚本会读取路径，最后两个如果不是番剧名和季数就会报错。

最后点击保存，番剧便会开始下载，有更新时也会自动下载。



如果你这个qBittorrent只用于更新番剧，并且服务器硬盘空间也不够大，可以改下这个设置，适当做种后删除文件。

![](https://tva2.sinaimg.cn/large/007dA9Dely8h2ilfidpmnj30r00pldii.jpg)
