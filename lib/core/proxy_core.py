import socket
import select
import time
import _thread as thread
from lib.parse.http_package import HttpRequestPacket


def debug(tag, msg):
    print('[%s] %s' % (tag, msg))

#简单的HTTP代理
class HttpProxy(object):

    #   初始化代理套接字，用于与客户端、服务端通信

    #    参数：host 监听地址，默认0.0.0.0，代表本机任意ipv4地址
    #    参数：port 监听端口，默认8080
    #    参数：listen 监听客户端数量，默认10
    #    参数：bufsize 数据传输缓冲区大小，单位kb，默认8kb
    #    参数：delay 数据转发延迟，单位ms，默认1ms
    def __init__(self, host='127.0.0.1', port=8080, listen=10, bufsize=8, delay=1):
        
        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
        self.socket_proxy.bind((host, port))
        self.socket_proxy.listen(listen)

        self.socket_recv_bufsize = bufsize*1024
        self.delay = delay/1000.0

        debug('info', 'bind=%s:%s' % (host, port))
        debug('info', 'listen=%s' % listen)
        debug('info', 'bufsize=%skb, delay=%sms' % (bufsize, delay))

    def __del__(self):
        self.socket_proxy.close()
    
    def connect(self, host, port):

        (family, sockettype, _, _, target_addr) = socket.getaddrinfo(host, port)[0]
        
        tmp_socket = socket.socket(family, sockettype)
        tmp_socket.setblocking(0)
        tmp_socket.settimeout(5)
        tmp_socket.connect(target_addr)
        return tmp_socket
         
    def proxy(self, socket_client):
        '''
        代理核心程序

        参数：socket_client 代理端与客户端之间建立的套接字
        '''
        # 接收客户端请求数据
        req_data = socket_client.recv(self.socket_recv_bufsize)
        print(req_data)
        if req_data == b'':
            return

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)
        print(http_packet.req_line)
        CUSTOM_HEADERS = {'X-Custom-Header': 'proxy'}
        req_data = req_data.decode().replace('\r\n\r\n', '\r\n'+'\r\n'.join('%s: %s' % (k,v) for k,v in CUSTOM_HEADERS.items())+'\r\n\r\n')
        print('host', http_packet.host)
        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            # 建立连接
            socket_server = self.connect(server_host, server_port) 
            # 将客户端请求数据发给服务端
            socket_server.send(req_data.encode())

        # 使用select异步处理，不阻塞
        self.nonblocking(socket_client, socket_server)

    #异步数据处理
    #socket_client 代理端与客户端之间建立的套接字
    #socket_server 代理端与服务端之间建立的套接字
    def nonblocking(self, socket_client, socket_server):
        _rlist = [socket_client, socket_server]
        is_recv = True
        while is_recv:
            try:
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    # 接收数据
                    data = tmp_socket.recv(self.socket_recv_bufsize)
                    if data == b'':
                        is_recv = False
                        continue
                    
                    # socket_client状态为readable, 当前接收的数据来自客户端
                    if tmp_socket is socket_client: 
                        # 将客户端请求数据发往服务端
                        socket_server.send(data)

                    # socket_server状态为readable, 当前接收的数据来自服务端
                    elif tmp_socket is socket_server:
                        # 将服务端响应数据发往客户端
                        socket_client.send(data)

                time.sleep(self.delay) 
            except Exception as e:
                break

        socket_client.close()
        socket_server.close()

    def client_socket_accept(self):
        socket_client, _ = self.socket_proxy.accept()
        return socket_client

    def handle_client_request(self, socket_client):
        try:
            self.proxy(socket_client)
        except:
            pass

    def start(self):
        while True:
            try:
                # self.handle_client_request(self.client_socket_accept())
                thread.start_new_thread(self.handle_client_request, (self.client_socket_accept(), ))
            except KeyboardInterrupt:
                break
