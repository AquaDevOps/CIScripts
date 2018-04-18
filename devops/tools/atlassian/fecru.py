import requests
import json

class Respotory:
    def __init__(self, instance):
        self.instance = instance

    def put(self, namespace):
        response = requests.request(
            method='post', auth=(self.instance.username, self.instance.password), headers={
                'Accept': 'application/json', 'Content-Type': 'application/json'
            }, url='{resturl}/admin/repositories'.format(
                resturl=self.instance.resturl
            ), data=json.dumps({
                'type': 'git',
                'name': '_'.join(namespace.split('/')),
                'enabled': True,
                'storeDiff': True,
                'git': {
                    'location': 'http://jenkins@devops.gsafety.com/git/{namespace}.git'.format(namespace=namespace),
                    'auth': {'authType': 'password', 'password': 'jenkins123'},
                    'renameDetection': 'none'
                },
            })
        )
        if 201 == response.status_code:
            result = response.json()
            print('repository {name} created'.format(name=namespace))
            response = requests.request(
                method='put', auth=(self.instance.username, self.instance.password), headers={
                    'Accept': 'application/json', 'Content-Type': 'application/json'
                }, url='{resturl}/admin/repositories/{namespace}/{action}'.format(
                    resturl=self.instance.resturl,
                    namespace='_'.join(namespace.split('/')),
                    action='start'
                )
            )
            if 202 == response.status_code:
                print('repository {name} start accepted'.format(name=namespace))
                return result
            else:
                print(response.status_code)
                print(response.content)
        else:
            print(response.status_code)
            print(response.content)
        pass


class Fecru:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.repository = Respotory(self)
        self.resturl = '{url}/rest-service-fecru'.format(url=url)


