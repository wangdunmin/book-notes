# Centos安装Redis
## 版本说明
* Redis 3.2.0

## 安装说明
1.  下载Redis安装包到服务器上

到要安装的文件夹下
```
wget http://download.redis.io/releases/redis-3.2.0.tar.gz
```
2. 解压安装包
```
tar xzf redis-3.2.0.tar.gz 
```
3. 编译安装包
```
cd redis-3.2.0/
make
```
4. 安装编译后的安装包
```
cd src/
make install
```
## 运行说明
1. 为了方便操作，可以选择将安装目录redis.conf 和src/下的二进制文件(编译安装后的可运行二进制文件)复制到统一文件夹下

2. 修改配置文件

    2.1 关于后台运行
    ```
    daemonize yes
    ```
    2.2 关于Key事件监听
    ```
    notify-keyspace-events EA
    ```

2. 运行Redis

```
redis-server redis.conf
```

> 1. 没有配置环境变量时需要指定redis-server的全路径或者到redis-server所在路径下
> 2. redis.conf可以是相对路径和全路径