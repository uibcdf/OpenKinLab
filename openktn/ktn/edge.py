class Edge():

    def __init__(self, origin, end, weight=0.0, probability=0.0):

        self.index = None
        self.origin = None
        self.end = None
        self.weight = 0.0
        self.probability = 0.0
        self.symmetrized = False

        self.origin=origin
        self.end=end
        self.weight=weight
        if probability is not None:
            self.probability=probability

    def is_intra_basin():
        raise NotImplementedError

    def is_inter_basins():
        raise NotImplementedError
