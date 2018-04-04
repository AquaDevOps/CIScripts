from .project import ProjectHelper
from .group import GroupHelper
from .user import UserHelpder


class Gitlab:
    def __init__(self, host, token, api='v4'):
        self.host = host
        self.token = token
        self.resturl = '{host}/api/{api}'.format(host=host, api=api)

        self.project = ProjectHelper(self)
        self.group = GroupHelper(self)
        self.user = UserHelpder(self)


