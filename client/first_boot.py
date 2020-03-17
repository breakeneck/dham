
from network import WLAN, STA_IF

wlan = WLAN(STA_IF)
wlan.active(True)
with open('first_boot_wifi.txt') as f:
    for line in f:
        ssid, password = line.split(':')
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass
print('\nFirmware with: php firmware.php {location} ', wlan.ifconfig()[0])

WebServer()
