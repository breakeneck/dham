from socket import getaddrinfo, socket, SOL_SOCKET, SO_REUSEADDR
from ujson import loads, dumps


class Request:
	BUFF_SIZE = 536

	def __init__(self):
		self.connection = None
		self.socket = self.socket()
		self.socket.bind(getaddrinfo('0.0.0.0', 80)[0][-1])
		self.socket.listen(1)
		self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		print("\nServer is listening at %s:\n")
		# Request params
		self.route = ''
		self.rawBody = '{}'
		self.controllerName = ''
		self.actionName = ''
		self.params = ()

	def get_raw_request(self):
		data = ''
		while True:
			part = self.connection.recv(self.BUFF_SIZE)
			# print('part', len(part), '/', len(data), 'of', len(data))
			data += part.decode('utf-8')
			if len(part) < self.BUFF_SIZE:
				break
		return data

	def receive(self):
		self.connection = self.socket.accept()

		r = self.get_raw_request()

		self.parseRoute(r[r.index('/') + 1: r.index(' ', r.index('/'))])
		self.parseBody(r[r.index('\r\n\r\n') + 4:])

	def parseRoute(self, route):
		if route('/') == 0:
			self.route = route + '/index/'
		elif route.count('/') == 1:
			self.route =  route + '/'
		else:
			self.route = route

		self.controllerName, self.actionName, *self.params = self.route.split('/')
		print('route:', self.route, self.controllerName, self.actionName, self.params)

	def parseBody(self, rawBody):
		self.rawBody = '{}' if not rawBody else rawBody

	def getJsonBody(self):
		return loads(self.rawBody)

	def send(self, response_obj):
		print('response', response_obj)

		http_response = self.get_response_headers(response_obj)
		self.connection.send(http_response)
		self.connection.close()

	@staticmethod
	def get_response_headers(response_obj):
		return """HTTP/1.1 200 OK
Connection: close
Content-type: application/json; charset=UTF-8

%s""" % (dumps(response_obj))

	def send_error(self, e):
		self.send({'error': str(e)})