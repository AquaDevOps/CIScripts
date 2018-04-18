from snippets.sample_config import config
from devops.tools.scm import Gitlab
from devops.tools.scm.gitlab.helper import (DEVELOPER, MASTER, OWNER)


class Project:
    def __init__(self, sn, name):
        self.sn = sn
        self.name = name
        self.gitlab = Gitlab(config.gitlab.url, config.gitlab.token)

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


