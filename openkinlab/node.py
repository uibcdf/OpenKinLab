from .edge import Edge

class Node():


    def __init__(self, microstate=None, weight=0, probability=None):

        self.index=None
        self.microstate=None
        self.edge={}
        self.n_edges=0
        self.weight=0
        self.cluster=0
        self.component=0
        self.coordinates=None
        self.color=None
        self.size=None

        self.microstate=microstate
        self.weight=weight
        if probability is not None:
            self.probability=probability

    def add_edge(self, edge):

        if edge.end.index in self.edge:

            raise ValueError("The edge is already included in this network.")

        self.edge[edge.end.index]=edge
        self.weight+=edge.weight
        self.n_edges+=1

    #def most_weighted_links(self,length=1):

    #    aux_bak=[[self.link[x],x] for x in self.link.keys()]
    #    aux_bak.sort(reverse=True)
    #    most_w_destin=[]
    #    for ii in range(length):
    #        most_w_destin.append(aux_bak[ii][1])
    #    return most_w_destin

