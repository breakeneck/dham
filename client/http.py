from request import Request


class WebServer:
	OFFLINE_ACTION = 'loop'

	connection = None
	route = ""
	headers = ""
	request = ""
	data = ""

	def __init__(self, controllers=None):
		self.request = Request()
		self.controllers = controllers or []

		while True:
			try:
				# Processing online actions
				self.handle_request()
				# Processing offline actions (used for track buttons state)
				for controller in self.controllers:
					if hasattr(controller, self.OFFLINE_ACTION):
						getattr(controller, self.OFFLINE_ACTION)()

			except Exception as e:
				self.request.send({'error': str(e)})

	def get_controller(self):
		capitalizedControllerName = self.request.controllerName[0:1].upper() + self.request.controllerName[1:]
		for controller in self.controllers:
			if controller.class_name() == capitalizedControllerName:  # self.request.controllerName.capitalize():
				return controller

	def get_action(self):
		controller = self.get_controller()

		if not controller:
			print('Controller %s Not Found' % self.request.controllerName)
			return None
		if not hasattr(controller, self.request.actionName):
			print('Action %s Not Found' % self.request.actionName)
			return None

		return getattr(controller, self.request.actionName)

	def handle_request(self):
		self.request.receive()
		self.get_action()(self.request, *self.request.params)


