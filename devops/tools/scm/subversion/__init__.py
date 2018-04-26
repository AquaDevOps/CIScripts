import os

import paramiko as ssh
from devops.tools.scm.subversion import template
from devops.tools.ldap.get_authz import get_members
from configparser import ConfigParser
from snippets.sample_config import config
from io import StringIO

class Subversion:
    class SSHWrapper:
        def __init__(self, host, username, password, port=22):
            self.host = host
            self.username = username
            self.password = password
            self.port = port
            self.client = ssh.SSHClient()
            self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())

        def connect(self):
            self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
            return self.client

        def execute(self, command):
            print('executing : {}'.format(command))
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout = stdout.read()
            stderr = stderr.read()
            for line in stdout.splitlines():
                print('[STDOUT] {}'.format(line))
            for line in stderr.splitlines():
                print('[STDERR] {}'.format(line))
            print('')
            return stdout, stderr

        def close(self):
            self.client.close()

    def __init__(self, url, username, password, workspace, port=22, conf='/etc/httpd/conf.d/subversion.conf'):
        self.ssh = Subversion.SSHWrapper(url, username, password, port)
        self.url = "http://" + url
        self.conf = conf
        self.workspace = workspace
        self.template = template.catalog

    def create(self, owner, group, project, template='工程项目', members=[]):
        self.ssh.connect()
        self.ssh.execute('mkdir {workspace}/{group} -p'.format(workspace=self.workspace, group=group))

        # ==================================================
        # Check project folder not exist
        # ==================================================
        stdout, stderr = self.ssh.execute('stat {workspace}/{group}/{project}'.format(
            workspace=self. workspace, group=group, project=project
        ))
        # assert not stdout, "project folder [{workspace}/{group}/{project}] already exist".format(
        #     workspace=self.workspace, group=group, project=project
        # )
        if stdout:
            print('project folder exist')
            # self.ssh.close()
            # return

        # ==================================================
        # Create Repo for Project
        # ==================================================
        stdout, stderr = self.ssh.execute('svnadmin create {workspace}/{group}/{project}'.format(
            workspace=self.workspace, group=group, project=project
        ))
        if stderr:
            print('repository exist')
            # self.ssh.close()
            # return

        # ==================================================
        # Create initial directories
        # ==================================================
        stdout, stderr = self.ssh.execute(
            'svn mkdir file://{workspace}/{group}/{project}/{{{directories}}} -m "{message}"'.format(
                workspace=self.workspace, group=group, project=project,
                directories=','.join(['tags', 'trunk', 'branches']), message='create initial directories'
            )
        )
        if stderr:
            print('file already exists')
            # self.ssh.close()
            # return

        # ==================================================
        # Create templated directories
        # ==================================================
        if template in self.template:
            stdout, stderr = self.ssh.execute(
                'svn mkdir file://{workspace}/{group}/{project}/trunk/{{{directories}}} -m "{message}"'.format(
                    workspace=self.workspace, group=group, project=project,
                    directories=','.join(self.template[template]),
                    message='create templated directories for {template}'.format(template=template)
                )
            )
            if stderr:
                print('file already exists')
                # self.ssh.close()
                # return

        # ==================================================
        # Check or Create repo configuration
        # ==================================================
        # delete all svn/repos
        repos_delete = "sed -i.bak '/^\s*{prefix}/,/^\s*{suffix}/d' {file}".format(
            prefix='<Location /svn/'.replace('/', '\/'), suffix='</Location>'.replace('/', '\/'), file=self.conf
        )
        # delete specific svn/repos's contents
        repo_delete = "sed -i.bak '/^\s*{prefix}/,/^\s*{suffix}/{{/^\s*{prefix}\|^\s*{suffix}/!d}}' {file}".format(
            prefix='<Location /svn/{group}>'.format(group=group).replace('/', '\/'),
            suffix='</Location>'.replace('/', '\/'), file=self.conf
        )
        # print specific svn/repos's contents
        repo_print = "sed -n '/^\s*{prefix}/,/^\s*{suffix}/p' {file}".format(
            prefix='<Location /svn/{group}>'.format(group=group).replace('/', '\/'),
            suffix='</Location>'.replace('/', '\/'), file=self.conf
        )
        # TODO 删除连续空行

        stdout, stderr = self.ssh.execute(repos_delete)
        if stdout:
            print('repo configuration already exist!')
            # self.ssh.close()
            # return
        else:
            with open('resources/templates/subversion_repo.conf', 'r', encoding='utf-8') as file:
                conf_content = file.read().format(
                    workspace=self.workspace, group=group, ldap_url=config.ldap.url,
                    ldap_search_filter='ou=user,ou=workspace,dc=gsafety,dc=com?uid?sub?(objectClass=aqua-user)'
                )
                self.ssh.execute("echo '{content}' >> {file}".format(content=conf_content, file=self.conf))

        # ==================================================
        # Regenerate Authz
        # ==================================================
        self.ssh.execute('rm -f {workspace}/{group}/authz'.format(workspace=self.workspace, group=group))

        authz_config = ConfigParser()
        for section in ['groups', '/tags', '/trunk', '/branches'] + [
            '{project}:/tags', '{project}:/trunk', '{project}:/branches',
        ]:
            authz_config.add_section(section.format(project=project))

        authz_config.set('groups', 'qa', ','.join(['weichunhua', 'wangweiwei', 'wanfang']))

        authz_config.set('groups', '{project}.developer'.format(project=project), ','.join(members))

        for folder in ['tags', 'trunk', 'branches']:
            authz_config.set(
                '{project}:/{folder}'.format(project=project, folder=folder),
                '@qa',
                'rw'
            )
            authz_config.set(
                '{project}:/{folder}'.format(project=project, folder=folder),
                '@{project}.developer'.format(project=project),
                'rw'
            )

        authz = StringIO()
        authz_config.write(authz)

        self.ssh.execute("echo '{content}' >> {workspace}/{group}/authz".format(
            content=authz.getvalue(), workspace=self.workspace, group=group
        ))








        # self.ssh.execute('echo ')


        # stdout, stderr = self.ssh.execute(
        #     "sed -n '/^\s*{prefix}/,/^\s*{suffix}/p' {file}".format(
        #         prefix='<Location /svn/{group}>'.format(group=group).replace('/', '\/'),
        #         suffix='</Location>'.replace('/', '\/'), file=self.conf
        #     )
        # )



        self.ssh.close()




    def create2(self, owner, project_number, project_name, template, members=[]):
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
            doc=project_name
        )
        create_command.append(comm2)

        command3 = 'subversion mkdir file://{svn_home}/{project_number}/{doc}/{init}  -m "initial directories"'
        comm3 = command3.format(
            doc=project_name,
            svn_home=self.svn_home,
            project_number=project_number,
            init=self.template[template] if self.template.__contains__(template) else "{tags,trunk,branches}"
            # init="{tags,trunk,branches}"
        )
        create_command.append(comm3)

        repo_conf = """
<Location /subversion/{project_number}>
  DAV subversion
  SVNParentPath {svn_home}/{project_number}
  SVNListParentPath On

  AuthType Basic
  AuthName "Repositories of {project_number}"
  AuthzSVNAccessFile {svn_home}/{project_number}/{project_name}/authz

  Satisfy all
  Require valid-user

  AuthBasicProvider ldap

  AuthLDAPURL "ldap://172.17.38.163:10389/ou=user,ou=workspace,dc=gsafety,dc=com?uid?sub?(objectClass=aqua-user)"
</Location>
    """
        repo_conf = repo_conf.format(
            project_number=project_number,
            svn_home=self.svn_home,
            project_name=project_name
        )
        command4 = "echo '{repo_conf}' >>/etc/httpd/conf.d/subversion.conf"
        comm4 = command4.format(
            repo_conf=repo_conf,
        )
        create_command.append(comm4)

        repo_groups = '[groups]'
        for r in members.keys():
            repo_groups = repo_groups + """
""" + r + "="
            r_members = ','.join(members[r])
            repo_groups = repo_groups + r_members
        repo_field = "[" + project_name + ":/]"
        for ff in members.keys():
            repo_field = repo_field + """
@""" + ff + " = rw"

        repo_authz = """{groups}

{field}"""
        repo_auth = repo_authz.format(
            groups=repo_groups,
            field=repo_field
        )
        command5 = 'echo "{repo_authz}" >>{svn_home}/{project_number}/{project_name}/authz'
        comm5 = command5.format(
            project_number=project_number,
            svn_home=self.svn_home,
            repo_authz=repo_auth,
            project_name=project_name
        )
        create_command.append(comm5)

        comm6 = "systemctl restart httpd.service"
        create_command.append(comm6)
        try:
            for c in create_command:
                self.ssh.exec_command(c)
        except Exception as e:
            pass
        return self.url + '/' + project_number + '/' + project_name
        # self.add_authz(project_name, project_number, members)

    def add_authz(self, project_name, project_number, new_members):
        # add ldap

        if self.auth_ldap(project_number, project_name):
            repo_groups = '[groups]'
            for r in new_members.keys():
                repo_groups = repo_groups + """
""" + r + "="
                members = ','.join(new_members[r])
                repo_groups = repo_groups + members
            repo_field = "[" + project_name + ":/]"
            for ff in new_members.keys():
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
            command5 = 'echo "{repo_authz}" >{svn_home}/{project_number}/{project_name}/authz'
            comm5 = command5.format(
                project_number=project_number,
                svn_home=self.svn_home,
                repo_authz=repo_auth,
                project_name=project_name
            )
            create_command.append(comm5)

            comm6 = "systemctl restart httpd.service"
            create_command.append(comm6)
            for c in create_command:
                try:
                    self.ssh.exec_command(c)
                except Exception as e:
                    pass
            return self.url + '/' + project_number + '/' + project_name
        else:
            print("ladp message is not same with conf message")
            return "ladp message is not same with conf message"


    def get_auth(self, project_number, project_name):
        c = 'cat {svn_home}/{project_number}/{project_name}/authz'
        c = c.format(
            svn_home=self.svn_home,
            project_number=project_number,
            project_name=project_name
        )
        stdin, stdout, stderr = self.ssh.exec_command(c)

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
            # config = ConfigParser()
            config.read('tmp/1.ini', 'utf-8')
            roles = config.options('groups')
            value = {}
            for r in roles:
                members = config.get('groups', r)
                members = members.split(',')
                value[r] = members
            print(value)
            return value

    def auth_ldap(self, project_number, project_name):
        if self.get_auth(project_number=project_number,
                         project_name=project_name) == get_members(project_number, project_name):
            return True
        else:
            return False
