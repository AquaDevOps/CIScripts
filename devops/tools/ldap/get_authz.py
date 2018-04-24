# encoding=utf-8

from devops.tools.ldap import LDAP

from snippets.sample_config import config


def get_members(project_number='__GCJC2013029', display_name='src'):
    ldap = LDAP(url=config.ldap.url, username=config.ldap.username, password=config.ldap.password)
    ldap.bind()
    base = 'group={display_name},group={project_number},ou=workgroup,ou=group,ou=workspace,dc=gsafety,dc=com'
    base = base.format(
        project_number=project_number,
        display_name=display_name
    )
    collection = ldap.search(
        base=base,
        filter='(&(objectClass=aqua-role))'
    )
    field = {}
    for collect in collection:
        r = collect['attr']['role'][0]
        field[r]=[]
        for m in collect['attr']['member']:
            field[r].append(m.split(',')[0][4:])
    return field



# print(get_members())
