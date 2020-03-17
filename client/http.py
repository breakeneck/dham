from socket import getaddrinfo, socket, SOL_SOCKET, SO_REUSEADDR
from ujson import loads, dumps
from machine import reset
from time import sleep


class WebServer:
    BUFF_SIZE = 536
    RESTART_ACTION = 'restart'
    PUT_ACTION = 'put/'
    GET_ACTION = 'get/'

    socket = None
    connection = None
    route = ""
    headers = ""
    request = ""
    data = ""

    def __init__(self, controllers=None):
        self.listen_socket()
        self.controllers = controllers or []
        print("\nServer is listening:\n")
        while True:
            try:
                self.handle_request()
            except Exception as e:
                self.send_json({'error': str(e)})

    def listen_socket(self):
        addr = getaddrinfo('0.0.0.0', 80)[0][-1]
        self.socket = socket()
        self.socket.bind(addr)
        self.socket.listen(1)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def receive_raw(self):
        data = ''
        while True:
            part = self.connection.recv(self.BUFF_SIZE)
            # print('part', len(part), '/', len(data), 'of', len(data))
            data += part.decode('utf-8')
            if len(part) < self.BUFF_SIZE:
                break
        return data

    def receive(self):
        self.connection, addr = self.socket.accept()

        r = self.receive_raw()
        # print('http_request:', r)
        self.route = r[r.index('/') + 1: r.index(' ', r.index('/'))]
        print('route:', self.route)
        self.request = r[r.index('\r\n\r\n') + 4:]
        if not self.request:
            return '{}'
        # print('request', self.request)
        return self.request

    def send_json(self, response_obj):
        print('response', response_obj)

        http_response = self.get_response_headers(response_obj)
        self.connection.send(http_response)
        self.connection.close()
        
    def send_error(self, e):
        self.send_json({'error': str(e)})

    @staticmethod
    def get_response_headers(response_obj):
        return """HTTP/1.1 200 OK
Connection: close
Content-type: application/json; charset=UTF-8

%s""" % (dumps(response_obj))

    def get_controller(self, raw_controller_name):
        controller_name = raw_controller_name[0:1].upper() + raw_controller_name[1:]
        
        for controller in self.controllers:
            if controller.class_name() == controller_name:
                return controller

    def get_action(self):
        if '/' not in self.route:
            raw_controller_name, action_name = self.route, 'index'
        else:
            raw_controller_name, action_name = self.route.split('/')
        controller = self.get_controller(raw_controller_name)
        if not controller:
            print('Controller Not Found')
            return None
        if not hasattr(controller, action_name):
            print('Action index Not Found')
            return None

        return getattr(controller, action_name)

    def handle_request(self):
        # Get request
        data = self.receive()
        # print('data', data)

        # Restart machine
        if self.route == self.RESTART_ACTION:
            self.send_json({'status': 'restarting'})
            sleep(1)
            reset()
        elif self.route[:4] == self.GET_ACTION:
            print('Content of ', self.route[4:])
            with open(self.route[4:], "r") as f:
                self.send_json({'content': f.read()})
        elif self.route[:4] == self.PUT_ACTION:
            print('Writing file %s to machine: ' % self.route[4:])
            with open(self.route[4:], "w") as f:
                f.write(data)
            self.send_json({'updated file': self.route[4:]})
        # Run controller
        else:
            action = self.get_action()
            if not action:
                self.send_json({'error': 'Route ' + self.route + ' not found'})
            else:
                request = loads(data)
                response = action(request)
                # Send response
                self.send_json(response)


class Controller:
    name: None

    def class_name(self):
        return self.name if self.name else self.__class__.__name__
