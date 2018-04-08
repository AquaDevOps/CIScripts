import ssh
class svn:
    def __init__(self, svn_home='/home/workspace/repos', host='172.17.38.181', password='intel@123'):
        self.client = ssh.SSHClient()
        self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        self.client.connect(host, port=22, username='root', password=password)

        self.svn_home = svn_home
        self.svn_repo_name = 'doc'



    def create_svn(self, project_number, members=None):
        create_command = []
        command1 = 'mkdir {svn_home}/{project_number}'
        comm1 = command1.format(
            svn_home=self.svn_home,
            project_number=project_number
        )
        create_command.append(comm1)

        command2 = 'svnadmin create {svn_home}/{project_number}/doc'
        comm2 = command2.format(
            svn_home=self.svn_home,
            project_number=project_number
        )
        create_command.append(comm2)

        command3 = 'svn mkdir file://{svn_home}/{project_number}/doc/{init}  -m "initial directories"'
        comm3 = command3.format(
            svn_home=self.svn_home,
            project_number=project_number,
            init="{tags,trunk,branches}"
        )
        create_command.append(comm3)

        repo_conf = """
    <Location /svn/{project_number}>
      DAV svn
      SVNParentPath {svn_home}/{project_number}
      SVNListParentPath On

      AuthType Basic
      AuthName "Repositories of {project_number}"
      AuthzSVNAccessFile {svn_home}/{project_number}/authz

      Satisfy all
      Require valid-user

      AuthBasicProvider ldap

      AuthLDAPURL "ldap://172.17.38.163:10389/ou=user,ou=workspace,dc=gsafety,dc=com?uid?sub?(objectClass=aqua-user)"
    </Location>
    """
        repo_conf = repo_conf.format(
            project_number=project_number,
            svn_home=self.svn_home
        )
        command4 = "echo '{repo_conf}' >>/etc/httpd/conf.d/subversion.conf"
        comm4 = command4.format(
            repo_conf=repo_conf,
        )
        create_command.append(comm4)

        repo_authz = """[groups]
    qa = {user3}
    doc_developer = {user3}

    [/tags]
    @qa = rw

    [doc:/]
    * = r

    [doc:/trunk]
    @doc_developer = rw

    [doc:/branches]
    @doc_developer = rw"""
        users = ''
        for user in members:
            users = users + ',' + user
        repo_authz = repo_authz.format(
            user3=users
        )
        command5 = 'echo "{repo_authz}" >>{svn_home}/{project_number}/authz'
        comm5 = command5.format(
            project_number=project_number,
            svn_home=self.svn_home,
            repo_authz=repo_authz
        )
        create_command.append(comm5)

        comm6 = "systemctl restart httpd.service"
        create_command.append(comm6)
        try:
            for c in create_command:
                self.client.exec_command(c)
        except Exception as e:
            pass
