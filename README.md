# 💻 http-proxy
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-Apache_2.0-red.svg)](https://raw.githubusercontent.com/duibu/http-proxy/main/LICENSE) 

```bash
  _ __  _ __ _____  ___   _ 
 | '_ \| '__/ _ \ \/ / | | | 
 | |_) | | | (_) >  <| |_| | 
 | .__/|_|  \___/_/\_\\__, | 
 |_|                  |___/ 
```

一款用于开发人员在接口调试过程中使用的http代理工具，可以用来修改http请求的请求头

## 🏆 环境说明

python:3.x

## 🔧 安装

使用git下载代码

```bash
git clone https://github.com/duibu/http-proxy.git
```

## 🚀 参数说明

```
--host: IP地址，默认是127.0.0.1
--port: 代理服务端口，默认是8372
--listen: 监听客户端数量，默认是10
--buf: 缓冲区大小，默认8kb
--delay: 延迟时间，默认1ms
```

## 📖 Extends编写规则     
http-proxy支持自定义编写extends         
http-proxy统一要求python3编写，具有inject_headers函数进行自定义请求头注入                     

#### 👻 注入请求头函数(inject_headers)编写应该满足以下条件:                   
1. 函数名为 inject_headers， 参数接收请求头（header）和请求数据（data）两个参数           
2. 函数的返回结果以字典的形式返回自定义的请求头，字典的key是请求头的名称，字典的value是请求头的内容
3. 如果扩展脚本返回的请求头在原请求头存在，则回替换原请求头的内容                             

    ```python
    def inject_headers(header = {}, data = None):
        costum = config()
        for key in list(costum.keys()):
            if key.encode() in header:
                del costum[key]
                continue
        return costum
        
    def config():
        if not file_is_exits(DEFAULT_CONFIG_PATH + '/header.json'):
            logger.error('config/header.json配置文件不存在')
            return {}
        with open(DEFAULT_CONFIG_PATH + '/header.json') as f:
            data = json.load(f)
        return data
    ```

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [Apache License](LICENSE) license.