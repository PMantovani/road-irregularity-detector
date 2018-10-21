class GsmHttpConnection(object):

    def __init__(self, host, path='', resource='', port=80):
        self.port = port
        self.host = host
        self.path = path
        self.resource = resource
        self.method = 'GET'
        self.headers = {}
        self.body = ''
        self.params = {}

    def set_method(self, method):
        self.method = method

    def set_body(self, body):
        self.body = body

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def build(self):
        request = self.method
        if len(self.path) > 0:
            if self.path[0] == '/':
                self.path = self.path[1:]

        if len(self.resource) > 0:
            if self.resource[0] == '/':
                self.resource = self.resource[1:]

        request += ' /' + self.path + '/' + self.resource
        request += ' HTTP/1.1\r\n'
        request += 'Host: GSMDevice\r\n\r\n'

        if len(self.body) > 0:
            request += self.body + '\r\n\r\n'

        return request
