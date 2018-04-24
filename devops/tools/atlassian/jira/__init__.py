from .applink import Applink
from .issue import IssueHelper

class Jira:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.resturl = '{url}/rest'.format(url=url)

        self.applink = Applink(self)
        self.issue = IssueHelper(self)
