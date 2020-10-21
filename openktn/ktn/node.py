from .edge import Edge

class Node():

    def __init__(self, microstate=None, weight=0.0, probability=0.0):

        self.index=None
        self.microstate=None
        self.edge={}
        self.n_edges=0
        self.weight=0.0
        self.probability=0.0
        self.basin=None
        self.component=None
        self.coordinates=None
        self.color=None
        self.size=None

        self.microstate=microstate
        self.weight=weight
        self.probability=probability

    def add_edge(self, edge):

        if edge.end.index in self.edge:

            raise ValueError("The edge is already included in this network.")

        self.edge[edge.end.index]=edge
        self.weight+=edge.weight
        self.n_edges+=1

    #def most_likely_edges(self,length=1):

    #    aux_bak=[[self.link[x],x] for x in self.link.keys()]
    #    aux_bak.sort(reverse=True)
    #    most_w_destin=[]
    #    for ii in range(length):
    #        most_w_destin.append(aux_bak[ii][1])
    #    return most_w_destin

