import requests
import json


class Helper:
    PAGESIZE = 16

    def __init__(self, instance):
        self.instance = instance

    def request(self, path, method='get', headers={}, params={}, data={}):
        url = '{resturl}/{path}'.format(resturl=self.instance.resturl, path=path)
        print(url)

        return requests.request(method=method, url=url, params=params, data=json.dumps(data), headers=dict(headers, **{
            'Accept': 'application/json', 'Content-Type': 'application/json'
        }), auth=(
            self.instance.username, self.instance.password
        ))

    def pager(self, path, headers={}, params={}, data={}, page=0, result_key=None):
        response = self.request(
            path, method='post', headers=headers, params=params, data=dict({
                'maxResults': Helper.PAGESIZE, 'startAt': page*Helper.PAGESIZE
            }, **data)
        )
        if 200 == response.status_code:
            collection = response.json()[result_key] if result_key else response.json()
            return collection if len(collection) < Helper.PAGESIZE else collection + self.pager(
                path, headers=headers, params=params, data=data, page=page + 1, result_key=result_key
            )
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

