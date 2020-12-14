# nmap_restful
## 功能
nmap调用的 restful api 接口
## 运行
### Docker
进入到`nmap_restful`目录

先构建镜像，`docker build -t nmaprest:v1 .`

然后，运行`docker run  --net=host  nmaprest:v1`  (docker容器使用宿主机的网络)

结束运行
`docker ps`找到对应的ID
`docker stop $ID`


运行起来之后，API地址是 `localhost:5000/v1.0`
文档地址 http://127.0.0.1:5000/apidocs/#/
具体的扫描参数分类参考 `zenmap`


### 本地运行
Pull到本地，安装依赖 `pip install -r requirements.txt`

为了演示方便暂时使用的sqlite,
在`main.py`中更改数据库的设置，我代码`app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nmapuser:123456@localhost:3306/nmap'`
对应的是用户nmapuser，密码123456，端口3306，数据库名nmap

如果是以root用户运行的这个程序，不需要修改。如果是普通用户请将`app/libs/nmapScan_threading.py`文件中的12行打开将15行注释

终端运行(普通用户)，`sudo python run.py`
(使用UDP扫描时需要root)


运行起来之后，API地址是 `localhost:5000/v1.0`
文档地址 http://127.0.0.1:5000/apidocs/#/
具体的扫描参数分类参考 `zenmap`


## 示例
### 请求
```
curl --location --request POST 'localhost:5000/nmap/api/v1.0' \
--header 'Content-Type: application/json' \
--data-raw '{"host":"127.0.0.1","port":"445,446-1024","tcp":"-sS","scan":"-O"}'
```
## 另一个版本(已删)
`api_restful_errors.py`是另一个版本，这个版本全部使用的是 Flask Restful Api 的错误处理，也就是没有自己的`try/catch`。
这个版本当nmap扫描出错时，触发 PortScannerError，不会向上面的版本返回具体的错误提示信息，而是返回代码中 `errors`变量 中预定义的固定的错误信息。
