# -*- coding: utf-8 -*-
import networkx as nx
import os

class GraphTree:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodeTree = {}

    def add(self, node, label=None, **attr):
        if label is None: label = len(self.nodeTree)
        self.nodeTree[label] = node
        self.graph.add_node(label, **attr)
        return node

    def write(self, target):
        # if os.path.exists(target): os.remove(target)
        nx.write_gml(self.graph, target)