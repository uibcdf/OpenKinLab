class TransitionsList(list):

    def __init__(self):
        super().__init__()

    def append_transition(self, transition):

        transition.index=self.__len__()
        return self.append(transition)

    def remove_transition(self, index):

        transition = self.pop[index]

        for transition in self[index:]:
            transition.index-=1

class TransitionsDict(dict):

    def __init__(self):
        super().__init__()

        self.end_name_to_end_index={}

    def __call__(self, name):

        end_index=select.end_name_to_end_index[name]
        return self.__getitem__(end_index)

    def add_transition(self, transition):

        self.__setitem__(transition.end.index)=transition
        self.end_name_to_end_index[transition.end.name]=transition.end.index

    def pop_microstate(self, end_index=None, end_name=None):

        if end_name is not None:
            end_index = self.end_name_to_end_index[name]

        transition = self.pop[end_index]
        del self.end_name_to_end_index[transition.end_name]

        return transition

class Transition():

    def __init__(self, origin, end, weight=0.0):

        self.index = None
        self.origin = None
        self.end = None
        self.weight = 0.0
        self.probability = 0.0
        self.symmetrized = False

        self.origin=origin
        self.end=end
        self.weight=weight

    def is_intra_basin():
        raise NotImplementedError

    def is_inter_basins():
        raise NotImplementedError

