import sys
import requests

IP = 'http://192.168.88.102'


def main(filename):
    with open(filename) as file:
        requests.post('%s/firmware/put/%s' % (IP, filename), data=file.read())


if __name__ == '__main__':
    main(*sys.argv[1:])
