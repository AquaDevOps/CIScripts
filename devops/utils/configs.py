import os

from configparser import ConfigParser

from backports import configparser

class ConfigWrapper(object):
    def __init__(self):
        self.config = ConfigParser()

    def reload(self, path='config.ini', override=False):
        path = os.path.abspath(path)
        if os.path.exists(path):
            self.config.read(path)
        else:
            print('{path} does not exist'.format(path=path))

        if not os.path.exists(path) and override:
            self.config.write(open(path, 'w+'))

