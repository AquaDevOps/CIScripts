from devops.tools.ldap.get_authz import get_members
from .project import ProjectHelper
from .group import GroupHelper
from .user import UserHelpder


class Gitlab:

    def __init__(self, url, token, api='v4'):
        self.url = url
        self.token = token
        self.resturl = '{url}/api/{api}'.format(url=url, api=api)

        self.project = ProjectHelper(self)
        self.group = GroupHelper(self)
        self.user = UserHelpder(self)

    def create(self, owner, project_number, template=None):
        groups = get_members(project_number)
        names = []
        members =[]
        for g in groups:
            names = g['field']
            members = g['members']
        self.group.create(path=project_number, name=None)
        groupid = self.group.list(project_number)[0]['id']

        ownerid = self.user.list(search={'username': owner})[0]['id']
        self.group.add_member(userid=ownerid, access_level=50, groupid=groupid)
        for name in names:
            self.project.create(owner=ownerid, name=name, groupid=groupid, path=name)
            project = self.project.list(project_number+'/'+name)[0]['id']
            if len(members) > 0:
                for member in members:
                    member = self.user.list(search={'username': member})[0]['id']
                    try:
                        self.project.add_member(userid=member, access_level=30, projectid=project)
                    except Exception as e:
                        pass