import ldap
from ldap import modlist


class LDAP:
    def __init__(self, url, username, password):
        self.session = ldap.initialize(url)
        self.session.set_option(ldap.OPT_REFERRALS, 0)
        self.session.protocol_version = ldap.VERSION3
        self.session.simple_bind_s(username.encode('utf-8'), password.encode('utf-8'))

        self.schemas = {}

    def add(self, dn, entry):
        return self.session.add_s(dn, ldap.modlist.addModlist(entry))

    def drop(self):
        self.session.unbind_s()

    def modify(self, basedn, oldvalue, newvalue):
        self.session.modify_s(basedn, modlist.modifyModlist(oldvalue, newvalue))

    def rename(self, dn, newrdn, newsuperior=None, delold=True):
        self.session.rename(dn=dn, newrdn=newrdn, newsuperior=newsuperior, delold=delold)

    def search(self, scope=ldap.SCOPE_SUBTREE, basedn='dc=gsafety,dc=com', filter='(&(objectClass=*))', attrlist=[]):
        try:
            return self.session.search_s(basedn, scope, filterstr=filter, attrlist=attrlist)
        except ldap.NO_SUCH_OBJECT:
            return []

    def exist(self, dn):
        return len(self.session.search(scope=ldap.SCOPE_BASE, basedn=dn)) > 0


    def product(self, collect):
        for node in collect:
            self.add(node['dn'], node['obj'])
            self.product(node['children'])

    def collect(self, basedn):
        nodes = [
            {
                'dn': dn,
                'obj': obj,
                'children': self.collect(basedn=dn)
            } for dn, obj in self.search(scope=ldap.SCOPE_ONELEVEL, basedn=basedn)
        ]

        for node in nodes:
            cls = '/'.join(node['obj']['objectClass'])
            self.schemas[cls] = list(set(self.schemas.get(cls, []) + node['obj'].keys()))

        return nodes

    def walk(self, collection):
        for node in collection:
            for dn, obj in self.walk(node['children']):
                yield(dn, obj)
            yield(node['dn'], node['obj'])

    def migrate(self, collection, basedn='', dn_mapping={}, cls_mapping={}, attr_mapping={}):
        migrated_collection = []
        for node in collection:
            connected_class = '/'.join(set(node['obj']['objectClass']))
            migrated_dn = dn_mapping.get(connected_class, lambda node, parent: node['dn'])(node, '')

            migrated_node = {
                'dn': '{dn},{basedn}'.format(dn=migrated_dn, basedn=basedn),
                'obj': dict(
                    {
                        'objectClass': cls_mapping.get(connected_class, node['obj']['objectClass'])
                    },
                    **{
                        # attr: value for attr, value in node['obj'].iteritems() if attr is not 'objectClass'
                        attr: operator(node, '') for attr, operator in attr_mapping[connected_class].iteritems()
                    }),
                'children': self.migrate(
                    node['children'],
                    basedn='{dn},{basedn}'.format(dn=migrated_dn, basedn=basedn),
                    dn_mapping=dn_mapping,
                    cls_mapping=cls_mapping,
                    attr_mapping=attr_mapping,
                )
            }
            migrated_collection.append(migrated_node)
        return migrated_collection

    def refactor2(self, nodes, basedn='', dn_naming={}, dn_mapping={}, cls_mapping={}, attr_mapping={}):
        dn_naming = {'/'.join(set(dn.split('/'))): mapping for dn, mapping in dn_naming.iteritems()}
        cls_mapping = {'/'.join(set(cls.split('/'))): mapping for cls, mapping in cls_mapping.iteritems()}
        migrated = []
        for node in nodes:
            dn = '/'.join(set(node['obj']['objectClass']))
            if dn in dn_naming:
                node['dn'] = '{dn}={val},{basedn}'.format(
                    dn=dn_naming[dn][0],
                    val=dn_mapping.get(dn, {}).get(
                        node['obj'][dn_naming[dn][1]][0].decode('utf-8'),
                        node['obj'][dn_naming[dn][1]][0]
                    ),
                    basedn=basedn,
                )

            for attr in node['obj'].keys():
                if attr in attr_mapping:
                    for mapping in attr_mapping[attr]:
                        node['obj'][mapping] = node['obj'][attr]
                    node['obj'].pop(attr)

            node['obj']['objectClass'] = cls_mapping.get(
                '/'.join(set(node['obj']['objectClass'])),
                node['obj']['objectClass']
            )
            node['children'] = self.refactor(
                nodes=node['children'],
                basedn=node['dn'],
                dn_naming=dn_naming,
                dn_mapping=dn_mapping,
                cls_mapping=cls_mapping,
                attr_mapping=attr_mapping,
            )

            migrated.append(node)
        return migrated

