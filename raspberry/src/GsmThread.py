from threading import Thread
from GsmException import GsmException

class GsmThread(Thread):

    def __init__(self, gsm_device):
        Thread.__init__(self)
        self.gsm_device = gsm_device
        self.apn_config = False
        self.http_config = False

        self.gsm_device.enable_gps()
        self.latitude = 0.0
        self.longitude = 0.0
        self.speed = 0.0
        self.course = 0.0
        self.gps_validity = False

        self.pending_http_request = False
        self.response_body = ''
        self.response_code = 0

    def get_coordinates(self):
        return self.latitude, self.longitude

    def get_speed(self):
        return self.speed

    def get_gps_validity(self):
        return self.gps_validity

    def set_apn_config(self, apn_config):
        self.apn_config = apn_config

    def set_http_config(self, http_config):
        self.http_config = http_config

    def trigger_http_request(self):
        self.pending_http_request = True

    def has_http_response(self):
        return bool(self.response_body)

    def get_http_response(self):
        response = self.response_code, self.response_body
        self.response_code = 0
        self.response_body = ''
        return response

    def run(self):
        while True:
            try:
                if self.pending_http_request:
                    self.pending_http_request = False
                    code, body = self.gsm_device.send_http(self.http_config, self.apn_config)
                    self.response_body = body
                    self.response_code = code

                else:
                    gps_info = self.gsm_device.get_gps_info()
                    fix, lat, lng, speed, course = gps_info
                    if fix == '0':
                        self.gps_validity = False
                    else:
                        self.gps_validity = True
                        self.latitude = float(lat)
                        self.longitude = float(lng)
                        self.speed = float(speed)
                        self.course = float(course)

            except GsmException:
                    self.pending_http_request = False
                    self.response_code = -1
                    self.response_body = 'GSM Exception'
