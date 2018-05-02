from snippets.sample_config import config
from devops.tools.scm import Gitlab
from devops.tools.scm.gitlab.helper import (DEVELOPER, MASTER, OWNER)
from devops.tools.scm import Subversion
from devops.tools.ldap import LDAP

class ProjectManager:
    def __init__(self, sn, name=None):
        self.sn = sn
        self.name = name
        self.gitlab = Gitlab(config.gitlab.url, config.gitlab.token)
        self.subversion = Subversion(
            config.subversion.url, config.subversion.username, config.subversion.password, config.subversion.workspace
        )
        self._ldap = None

    @property
    def ldap(self):
        if self._ldap is None:
            self._ldap = LDAP()
            # projects = [collect for collect in collection if 'aqua-group' in collect['objectClass']]
            # public_roles = [collect for collect in collection if 'aqua-role' in collect['objectClass']]

        # ldap.bind()
        # collection = ldap.collect(
        #     base='ou=workgroup,ou=group,ou=workspace,dc=gsafety,dc=com', include_root=False, flat=True
        # )
        # ldap.unbind()
        return self._ldap


    def ldap_reload(self):
        ldap = LDAP()
        ldap.bind()
        self._ldap = LDAP.collect(
            base='ou=workgroup,ou=group,ou=workspace,dc=gsafety,dc=com', include_root=False, flat=True
        )
        ldap.unbind()



    def git_group(self, owner, masters=[]):
        groupid = self.gitlab.group.create(self.sn, name=self.name)['id']
        self.gitlab.group.add_member(userid=self.gitlab.user.userid(owner), access_level=OWNER, groupid=groupid)
        for master in masters:
            self.gitlab.group.add_member(
                userid=self.gitlab.user.userid(master), access_level=MASTER, groupid=groupid
            )
        return groupid

    def git_repo(self, path, owner, groupid, name=None, members=[]):
        projectid = self.gitlab.project.create(
            path=path, name=name, owner=self.gitlab.user.userid(owner), groupid=groupid
        )['id']

        for member in [member for member in members if member not in [owner]]:
            self.gitlab.project.add_member(
                userid=self.gitlab.user.userid(member), access_level=DEVELOPER, projectid=projectid
            )
        self.gitlab.project.add_member(
            userid=self.gitlab.user.userid(owner), access_level=MASTER, projectid=projectid
        )
        return projectid

    def subversion_repo(self, path, owner, members=[]):
        self.subversion.create(owner=owner, group=self.sn, project=path, members=members)



