import os
from builtins import Exception

import paramiko as ssh
from devops.tools.scm.svn import template
from devops.tools.ldap.get_authz import get_members
from configparser import ConfigParser



class svn:
    def __init__(self, svn_home='/home/workspace/repos', host='172.17.38.181', password='intel@123'):
        self.client = ssh.SSHClient()
        self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        self.client.connect(host, port=22, username='root', password=password)

        self.svn_home = svn_home
        self.svn_repo_name = 'doc'

        self.template = template.catalog

    def create(self, owner, project_number, template, display_name, members=[]):

        display_name = self.svn_repo_name
        create_command = []
        command1 = 'mkdir {svn_home}/{project_number}'
        comm1 = command1.format(
            svn_home=self.svn_home,
            project_number=project_number
        )
        create_command.append(comm1)

        command2 = 'svnadmin create {svn_home}/{project_number}/{doc}'
        comm2 = command2.format(
            svn_home=self.svn_home,
            project_number=project_number,
            doc=display_name
        )
        create_command.append(comm2)

        command3 = 'svn mkdir file://{svn_home}/{project_number}/{doc}/{init}  -m "initial directories"'
        comm3 = command3.format(
            doc=display_name,
            svn_home=self.svn_home,
            project_number=project_number,
            init=self.template[template] if self.template.__contains__(template) else "{tags,trunk,branches}"
            # init="{tags,trunk,branches}"
        )
        create_command.append(comm3)

        repo_conf = """
<Location /svn/{project_number}>
  DAV svn
  SVNParentPath {svn_home}/{project_number}
  SVNListParentPath On

  AuthType Basic
  AuthName "Repositories of {project_number}"
  AuthzSVNAccessFile {svn_home}/{project_number}/{display_name}/authz

  Satisfy all
  Require valid-user

  AuthBasicProvider ldap

  AuthLDAPURL "ldap://172.17.38.163:10389/ou=user,ou=workspace,dc=gsafety,dc=com?uid?sub?(objectClass=aqua-user)"
</Location>
    """
        repo_conf = repo_conf.format(
            project_number=project_number,
            svn_home=self.svn_home,
            display_name=display_name
        )
        command4 = "echo '{repo_conf}' >>/etc/httpd/conf.d/subversion.conf"
        comm4 = command4.format(
            repo_conf=repo_conf,
        )
        create_command.append(comm4)

        repo_authz = """[groups]
developer = {user3}

[{doc}:/]
* = r

[{doc}:/*]
@developer = rw"""
        users = owner
        for user in members:
            users = users + ',' + user
        repo_authz = repo_authz.format(
            user3=users,
            doc=display_name
        )
        command5 = 'echo "{repo_authz}" >>{svn_home}/{project_number}/{display_name}/authz'
        comm5 = command5.format(
            project_number=project_number,
            svn_home=self.svn_home,
            repo_authz=repo_authz,
            display_name=display_name
        )
        create_command.append(comm5)

        comm6 = "systemctl restart httpd.service"
        create_command.append(comm6)
        try:
            for c in create_command:
                self.client.exec_command(c)
        except Exception as e:
            pass
        self.add_authz(display_name, project_number, members)

    def add_authz(self, display_name, project_number, members=[]):
        # add ldap

        groups = get_members(project_number, display_name)
        repo_groups = '[groups]'
        for r in groups.keys():
            repo_groups = repo_groups + """
""" + r + "="
            members = ','.join(groups[r])
            repo_groups = repo_groups + members
        repo_field = "[" + display_name + ":/]"
        for ff in groups.keys():
            repo_field = repo_field + """
@""" + ff + " = rw"

        repo_authz = """{groups}

{field}"""
        repo_auth = repo_authz.format(
            groups=repo_groups,
            field=repo_field
        )
        # print(repo_auth)

        create_command = None
        command5 = 'echo "{repo_authz}" >{svn_home}/{project_number}/{display_name}/authz'
        comm5 = command5.format(
            project_number=project_number,
            svn_home=self.svn_home,
            repo_authz=repo_auth,
            display_name=display_name
        )
        create_command.append(comm5)

        comm6 = "systemctl restart httpd.service"
        create_command.append(comm6)
        try:
            for c in create_command:
                self.client.exec_command(c)
        except Exception as e:
            pass

    def get_auth(self, project_number, display_name):
        c = 'cat {svn_home}/{project_number}/{display_name}/authz'
        c = c.format(
            svn_home=self.svn_home,
            project_number=project_number,
            display_name=display_name
        )
        stdin, stdout, stderr = self.client.exec_command(c)

        result = stdout.read()
        if not result:
            print("this is not authz")
            result = stderr.read()
            print(result.decode())
            return None
        else:
            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            with open('tmp/1.ini', 'w') as f:

                data = result.decode()
                f.write(data)
            config = ConfigParser()
            config.read('tmp/1.ini', 'utf-8')
            roles = config.options('groups')
            value = {}
            for r in roles:
                members = config.get('groups', r)
                members = members.split(',')
                value[r] = members
            print(value)
            return value

    def modify_ldap(self, project_number, display_name):
        if self.get_auth(project_number=project_number,
                         display_name=display_name) == get_members(project_number, display_name):
            return True
        else:
            return False
