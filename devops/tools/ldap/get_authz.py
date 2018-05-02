# encoding=utf-8
import ldap3

from devops.tools.ldap import LDAP

from snippets.sample_config import config

base_ldap1 = 'ou=workgroup,ou=group,ou=workspace,dc=gsafety,dc=com'
base_ldap = 'ou=lpftest,ou=department,ou=group,dc=gsafety,dc=com'

cn_dist = {
    'owner': '负责人',
    'developer': '开发'
}


def get_members(project_number='__GCJC2013029', project_name='doc'):
    ldap = LDAP(url=config.ldap.url, username=config.ldap.username, password=config.ldap.password)
    ldap.bind()
    base = 'group={project_name},group={project_number},{base}'
    base = base.format(
        project_number=project_number,
        project_name=project_name,
        base=base_ldap
    )
    collection = ldap.search(
        base=base,
        filter='(&(objectClass=aqua-role))'
    )
    field = {}
    for collect in collection:
        print(collect)
        r = collect['attr']['role'][0]
        field[r] = []
        for m in collect['attr']['member']:
            field[r].append(m.split(',')[0][4:])
    return field


# print(get_members())


def add_project(project_number, project_name, members):
    display_name = project_number
    ldap = LDAP(url=config.ldap.url, username=config.ldap.username, password=config.ldap.password)
    ldap.bind()

    dn = "group={project_number},{base}".format(
        project_number=project_number,
        base=base_ldap
    )
    attributes = {
        'cn': display_name,
        'ou': display_name,
        'fullname': display_name,
        'fullpath': project_number,
        'group': project_number
    }
    if not ldap.exist(dn):
        ldap.add(dn=dn, object_class=['top', 'aqua-object', 'aqua-group', 'organizationalUnit'], attributes=attributes)
    else:
        print(project_number + ' is already existed')

    s_dn = "group={project_name},{base}".format(
        project_name=project_name,
        base=dn
    )
    s_attributes = {
        'cn': project_name,
        'ou': project_name,
        'fullname': project_name + '/' + project_name,
        'fullpath': project_number + '/' + project_name,
        'group': project_name
    }
    if not ldap.exist(s_dn):
        ldap.add(dn=s_dn, object_class=['top', 'aqua-object', 'aqua-group', 'organizationalUnit'],
                 attributes=s_attributes)
    else:
        print(project_name + ' is already existed')
    for r in members.keys():
        role = "role={role},{base}".format(
            role=r,
            base=s_dn
        )
        r_members = []
        for m in members[r]:
            m = 'uid={name},ou=staff,ou=user,ou=workspace,dc=gsafety,dc=com'.format(name=m)
            r_members.append(m)
        r_attributes = {
            'cn': cn_dist[r],
            'role': r,
            'fullname': project_number + '/' + project_name + '/' + r,
            'fullpath': project_number + '/' + project_name + '/' + r,
            'member': r_members,
        }
        if not ldap.exist(role):
            ldap.add(dn=role, object_class=['top', 'aqua-object', 'groupOfNames', 'aqua-role'],
                     attributes=r_attributes)
        else:
            changes = {
                'member': [
                    (ldap3.MODIFY_REPLACE, r_members),
                ]
            }
            print('modify')
            ldap.modify(dn=role, changes=changes)

def modify_project(project_number, project_name, members):
    ldap = LDAP(url=config.ldap.url, username=config.ldap.username, password=config.ldap.password)
    ldap.bind()

    dn = "group={project_number},{base}".format(
        project_number=project_number,
        base=base_ldap
    )
    s_dn = "group={project_name},{base}".format(
        project_name=project_name,
        base=dn
    )

    for r in members.keys():
        role = "role={role},{base}".format(
            role=r,
            base=s_dn
        )
        r_members = []
        for m in members[r]:
            m = 'uid={name},ou=staff,ou=user,ou=workspace,dc=gsafety,dc=com'.format(name=m)
            r_members.append(m)
        r_attributes = {
            'cn': cn_dist[r],
            'role': r,
            'fullname': project_number + '/' + project_name + '/' + r,
            'fullpath': project_number + '/' + project_name + '/' + r,
            'member': r_members,
        }
        if not ldap.exist(role):
            ldap.add(dn=role, object_class=['top', 'aqua-object', 'groupOfNames', 'aqua-role'],
                     attributes=r_attributes)
        else:
            changes = {
                'member': [
                    (ldap3.MODIFY_REPLACE, r_members),
                ]
            }
            print('modify')
            ldap.modify(dn=role, changes=changes)
