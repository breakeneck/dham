from dht import DHT22
from machine import Pin, reset
from time import sleep


class Controller:
	name = ''

	def class_name(self):
		return self.name if self.name else self.__class__.__name__


class Firmware(Controller):
	@staticmethod
	def restart(request):
		request.send({'status': 'restarting'})
		sleep(1)
		reset()

	@staticmethod
	def read(request, filename):
		print('Content of ', filename)
		with open(filename, "r") as f:
			request.send({'content': f.read()})

	@staticmethod
	def write(request, filename):
		print('Writing file %s to machine: ' % filename)
		with open(filename, "w") as f:
			f.write(request.rawBody)
		request.send({'updated file': filename})


class Relay(Controller):
	RELAY_ON = 0
	RELAY_OFF = 1

	def __init__(self, name, relay_pin, default_state=RELAY_OFF):
		self.name = name
		self.relay = Pin(relay_pin, Pin.OUT)
		self.relay.value(default_state)

	def index(self, request):
		value = self.relay.value()
		request.send({'current state': 'off' if value == self.RELAY_OFF else 'on'})

	def on(self, request):
		self.relay.value(self.RELAY_ON)
		request.send({'new state': 'on'})

	def off(self, request):
		self.relay.value(self.RELAY_OFF)
		request.send({'new state': 'off'})


class InverseRelay(Relay):
	RELAY_ON = 1
	RELAY_OFF = 0


class Dht(Controller):
	def __init__(self, name, pin):
		self.name = name
		self.dht = DHT22(Pin(pin))

	def index(self, request):
		self.dht.measure()
		request.send({
			'temperature': self.dht.temperature(),
			'humidity': self.dht.humidity()
		})


class SwitchButton(Controller):
	BTN_ON = 1
	BTN_OFF = 0

	def __init__(self, name, btn_pin, action_on, action_off):
		self.name = name
		self.action_on = action_on
		self.action_off = action_off
		self.btn = Pin(btn_pin, Pin.OUT, Pin.PULL_UP)
		self.switch_state = self.BTN_OFF
		self.last_state = self.btn.value()

	def loop(self):
		if self.btn.value() != self.last_state and self.last_state == self.BTN_OFF:
			self.switch_state = self.BTN_ON if self.switch_state == self.BTN_OFF else self.BTN_OFF

			if self.switch_state == self.BTN_ON:
				if self.action_on:
					self.action_on()
			else:
				if self.action_off:
					self.action_off()

