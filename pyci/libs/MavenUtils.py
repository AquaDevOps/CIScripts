# -*- coding: utf-8 -*-
import os, sys, getopt
sys.path.append(os.path.dirname(__file__))

from GraphUtils import GraphTree
from MavenStructs import Pom, PomTree
from MavenCommands import *

def support(pom, pomtree, sequence=[]):
    if pom is None:
        return
    elif pomtree.fetch(pom) is not None:
        return
    support(pom.parent, pomtree, sequence)
    for dependency in pom.dependencies: support(dependency, pomtree, sequence)
    
    sequence.append(pomtree.store(pom))
    return sequence

def sequence(poms, target, log=False):
    pomtree_src, pomtree_dst = PomTree(), PomTree()
    for pom in poms:
        pomtree_src.store(pom)

    for pom in poms:
        pom.dependencies = [pomtree_src.fetch(dep, log=log) for dep in pom.dependencies]
        pom.dependencies = [dep for dep in pom.dependencies if dep is not None]
        if pom.parent is not None: pom.parent = pomtree_src.fetch(pom.parent, log=log)

    if not isinstance(target, Pom): target = Pom.from_str(target)
    return support(pomtree_src.fetch(target), pomtree_dst), poms

def tree(poms, target):
    pomtree = PomTree()
    for pom in poms:
        pomtree.store(pom)

    graph = GraphTree()

    for pom in poms:
        part = ''
        if pom.subpath.startswith('cloud-basic-components') : part = 'basic'
        if pom.subpath.startswith('cloud-business-components') : part = 'business'
        if pom.subpath.startswith('cloud-business-components/cloud-common-components') : part = 'common'
        if pom.subpath.startswith('cloud-business-components/cloud-framework-components') : part = 'framework'
        if pom.subpath.startswith('cloud-business-components/cloud-portal-components') : part = 'portal'

        if pom.subpath.startswith('cloud-business-components/common-business') : part = 'common'
        if pom.subpath.startswith('cloud-business-components/cloudframework-relate') : part = 'framework'
        if pom.subpath.startswith('cloud-business-components/cloudportal-relate') : part = 'portal'
        if pom.subpath.startswith('cloud-technical-components') : part = 'technical'
        graph.add(pom, pom.artifactId, part=part)

    for pom in poms:
        if pom.parent is not None:
            graph.graph.add_edge(pom.artifactId, pomtree.fetch(pom.parent).artifactId, color='red')

        # for dep in pom.dependencies:
        #     if pomtree.fetch(dep) is not None:
        #         graph.graph.add_edge(pom.artifactId, dep.artifactId, color='blue')

    graph.write(target)