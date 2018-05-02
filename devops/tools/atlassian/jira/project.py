from .helper import Helper
import json

class ProjectHelper(Helper):

    PROJECT_TYPE = {
        '项目管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-project-management'],
        '任务管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-task-management'],
        '流程管理': ['business', 'com.atlassian.jira-core-project-templates:jira-core-process-management'],
        'Basic': ['service desk', 'com.atlassian.servicedesk:classic-service-desk-project'],
        'IT Service Desk': ['service desk', 'com.atlassian.servicedesk:itil-service-desk-project'],
        'Customer service': ['service desk', ''],
        'Scrum开发方法': ['software', 'com.pyxis.greenhopper.jira:gh-scrum-template'],
        'Kanban开发方法': ['software', 'com.pyxis.greenhopper.jira:gh-kanban-template'],
        '基本开发方法': ['software', 'com.pyxis.greenhopper.jira:basic-software-development-template'],
    }


    def category(self, name):
        print(name)
        result = self.request(
            method='get',
            path='api/2/projectCategory',
        )
        if result:
            data = filter(lambda x: name == x['name'], result.json())
            data = list(data)
            if len(data)>0:
                return data[0]['id']
    # print get_categoryId_byName(u'公共安全云平台')

    def create(self, owner, key, project_type, name=None, model=None, description=None):

        project_data={
            "key": key,
            "name": name,
            "projectTypeKey": self.PROJECT_TYPE[project_type][0],
            "projectTemplateKey": self.PROJECT_TYPE[project_type][1],
            "description": description,
            "lead": owner,
            # "url": value['url'],
            # "assigneeType": "PROJECT_LEAD",
            # "avatarId": 10200,
            # "issueSecurityScheme": 10001,
            # "permissionScheme": 10011,
            # "notificationScheme": 10021,
            "categoryId": self.category(model) if model else '',
        }

        response = self.request(
            method='post',
            path='api/2/project',
            data=project_data
        )
        print('ss')
        if 201 == response.status_code:
            result = response.json()
            # print('project ({id}) {fullpath} created'.format(id=result['id'], fullpath=result['path_with_namespace']))
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def roles(self, key):
        response = self.request(
            method='get',
            path='api/2/project/{projectKey}/role'.format(projectKey=key)
        )
        if response.status_code == 200:
            result = response.json()
            roles_list = [
                {
                    'name': role,
                    'id': result[role].split('/')[-1]
                } for role in result.keys()
            ]
            return roles_list
        else:
            print(response.status_code)
            print(response.content)

    def add_members(self, key, roleName, members=[]):
        roles_list = self.roles(key=key)
        role = list(filter(lambda x: roleName == x['name'], roles_list))
        roleId = role[0]['id'] if role else ''
        if roleId:
            data = {
                'user': members
            }
            response = self.request(
                method='post',
                path='api/2/project/{projectKey}/role/{roleId}'.format(
                    projectKey=key,
                    roleId=roleId
                ),
                data=data
            )
            return response.json()
        else:
            return "failed"

    def delete_member(self, key, roleName, member):
        roles_list = self.roles(key=key)
        role = list(filter(lambda x: roleName == x['name'], roles_list))
        roleId = role[0]['id'] if role else ''
        if roleId:
            response = self.request(
                method='delete',
                path='api/2/project/{projectKey}/role/{roleId}?user={user}'.format(
                    projectKey=key,
                    roleId=roleId,
                    user=member
                ),
            )
            return response.json()
        else:
            return "failed"


    def get_members(self, key):
        roles_list = self.roles(key=key)
        field = {}
        print(roles_list)
        for r in roles_list:
            field[r['name']] = []
        for r in roles_list:
            roleId = r['id']
            response = self.request(
                method='get',
                path='api/2/project/{projectKey}/role/{roleId}'.format(
                    projectKey=key,
                    roleId=roleId,
                ),
            )
            result = response.json()
            print(result)
            field[r['name']] = [actor['name'] if actor else '' for actor in result['actors']]
        return field
