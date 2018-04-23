from builtins import Exception

from devops.tools.ldap.get_authz import get_members
from .project import ProjectHelper
from .group import GroupHelper
from .user import UserHelpder
from .helper import ROLE_2_LEVEL, LEVEL_2_ROLE


class Gitlab:

    def __init__(self, url, token, api='v4'):
        self.url = url
        self.token = token
        self.resturl = '{url}/api/{api}'.format(url=url, api=api)

        self.project = ProjectHelper(self)
        self.group = GroupHelper(self)
        self.user = UserHelpder(self)

    def create(self, owner, project_number, template, display_name, members=[]):
        self.group.create(path=project_number, name=None)
        groupid = self.group.list(project_number)[0]['id']

        ownerid = self.user.list(search={'username': owner})[0]['id']
        self.group.add_member(userid=ownerid, access_level=50, groupid=groupid)
        name = display_name
        self.project.create(owner=ownerid, name=name, groupid=groupid, path=name)
        project = self.project.list(project_number+'/'+name)[0]['id']
        if members:
            for member in members:
                member = self.user.list(search={'username': member})[0]['id']
                try:
                    self.project.add_member(userid=member, access_level=30, projectid=project)
                except Exception as e:
                    pass
        self.add_authz(display_name, project_number, members)

    def add_authz(self, display_name, project_number, members=[]):
        # add ldap
        groups = get_members(project_number)
        name = display_name
        project = self.project.list(project_number+'/'+name)[0]['id']
        for r in groups.keys():
            for member in groups[r]:
                member = self.user.list(search={'username': member})[0]['id']
                try:
                    self.project.add_member(userid=member, access_level=ROLE_2_LEVEL[r], projectid=project)
                except Exception as e:
                    pass

    def get_auth(self, project_number, display_name):
        name = display_name
        project = self.project.list(project_number+'/'+name)[0]['id']
        members = self.project.get_members(project)
        field={}
        for m in members:
            level = m['access_level']
            field[LEVEL_2_ROLE[level]]=[]
        for m in members:
            level = m['access_level']
            field[LEVEL_2_ROLE[level]].append(m['username'])
        return field

    def modify_ldap(self, project_number, display_name):
        if self.get_auth(project_number=project_number,
                         display_name=display_name) == get_members(project_number, display_name):
            return True
        else:
            return False


