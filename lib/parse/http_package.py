
class HttpRequestPacket(object):
    def __init__(self, data):
        self.parse(data)

    def parse(self, data):
        header_split = data.find(b'\r\n')
        data_split = data.find(b'\r\n\r\n')
    
        # 请求行 Request-Line
        self.request_line = data[:header_split]
        # 请求行由method、request uri、version组成
        self.method, self.request_uri, self.version = self.request_line.split() 
        
        # 请求头域 Request Header Fields
        self.request_header = data[header_split+2:data_split]
        self.headers = {}
        for header in self.request_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')
        
        # 请求数据
        self.request_data = data[data_split+4:]