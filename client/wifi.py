from network import WLAN, STA_IF
from ujson import load


def connect():
	with open('wifi.json', 'rt') as f:
		config = load(f)
	wlan = WLAN(STA_IF)
	wlan.active(True)
	wlan.ifconfig((config['static_ip'], config['netmask'], config['gateway'], config['gateway']))  # add static IP
	wlan.connect(config['ssid'], config['password'])
	while not wlan.isconnected():
		pass
