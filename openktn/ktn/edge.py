class Edge():

    def __init__(self, origin, end, weight=0, probability=None):

        self.index = None
        self.origin = None
        self.end = None
        self.weight = 0
        self.probability = None
        self.symmetrized = False
        self.intra_cluster= False
        self.inter_clusters= False

        self.origin=origin
        self.end=end
        self.weight=weight
        if probability is not None:
            self.probability=probability

