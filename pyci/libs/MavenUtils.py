# -*- coding: utf-8 -*-
import os, sys, getopt
sys.path.append(os.path.dirname(__file__))
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

def sequence(paths, target, log=False):
    poms = [Pom.from_pom(path) for path in paths]

    pomtree_src, pomtree_dst = PomTree(), PomTree()
    for pom in poms: pomtree_src.store(pom)
    for pom in poms:
        pom.dependencies = [pomtree_src.fetch(dep, log=log) for dep in pom.dependencies]
        pom.dependencies = [dep for dep in pom.dependencies if dep is not None]
        if pom.parent is not None: pom.parent = pomtree_src.fetch(pom.parent, log=log)

    if not isinstance(target, Pom): target = Pom.from_str(target)
    return support(pomtree_src.fetch(target), pomtree_dst)