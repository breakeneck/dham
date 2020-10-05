from http import Controller
from dht import DHT22
from machine import Pin

# class Firmware(Controller):



class Relay(Controller):
    def __init__(self, name, relay_pin, default_state=Controller.RELAY_OFF):
        self.name = name
        self.relay = Pin(relay_pin, Pin.OUT)
        self.relay.value(default_state)

    def index(self, data):
        value = self.relay.value()
        return {'current state': 'off' if value == self.RELAY_OFF else 'on'}

    def on(self, data):
        self.relay.value(self.RELAY_ON)
        return {'new state': 'on'}

    def off(self, data):
        self.relay.value(self.RELAY_OFF)
        return {'new state': 'off'}


class SSRelay(Controller):
    def __init__(self, name, relay_pin, default_state=Controller.SSRELAY_OFF):
        self.name = name
        self.relay = Pin(relay_pin, Pin.OUT)
        self.relay.value(default_state)

    def index(self, data):
        value = self.relay.value()
        return {'current state': 'off' if value == self.SSRELAY_OFF else 'on'}

    def on(self, data):
        self.relay.value(self.SSRELAY_ON)
        return {'new state': 'on'}

    def off(self, data):
        self.relay.value(self.SSRELAY_OFF)
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


class SwitchButton(Controller):
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

