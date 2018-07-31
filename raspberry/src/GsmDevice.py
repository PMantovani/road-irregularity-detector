from GsmException import GsmException
from GsmHttpResponse import GsmHttpResponse

class GsmDevice(object):

    def __init__(self, serial):
        self.serial = serial

    def send_http(self, httpConnection, apnConfiguration):

        if not self.has_ip_address():
            self.send_and_check('AT+CFUN=1')
            self.send_and_check('AT+CGATT=1')
            self.send_and_check('AT+CIPSHUT')
            self.send_and_check('AT+CIPMUX=0')
            self.send_and_check('AT+CSTT=' + apnConfiguration.get_apn() + ',' +
                                            apnConfiguration.get_user() + ',' +
                                            apnConfiguration.get_password())
            self.send_and_check('AT+CIICR')
            self.send_and_check('AT+CIFSR')
        else:
            self.send_and_read('AT+CIPCLOSE')
        self.send_and_check_cipstart('TCP', httpConnection.get_host(),
                                            httpConnection.get_port())

        request = httpConnection.build()

        self.send_and_read('AT+CIPSEND=' + str(len(request)))
        self.send(request + '\x1A')
        raw_response = self.read_until_closed()

        response = GsmHttpResponse(raw_response)
        return response.get_return_code(), response.get_response()

    def has_ip_address(self):
        try:
            self.send_and_check('AT+CIFSR')
        except GsmException:
            return False
        return True

    def send_and_check(self, at_command):
        self.serial.write(at_command + '\r\n')
        self.serial.readline()
        if self.serial.readline() == 'ERROR\r\n':
            raise GsmException
    
    def send_and_check_cipstart(self, protocol, host, port):
        self.serial.write('AT+CIPSTART="' + protocol +
                          '","' + host + '",' + str(port) + '\r\n')
        self.serial.readline()
        self.serial.readline()
        self.serial.readline()
        if self.serial.readline() != 'CONNECT OK\r\n':
            raise GsmException

    def send_and_read(self, at_command):
        self.serial.write(at_command + '\r\n')
        self.serial.readline()

    def send(self, at_command):
        self.serial.write(at_command + '\r\n')

    def read_until_closed(self):
        response = ''
        self.serial.readline()
        while True:
            line = self.serial.readline()
            if line != 'CLOSED\r\n':
                response += line
            else:
                return response
