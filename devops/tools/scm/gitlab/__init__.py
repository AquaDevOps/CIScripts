import os
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

    def create(self, owner, project_number, template, project_name, members):
        from devops.scripts.modify_project import modify_project_number
        project_number = modify_project_number(project_number)
        try:
            self.group.create(path=project_number, name=None)
        except Exception as e:
            print('pass')
        groupid = self.group.list(project_number)[0]['id']

        ownerid = self.user.list(search={'username': owner})[0]['id']
        # 将owner 以master 加入 group create 才不会报错
        self.group.add_member(userid=ownerid, access_level=40, groupid=groupid)
        name = project_name
        self.project.create(owner=ownerid, name=name, groupid=groupid, path=name)
        project = self.project.list(project_number + '/' + name)[0]['id']
        for r in members.keys():
            for member in members[r]:
                member = self.user.list(search={'username': member})[0]['id']
                try:
                    self.project.add_member(userid=member, access_level=ROLE_2_LEVEL[r], projectid=project)
                except Exception as e:
                    pass
        self.add_authz(project_name, project_number, members)
        return project

    def add_authz(self, project_name, project_number, members):
        # ldap
        from devops.tools.ldap.get_authz import add_project
        add_project(project_name=project_name, project_number=project_number, members=members)

        # if self.auth_ldap(project_number, project_name):
        if 1 == 1:
            for r in members.keys():
                for member in members[r]:
                    self.add_member(project_name=project_name,
                                    project_number=project_number,
                                    role=r,
                                    member=member)

    def get_auth(self, project_number, project_name):
        name = project_name
        project = self.project.list(project_number + '/' + name)[0]['id']

        print(project)

        members = self.project.get_members(project)
        field = {}
        for m in members:
            level = m['access_level']
            field[LEVEL_2_ROLE[level]] = []
        for m in members:
            level = m['access_level']
            field[LEVEL_2_ROLE[level]].append(m['username'])
        # owner only in group
        # group = self.group.list(project_number)[0]['id']
        # owners = self.group.get_members(group)
        # field['owner']=[]
        # for m in owners:
        #     field['owner'].append(m['username'])
        return field

    def auth_ldap(self, project_number, project_name):
        if self.get_auth(project_number=project_number,
                         project_name=project_name) == get_members(project_number, project_name):
            return True
        else:
            return False

    def get_difference(self, project_number, project_name, members):
        from devops.scripts.modify_project import diff
        conf_message = self.get_auth(project_number=project_number,
                                     project_name=project_name)
        ldap_message = get_members(project_number=project_number, project_name=project_name)
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        print(ldap_message)
        print(conf_message)
        with open('tmp/commit.ini', 'a') as f:
            if ldap_message == conf_message:
                data = diff(old=ldap_message, new=members)
                f.write('\n'+project_number+ ' : ' + project_name)
                f.write(data)
                return True
            else:
                f.write('\n'+project_number+ ' : ' + project_name)
                data = diff(old=conf_message, new=members)
                f.write(data)
                return False

    def add_member(self, project_number, project_name, role, member):
        project = self.project.list(project_number + '/' + project_name)[0]['id']
        group = self.group.list(project_number)[0]['id']
        if role == 'owner':
            member = self.user.list(search={'username': member})[0]['id']
            result = self.group.add_member(userid=member, access_level=ROLE_2_LEVEL[role], groupid=group)
        else:
            member = self.user.list(search={'username': member})[0]['id']
            result = self.project.add_member(userid=member, access_level=ROLE_2_LEVEL[role], projectid=project)
        return result

    def delete_member(self, project_number, project_name, role, member):
        project = self.project.list(project_number + '/' + project_name)[0]['id']
        group = self.group.list(project_number)[0]['id']
        if role == 'owner':
            member = self.user.list(search={'username': member})[0]['id']
            self.group.delete_member(userid=member, groupid=group)
        else:
            member = self.user.list(search={'username': member})[0]['id']
            self.project.delete_member(userid=member, projectid=project)

    def modify_authz(self, project_name, project_number, members):
        # ldap
        from devops.tools.ldap.get_authz import modify_project
        modify_project(project_name=project_name, project_number=project_number, members=members)

        old = self.get_auth(project_number=project_number,
                            project_name=project_name)
        new = members
        message = '\n'
        old_role_list = []
        for k in old.keys():
            old_role_list.append(k)
        for n_k in new.keys():
            if n_k in old_role_list:
                for n_m in new[n_k]:
                    if n_m in old[n_k]:
                        old[n_k].remove(n_m)
                    else:
                        self.add_member(project_name=project_name,
                                        project_number=project_number,
                                        role=n_k,
                                        member=n_m)
                        message = message + '\n' + ' add ' + n_m + ' to ' + n_k
                if len(old[n_k]):
                    for o_m in old[n_k]:
                        self.delete_member(project_name=project_name,
                                           project_number=project_number,
                                           role=n_k,
                                           member=o_m)
                        message = message + '\n' + ' delete ' + o_m + ' from ' + n_k
                old_role_list.remove(n_k)
            else:
                for on_m in new[n_k]:
                    self.add_member(project_name=project_name,
                                    project_number=project_number,
                                    role=n_k,
                                    member=on_m)
                message = message + '\n' + ' add role ' + n_k + ', memebers : ' + ','.join(new[n_k])
        if len(old_role_list):
            for o_k in old_role_list:
                for on_m in old[o_k]:
                    self.delete_member(project_name=project_name,
                                       project_number=project_number,
                                       role=o_k,
                                       member=on_m)
                message = message + '\n' + ' delete role ' + o_k + ', members : ' + ','.join(old[o_k])
        print(message)
        self.get_difference(project_number, project_name, members)

    def modify_authz_ldap(self, project_name, project_number, members):
        # ldap
        from devops.tools.ldap.get_authz import modify_project
        modify_project(project_name=project_name, project_number=project_number, members=members)