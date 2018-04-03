import requests

class Gitlab:
    def __init__(self, host='http://devops.gsafety.com/git', api='v4', token=TOKEN):
        self.resturl = '{host}/api/{api}'.format(host=host, api=api)
        self.token = token