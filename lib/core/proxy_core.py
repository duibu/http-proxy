import socket
import select
import time
import _thread as thread
from lib.parse.http_package import HttpRequestPacket
from lib.core import extends
from lib.core.log import logger

#简单的HTTP代理
class HttpProxy(object):

    def __init__(self, host='127.0.0.1', port=8080, listen=10, bufsize=8, delay=1):
        
        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.socket_proxy.bind((host, port))
        self.socket_proxy.listen(listen)

        self.socket_recv_bufsize = bufsize*1024
        self.delay = delay/1000.0

        logger.info('bind=%s:%s' % (host, port))
        logger.info('listen=%s' % listen)
        logger.info('bufsize=%skb, delay=%sms' % (bufsize, delay))

    def delete(self):
        self.socket_proxy.close()
    
    def connect(self, host, port):
        (schema, socket_type, _, _, target_address) = socket.getaddrinfo(host, port)[0]
        connect_socket = socket.socket(schema, socket_type)
        connect_socket.setblocking(0)
        connect_socket.settimeout(5)
        connect_socket.connect(target_address)
        return connect_socket
         
    def proxy(self, socket_client):

        req_data = socket_client.recv(self.socket_recv_bufsize)

        if req_data == b'':
            return

        # 解析http请求数据
        http_info = HttpRequestPacket(req_data)
        custom_headers = extends.header(header=http_info.headers,data=http_info.req_data)

        if custom_headers:
            logger.info('自定义Header -> [%s]' % custom_headers)
            req_data = req_data.decode().replace('\r\n\r\n', '\r\n'+'\r\n'.join('%s: %s' % (k,v) for k,v in custom_headers.items())+'\r\n\r\n', 1)

        if b':' in http_info.host:
            server_host, server_port = http_info.host.split(b':')
        else:
            server_host, server_port = http_info.host, 80

        u = b'%s//%s' % (http_info.req_uri.split(b'//')[0], http_info.host)
        req_data = req_data.replace(u.decode(), '', 1)

        # HTTP
        if http_info.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:

            socket_server = self.connect(server_host, server_port)
            socket_server.send(req_data.encode())

        self.nonblocking(socket_client, socket_server)


    #异步处理
    def nonblocking(self, socket_client, socket_server):
        in_list = [socket_client, socket_server]
        is_recv = True
        while is_recv:
            try:
                socket_list, _, elist = select.select(in_list, [], [], 2)
                if elist:
                    break
                for this_socket in socket_list:
                    is_recv = True
                    
                    data = this_socket.recv(self.socket_recv_bufsize)
                    if data == b'':
                        is_recv = False
                        continue

                    # client -> server
                    if this_socket is socket_client:
                        socket_server.send(data)

                    # server -> client
                    elif this_socket is socket_server:
                        socket_client.send(data)

                time.sleep(self.delay) 
            except Exception as e:
                print(e)
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
                thread.start_new_thread(self.handle_client_request, (self.client_socket_accept(),))
            except KeyboardInterrupt:
                break
