from http import Controller
from dht import DHT22
from machine import Pin


class Relay(Controller):
    def __init__(self, name, relay_pin):
        self.name = name
        self.relay = Pin(relay_pin, Pin.OUT)
        self.relay.value(1)  # default state is off

    def index(self, data):
        value = self.relay.value()
        return {'current state': 'off' if value == 1 else 'on'}

    def on(self, data):
        self.relay.value(0)
        return {'new state': 'on'}

    def off(self, data):
        self.relay.value(1)
        return {'new state': 'off'}


class Dht(Controller):
    def __init__(self, name, pin):
        self.name = name
        self.dht = DHT22(Pin(pin))

    def index(self, data):
        self.dht.measure()
        return {
            'temperature': self.dht.temperature(),
            'humidity': self.dht.humidity()
        }