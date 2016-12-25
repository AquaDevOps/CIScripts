# -*- coding: utf-8 -*-
import os, re, sys
import xml.etree.ElementTree as Tree
from collections import OrderedDict
sys.path.append(os.path.dirname(__file__))
import FileUtils

class Pom:
    namespace = ''

    def __init__(self, artifactId, groupId = None, version = None):
        self.artifactId = artifactId
        self.groupId = groupId
        self.version = version
        self.modules = []
        self.parent = None
        self.dependencies = []

    def __repr__(self):
        return self.to_str()

    def to_str(self):
        if self.version is None:
            return '%s:%s' % (self.groupId, self.artifactId)
        else:
            return '%s:%s:%s' % (self.groupId, self.artifactId, self.version)

    def to_xml(self):
        return '''
        <dependency>
            <groupId>%s</groupId>
            <artifactId>%s</artifactId>
        </dependency>
''' % (self.groupId, self.artifactId) if self.version is None else '''
        <dependency>
            <groupId>%s</groupId>
            <artifactId>%s</artifactId>
            <version>%s</version>
        </dependency>
''' % (self.groupId, self.artifactId, self.version)

    def to_dict(self):
        o_dict = OrderedDict()
        o_dict['groupId'] = self.groupId
        o_dict['artifactId'] = self.artifactId
        if self.version is not None: o_dict['version'] = self.version
        o_dict['path'] = self.path
        return o_dict

    # 解析并附加namespace
    @staticmethod
    def ns(tag):
        return '%s%s' % (Pom.namespace, tag)

    @staticmethod
    def from_str(string):
        parts = string.split(':')
        return Pom(
            artifactId=parts[1],
            groupId=parts[0],
            version=parts[2] if 3 == len(parts) else None
            )

    @staticmethod
    def from_pom(path):
        root = Tree.parse(path[0]).getroot()
        if '' == Pom.namespace:
            match = re.match('\{.*\}', root.tag)
            Pom.namespace = match.group(0) if match is not None else ''

        pom = Pom(root.find(Pom.ns('artifactId')).text)
        pom.dir = path[4]
        pom.path = path[0]
        pom.subpath = path[1]
        if root.find(Pom.ns('version')) is not None:
            pom.version = root.find(Pom.ns('version')).text

        # modules = root.find(Pom.ns('modules'))
        # if modules is not None:
        #     for module in modules
        # 采集parent信息
        parent = root.find(Pom.ns('parent'))
        if parent is not None:
            pom.parent = Pom(parent.find(Pom.ns('artifactId')).text)
            pom.groupId = pom.parent.groupId = parent.find(Pom.ns('groupId')).text
        # else:
            # pom.groupId = root.find(Pom.ns('groupId')).text
            
        groupId = root.find(Pom.ns('groupId'))
        if groupId is not None:
            pom.groupId = groupId.text

        # 采集依赖信息
        dependencies = root.find(Pom.ns('dependencies'))
        if dependencies is not None: 
            for dependency in dependencies: 
                pom.dependencies.append(Pom(
                    dependency.find(Pom.ns('artifactId')).text,
                    dependency.find(Pom.ns('groupId')).text,
                    # dependency.find(Pom.ns('version')).text,
                    ))
        return pom

class PomTree:
    def __init__(self):
        self.tree = {}

    def store(self, pom):
        self.tree[pom.groupId] = self.tree.get(pom.groupId, {})
        self.tree[pom.groupId][pom.artifactId] = pom
        return pom

    def fetch(self, pom=None, groupId=None, artifactId=None, log=False):
        if pom is not None:
            groupId, artifactId = pom.groupId, pom.artifactId
        if groupId in self.tree and artifactId in self.tree[groupId]:
            return self.tree[groupId][artifactId]
        else:
            if log: print('skipped %s:%s' % (groupId, artifactId))
            return None