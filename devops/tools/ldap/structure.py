import ldap3
from snippets.sample_config import config
from ldap3.utils.dn import safe_rdn
from ldap3.utils.log import set_library_log_activation_level
from ldap3.abstract.entry import Entry
import re
import logging
logging.basicConfig(filename='ldap_client.log', level=logging.DEBUG)
set_library_log_activation_level(logging.DEBUG)


class LDAP:
    REGEX_RDN = re.compile('(?P<attr>\S+)=(?P<val>\S+)')
    (BASE, LEVEL, SUBTREE) = (ldap3.BASE, ldap3.LEVEL, ldap3.SUBTREE)
    (MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE) = (ldap3.MODIFY_ADD, ldap3.MODIFY_DELETE, ldap3.MODIFY_REPLACE)

    def __init__(self, url=config.ldap.url, username=config.ldap.username, password=config.ldap.password):
        self.connection = ldap3.Connection(server=url, user=username, password=password)
        self.schemas = {}

    def bind(self):
        self.connection.bind()

    def unbind(self):
        self.connection.unbind()

    def add(self, dn, object_class, attributes={}):
        attributes = {
            key: value for key, value in attributes.items() if (
                key != 'objectClass' and (not isinstance(value, (set, list, tuple)) or len(value) > 0)
            )
        }
        result = self.connection.add(dn=dn, object_class=object_class, attributes=attributes)

    def delete(self, dn):
        return self.connection.delete(dn)

    # changes = {
    #   attr: [
    #     (MODIFY_ADD / MODIFY_DELETE / MODIFY_REPLACE, [contents]),
    #   ]
    # }
    def modify(self, dn, changes={}):
        self.connection.modify(dn, changes=changes)

    def modify_dn(self, dn, relatvie_dn=None, delete_old_dn=True, new_superior=None):
        if relatvie_dn is None:
            relatvie_dn = safe_rdn(dn)
        self.connection.modify_dn(dn, relative_dn=relatvie_dn, delete_old_dn=delete_old_dn, new_superior=new_superior)

    def search(
        self, base='dc=gsafety,dc=com', scope=SUBTREE, filter='(&(objectClass=*))', attributes=['*'], flat=False
    ):
        self.connection.search(search_base=base, search_scope=scope, search_filter=filter, attributes=attributes)
        return [dict({'dn': entry.entry_dn}, **entry.entry_attributes_as_dict) if flat else {
            'dn': entry.entry_dn, 'attr': entry.entry_attributes_as_dict
        } for entry in self.connection.entries]

    def exist(self, dn):
        return len(self.search(base=dn, scope=LDAP.BASE)) > 0

    def load(self, base_dn='dc=gsafety,dc=com', node=None):
        if node is None and self.exist(base_dn):
            node = self.search(base=base_dn, scope=LDAP.BASE)[0]
        if node is None:
            return None

        return dict(node, **{'children': [
            self.load(base_dn=child['dn'], node=child) for child in self.search(base=base_dn, scope=LDAP.LEVEL)
        ]})

    def collect(self, base, include_root=True, flat=False):
        collection = self.search(base=base, scope=LDAP.LEVEL, flat=flat)
        for node in collection:
            node['children'] = self.collect(node['dn'], include_root=False, flat=flat)
        return [
            dict(base, **{'collection': collection}) for base in self.search(base=base, scope=LDAP.BASE, flat=flat)
        ] if include_root else collection

    def product(self, collection):
        for node in collection:
            if not self.exist(node['dn']):
                self.add(node['dn'], object_class=node['obj']['objectClass'], attributes=node['obj'])
                self.product(node.get('children', []))
