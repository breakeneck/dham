import sys
import requests


class Upload:
    NODES_DIR = 'nodes/'
    RESTART_ROUTE = 'firmware/restart'
    SHARED_FILES = [
        'board.py',
        'controller.py',
        'http.py',
        'request.py',
        'wifi.py',
    ]
    USER_FILES = [
        'main.py',
        'wifi.json'
    ]
    NODES = {
        'altar': '192.168.88.102'
    }

    def single(self, nodeName, filename, asFilename=None):
        with open(filename) as file:
            url = 'http://%s/firmware/put/%s' % (self.NODES[nodeName], filename if not asFilename else asFilename)
            requests.post(url, data=file.read())


    def shared(self, nodeName):
        for file in self.SHARED_FILES:
            self.single(nodeName, file)

    def user(self, nodeName):
        for file in self.USER_FILES:
            self.single(nodeName, self.NODES_DIR + nodeName + '/' + file, file)

    def firmware(self, nodeName):
        self.shared(nodeName)
        self.user(nodeName)

        requests.post('http://%s/%s' % (self.NODES[nodeName], self.RESTART_ROUTE))


    def run(self, argv):
        action, node = argv[1], argv[2]
        getattr(self, action)(*argv[3:])



upload = Upload()
upload.run(sys.argv)

