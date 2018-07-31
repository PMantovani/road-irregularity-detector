from GsmDevice import GsmDevice
from GsmHttpConnection import GsmHttpConnection
from GsmApnConfiguration import GsmApnConfiguration
import serial


if __name__ == "__main__":

    gsm = GsmDevice(serial.Serial('/dev/ttyS0', 115200))

    gsm_http_con = GsmHttpConnection("monetovani.com")

    gsm_apn_config = GsmApnConfiguration("zap.vivo.com.br", "vivo", "vivo")

    response_code, response_body  = gsm.send_http(gsm_http_con, gsm_apn_config)

    print response_code