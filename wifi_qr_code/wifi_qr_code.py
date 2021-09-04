from sys import platform
import wifi_qrcode_generator as qr
import os


class GenQRCode(object):
    def __init__(self):
        pass

    def run(self):
        if platform == 'linux' or platform == 'linux2':
            self.__linuxQRCode()
        elif platform == 'win32':
            self.__windowsQRCode()
        else:
            self.__defaultQRCode()

    def __linuxQRCode(self):
        _, ssid, _, security, _, password = os.popen(
            "nmcli device wifi show-password").read().split()
        self.__createQRCode(ssid, security, password)

    def __windowsQRCode(self):
        ssid = self.__windowsGetSSID()
        security = self.__windowsGetSecurity(ssid)
        password = self.__windowsGetPass(ssid)
        self.__createQRCode(ssid, security, password)

    def __windowsGetSSID(self):
        output = os.popen("netsh wlan show interfaces").read().split()
        for i in range(len(output)):
            if output[i] == "SSID":
                return output[i+2]

    def __windowsGetSecurity(self, ssid):
        output = os.popen(
            f"netsh wlan show profile {ssid} key=clear").read().split()
        for i in range(len(output)):
            if output[i] == 'Authentication' and "WPA" in output[i+2]:
                return "WPA"
            if output[i] == 'Authentication' and "WEP" in output[i+2]:
                return "WEP"

    def __windowsGetPass(self, ssid):
        output = os.popen(
            f"netsh wlan show profile {ssid} key=clear").read().split()
        for i in range(len(output)):
            if output[i] == 'Key' and output[i+1] == 'Content':
                return output[i+3]

    def __defaultQRCode(self):
        ssid = input("WiFi SSID (name): ")
        security = input("WiFi Security (either 'WPA' or 'WEP'): ")
        password = input("WiFi password: ")
        self.__createQRCode(ssid, security, password)

    def __createQRCode(self, ssid, security, password):
        qr.wifi_qrcode(ssid, False, security, password).save(f"{ssid}.png")


if __name__ == "__main__":
    GenQRCode().run()
