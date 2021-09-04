# WiFi QR Code Generator

Tired of people always asking for your WiFi password? This script generates a QR code for you and your friends to use to automatically connect to your WiFi.

## How it works
This script uses the ****wifi_qrcode_generator**** library. [Here](https://github.com/lakhanmankani/wifi_qrcode_generator) is a link to the documentation.

****wifi_qr_code.py**** will automatically gather the credentials for the WiFi connection you are currently using. 

#### NOTE: Only Linux is currently configured to automatically grab active WiFi credentials in this version. For OS's not pre-configured you must manually type in the credentials (SSID, security and password).

## How to use
Install wifi_qrcode_generator
```
pip3 install wifi_qrcode_generator
```

Run the script
```
python3 wifi_qr_code.py
```

That easy!
