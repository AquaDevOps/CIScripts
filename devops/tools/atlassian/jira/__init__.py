from .applink import Applink
from .issue import IssueHelper
from .project import ProjectHelper

class Jira:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.resturl = '{url}/rest'.format(url=url)

        self.applink = Applink(self)
        self.issue = IssueHelper(self)
        self.project = ProjectHelper(self)

    def create(self, owner, project_number, template, project_name, members):
        self.project.create(
            owner=owner,
            key=project_number,
            project_type=template,
            name=project_name,
        )
        self.init_authz(project_number=project_number,project_name=project_name,members=members)


    def init_authz(self, project_name, project_number, members):
        # jira auzh
        for roleName in members.keys():
            self.project.add_members(
                key=project_number,
                roleName=roleName,
                members=members[roleName]
            )
        # ldap auzh
        # from devops.tools.ldap.get_authz import add_project
        # add_project(project_name=project_name, project_number=project_number, members=members)