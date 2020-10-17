import numpy as np
from .node import Node
from .edge import Edge
from .microstate import Microstate

class Network():

    def __init__(self, n_nodes=0, microstate_names=None):

        self.n_nodes=0
        self.n_edges=0
        self.n_clusters=0
        self.n_components=0

        self.node=[]
        self.edge=[]
        self.microstate={}
        self.cluster=[]
        self.component=[]

        self.weight=0

        self.is_symmetric=False


        if n_nodes>0:

            for _ in range(n_nodes):
                self.add_node()

        elif microstate_names is not None:

            if type(microstate_names)==dict:
                n_nodes=len(microstate_names)
                for _ in range(n_nodes):
                    self.add_node()
                for name, node_index in microstate_names.items():
                    self.add_microstate(name, node_index=node_index)
            else:
                for name in microstate_names:
                    self.add_microstate(name)

    def info(self):

        print('# OpenKinLab network:')
        nodes_suffix=' with no microstates'
        if len(self.microstate):
            nodes_suffix=' with microstates'
        print('{} nodes'.format(self.n_nodes)+nodes_suffix)
        print('{} edges'.format(self.n_edges))
        print('{} weight'.format(self.weight))

    def add_node(self, microstate_name=None, id=None, weight=0, probability=None):

        tmp_microstate = None
        if microstate_name is not None:
            if microstate_name in self.microstate:
                raise ValueError("The microstate is already included in this network.")
            tmp_microstate = Microstate(microstate_name)
            self.microstate[microstate_name] = tmp_microstate


        tmp_node = Node(weight=weight, probability=probability)
        tmp_node.index = len(self.node)
        self.node.append(tmp_node)
        self.weight=weight
        self.n_nodes+=1

        if microstate_name is not None:
            tmp_microstate.node = tmp_node
            tmp_node.microstate = tmp_microstate

    def add_edge(self, origin=None, end=None, weight=0, probability=None, with_microstates=False):

        if with_microstates:
            origin = self.microstates[origin].node
            end = self.microstates[end].node
        else:
            origin=self.node[origin]
            end=self.node[end]

        tmp_edge = Edge(origin, end, weight=weight, probability=probability)
        tmp_edge.index = len(self.edge)
        self.node[origin.index].add_edge(tmp_edge)
        self.weight+=weight
        self.n_edges+=1

    def add_microstate(self, name, node_index=None):

        if node_index is None:

            self.add_node(microstate_name=name)

        else:
            tmp_node = self.node[node_index]
            tmp_microstate = Microstate(name, node=self.node[node_index])
            for edge in tmp_node.edge.values():
                tmp_microstate.add_edge(edge)

            self.microstate[name]=tmp_microstate

    def add_transition(self, origin=None, end=None, weight=1, with_microstates=False):

        if with_microstates:
            origin = self.microstates[origin].node.index
            end = self.microstates[end].node.index

        if end not in self.node[origin].edge:
            self.add_edge(origin=origin, end=end, weight=weight)
        else:
            self.node[origin].edge[end].weight+=weight
            self.node[origin].weight+=weight
            self.weight+=weight

    def __call__(self):

        return self.info()

