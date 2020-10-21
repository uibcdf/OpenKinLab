import numpy as np

class TArrays():

    def __init__(self, network):

        n_nodes = network.n_nodes
        n_edges = network.n_edges

        self.ind=np.empty(n_edges, dtype=int)
        self.start=np.empty(n_nodes+1, dtype=int)
        self.pl=np.empty(n_edges, dtype=float)
        self.pn=np.empty(n_nodes, dtype=float)

        kk=0

        for ii in range(n_nodes):
            node = network.node[ii]
            self.pn[ii] = node.probability
            self.start[ii]=kk
            for jj, edge in node.edge.items():
                self.ind[kk]=jj+1
                self.pl[kk]=edge.probability
                kk+=1

        self.start[n_nodes]=kk

