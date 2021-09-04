from sys import platform
import wifi_qrcode_generator as qr
import os


class GenQRCode(object):
    def __init__(self):
        pass 

    def run(self):
        if platform == 'linux' or platform == 'linux2':
            self.__linuxQRCode()
        else:
            self.__defaultQRCode()

    def __linuxQRCode(self):
        _, ssid, _, security, _, password = os.popen("nmcli device wifi show-password").read().split()
        self.__createQRCode(ssid, security, password)

    def __defaultQRCode(self):
        ssid = input("WiFi SSID (name): ")
        security = input("WiFi Security (either 'WPA' or 'WEP'): ")
        password = input("WiFi password: ")
        self.__createQRCode(ssid, security, password)

    def __createQRCode(self, ssid, security, password):
        qr.wifi_qrcode(ssid, False, security, password).save(f"{ssid}.png")
        

if __name__ == "__main__":
    GenQRCode().run()