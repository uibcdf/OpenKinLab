import numpy as np

class TArrays():

    def __init__(self, network):

        n_nodes = network.n_nodes
        n_edges = network.n_edges

        self.T_ind=np.empty(n_edges, dtype=int)
        self.T_start=np.empty(n_nodes+1, dtype=int)
        self.T_wl=np.empty(n_edges, dtype=float)
        self.T_wn=np.empty(n_nodes, dtype=float)

        kk=0

        for ii in range(n_nodes):
            node = network.node[ii]
            self.T_wn[ii] = node.weight
            self.T_start[ii]=kk
            for jj, edge in node.edge.items():
                self.T_ind[kk]=jj
                self.T_wl[kk]=edge.weight
                kk+=1

        self.T_start[n_nodes]=kk

