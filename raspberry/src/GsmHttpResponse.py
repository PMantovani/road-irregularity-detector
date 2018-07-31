class GsmHttpResponse(object):

    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.return_code = -1
        self.response_body = ''
        self.parse(self.raw_response)

    def parse(self, raw_response):
        split_string = raw_response.split('\r\n\r\nSEND OK\r\n')
        response = split_string[1]

        end_first_line_idx = response.find('\n')

        if end_first_line_idx == -1:
            raise Exception

        first_line = response[0:end_first_line_idx]
        self.return_code = first_line.split(' ')[1]

        response_parts = response.split('\r\n\r\n')
        if len(response_parts) > 0:
            self.response_body = response_parts[1]
        else:
            self.response_body = ''

    def get_return_code(self):
        return self.return_code

    def get_response(self):
        return self.response_body
