from openktn.ktn import Node

class Basin():

    def __init__(self, nodes=None, index=None):

        self.n_nodes=0
        self.n_edges=0

        self.name=None
        self.index=index
        self.node=set()
        self.edge=set()
        self.weight=0.0
        self.probability=0.0

        self.symmetrized=False
        self.T_arrays=None

        if nodes is not None:
            self.add_nodes(nodes)

    def add_nodes(self, nodes):

        if type(nodes)==Node:
            nodes=[nodes]

        for node in nodes:
            node.basin=self
            self.node.add(node)
            self.weight+=node.weight
            self.probability+=node.probability

        for node in self.node:
            for edge in node.edge.values():
                if edge.end.basin==self:
                    self.edge.add(edge)

        self.n_nodes=len(self.node)
        self.n_edges=len(self.edge)


