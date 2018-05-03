import requests
import json

ROLE_TYPE = {
    'guest': 'User',
    'reporter': 'QA',
    'developer': 'Developers',
    'master': 'Manager',
    'owner': 'Tempo Project Managers'
}

PROJECT_TYPE = {
    '项目管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-project-management'],
    '任务管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-task-management'],
    '流程管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-process-management'],
    'Basic': ['service desk', 'com.atlassian.servicedesk:classic-service-desk-project'],
    'IT Service Desk': ['service desk', 'com.atlassian.servicedesk:itil-service-desk-project'],
    # 'Customer service': ['service desk', ''],
    'Scrum开发方法': ['software', 'com.pyxis.greenhopper.jira:gh-scrum-template'],
    'Kanban开发方法': ['software', 'com.pyxis.greenhopper.jira:gh-kanban-template'],
    '基本开发方法': ['software', 'com.pyxis.greenhopper.jira:basic-software-development-template'],
}

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

