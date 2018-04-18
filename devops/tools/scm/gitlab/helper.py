import requests


GUEST = 10
REPORTER = 20
DEVELOPER = 30
MASTER = 40
OWNER = 50

ROLE_2_LEVEL = {'guest': 10, 'reporter': 20, 'developer': 30, 'master': 40, 'owner': 50}
LEVEL_2_ROLE = {level: role for role, level in ROLE_2_LEVEL.items()}


class Helper:
    def __init__(self, instance):
        self.instance = instance

    def request(self, path, method='get', headers={}, params={}, data={}):
        url = '{resturl}/{path}'.format(resturl=self.instance.resturl, path=path)
        print(url)

        return requests.request(
            method=method.lower(),
            url=url,
            headers=dict({'PRIVATE-TOKEN': self.instance.token}, **headers),
            params=params,
            data=data
        )

    def pager(self, path, headers={}, params={}, data={}, page=1):
        response = self.request(
            path, headers=headers, params=params, data=dict({'per_page': 16, 'page': page}, **data)
        )
        if 200 == response.status_code:
            collection = response.json()
            return collection if len(collection) < 16 else collection + self.pager(
                path, headers=headers, params=params, data=data, page=page + 1
            )
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

