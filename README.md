turedns
=======

dns server

第一 需要学习一下python

第二 能用google查询点东西


初步构想，需要下面几个模块

读取配置
读取配置文件

打印日志
根据配置文件，打印日志

服务器端
监听服务端，并发送请求

客户端
对发送的请求，去访问配置中的服务器

缓存
如果已经有cache，就返回cache中的内容

DNS 信息
获取DNS数据进行解包和组包


truedns.py 
按最简单的方式，通过转发dns查询来做dns服务器

truedns1.py
实现了基本的dns服务器，能cache已经查询的域名。但是服务端还是会卡住。

truedns2.py
使用socketserver 来重写服务端，并且使用dnslib包


