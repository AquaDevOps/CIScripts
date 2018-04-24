import requests
import json


class Applink:

    def __init__(self, instance):
        self.instance = instance

    def list_applink(self, filter_fun=lambda x: True):
        response = requests.request(
            method='get', url='{resturl}/applinks/1.0/applicationlink'.format(resturl=self.instance.resturl), headers={
                'Accept': 'application/json', 'Content-Type': 'application/json'
            }, auth=(self.instance.username, self.instance.password)
        )
        if 200 == response.status_code:
            return list(filter(
                filter_fun, response.json()['applicationLinks']
            )) if filter_fun else response.json()['applicationLinks']
        else:
            print(response.status_code)
            print(response.content)

    def list_entity(self, appid, filter_fun=lambda x: True):
        response = requests.request(
            method='get', url='{resturl}/applinks/1.0/entities/{appid}'.format(
                resturl=self.instance.resturl, appid=appid
            ), headers={
                'Accept': 'application/json', 'Content-Type': 'application/json'
            }, auth=(self.instance.username, self.instance.password)
        )
        if 200 == response.status_code:
            return list(filter(filter_fun, response.json()['entity'])) if filter_fun else response.json()['entity']
        else:
            print(response.status_code)
            print(response.content)

    def put(self, key, appid, linktype, linkkey, linkname=None):
        linkname = linkkey if linkname is None else linkname
        response = requests.request(
            method='put', auth=(self.instance.username, self.instance.password), headers={
                'Accept': 'application/json', 'Content-Type': 'application/json'
            }, url='{resturl}/applinks/1.0/entitylink/{type}/{key}'.format(
                resturl=self.instance.resturl,
                type='com.atlassian.applinks.api.application.jira.JiraProjectEntityType',
                key=key
            ), data=json.dumps({'applicationId': appid, 'typeId': linktype, 'name': linkname, 'key': linkkey})
        )
        if 201 == response.status_code:
            print('linked {key} via {linktype} with {linkkey}'.format(key=key, linktype=linktype, linkkey=linkkey))
            return linkkey
        else:
            print(response.status_code)
            print(response.content)