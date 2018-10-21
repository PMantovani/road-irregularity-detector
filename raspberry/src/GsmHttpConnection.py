class GsmHttpConnection(object):

    def __init__(self, host, path='', resource='', port=80):
        self.port = port
        self.host = host
        self.path = path
        self.resource = resource
        self.method = 'GET'
        self.headers = {'Host': host}
        self.body = ''
        self.params = {}

    def set_method(self, method):
        self.method = method

    def set_body(self, body):
        self.body = body
        self.headers['Content-Length'] = len(body)

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def build(self):
        request = self.method
        if self.path:
            if self.path[0] == '/':
                self.path = self.path[1:]

        if self.resource:
            if self.resource[0] == '/':
                self.resource = self.resource[1:]

        request += ' '
        if self.path != '':
            request += '/' + self.path

        request += '/' + self.resource
        request += ' HTTP/1.1\r\n'
        for header, value in self.headers.items():
            request += header + ': ' + str(value) + '\r\n'
        request += '\r\n'

        if self.body:
            request += self.body

        return request
