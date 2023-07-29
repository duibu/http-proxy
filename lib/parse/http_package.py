
class HttpRequestPacket(object):
    '''
    HTTP请求包
    '''
    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data):
        '''
        解析一个HTTP请求数据包
        GET http://test.wengcx.top/index.html HTTP/1.1\r\nHost: test.wengcx.top\r\nProxy-Connection: keep-alive\r\nCache-Control: max-age=0\r\n\r\n
        
        参数：data 原始数据
        '''
        header_split = data.find(b'\r\n') # 请求行与请求头的分隔位置
        data_split = data.find(b'\r\n\r\n') # 请求头与请求数据的分隔位置
    
        # 请求行 Request-Line
        self.req_line = data[:header_split]
        self.method, self.req_uri, self.version = self.req_line.split() # 请求行由method、request uri、version组成
        
        # 请求头域 Request Header Fields
        self.req_header = data[header_split+2:data_split]
        self.headers = {}
        for header in self.req_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')
        
        # 请求数据
        self.req_data = data[data_split+4:]