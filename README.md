# http-proxy
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-Apache_2.0-red.svg)](https://raw.githubusercontent.com/duibu/http-proxy/main/LICENSE) 

```bash
  _ __  _ __ _____  ___   _ 
 | '_ \| '__/ _ \ \/ / | | | 
 | |_) | | | (_) >  <| |_| | 
 | .__/|_|  \___/_/\_\\__, | 
 |_|                  |___/ 
```

一款用于开发人员在接口调试过程中使用的http代理工具，可以用来修改http请求的请求头

## 环境说明

python:3.x

## 安装

使用git下载代码

```bash
git clone https://github.com/duibu/http-proxy.git
```

## 参数说明

```
--host: IP地址，默认是127.0.0.1
--port: 代理服务端口，默认是8372
--listen: 监听客户端数量，默认是10
--buf: 缓冲区大小，默认8kb
--delay: 延迟时间，默认1ms
```