# encoding=utf-8

from devops.tools.ldap import LDAP

from snippets.sample_config import config


def get_members(project_number='__GCJC2013029'):
    ldap = LDAP(url=config.ldap.url, username=config.ldap.username, password=config.ldap.password)
    ldap.bind()
    collection = ldap.search(
        base='ou=group,ou=workspace,dc=gsafety,dc=com',
        filter='(&(objectClass=aqua-role))'
    )
    result = []
    for collect in collection:
        if 'workgroup' in collect['dn'] and project_number in collect['dn']:
            data = {'field': '', 'role': '', 'members': []}
            # print(collect)
            data['field'] = collect['dn'].split(',')[1][6:]
            field = collect['dn'].split(',')[1][6:]
            data['role'] = []
            for r in collect['attr']['role']:
                data['role'].append(field + '_' + r)
            data['members'] = []
            for m in collect['attr']['member']:
                data['members'].append(m.split(',')[0][4:])
            result.append(data)
    # result = [{'field': 'src', 'role': ['src_developer'], 'members': ['libo', 'lipengfei']}]
#     for g in result:
#         repo_name = g['field']
#         repo_group_list = g['role']
#         repo_groups = '[groups]'
#         for r in g['role']:
#             repo_groups = repo_groups + """
# """ + r + "="
#             for m in g['members']:
#                 repo_groups = repo_groups + m + ","
#         repo_field = "[" + repo_name + ":/]"
#         for ff in repo_group_list:
#             repo_field = repo_field + """
# @""" + ff + " = rw"
#         repo_authz = """{groups}
#
# {field}"""
#         repo_auth = repo_authz.format(
#             groups=repo_groups,
#             field=repo_field
#         )
#         print(repo_auth)
    return result


# print(get_members())
