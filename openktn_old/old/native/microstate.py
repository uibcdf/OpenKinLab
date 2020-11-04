from .transition import Transition, TransitionDict

class MicrostatesList(list):

    def __init__(self):
        super().__init__()

        self.name_to_index={}

    def __call__(self, name):

        index=self.name_to_index[name]
        return self.__getitem__[index]

    def append_microstate(self, microstate):

        index=self.__len__()
        if microstate.name in self.name_to_index:
            raise ValueError("The microstate was already in this KTN. It can not be re-added.")
        else:
            microstate.index=index
            self.name_to_index[microstate.name]=index
            return self.append(microstate)

    def remove_microstate(self, index=None, name=None):

        if name is not None:
            index = self.name_to_index[name]

        microstate = self.pop[index]
        del self.name_to_index[microstate.name]

        for microstate in self[index:]:
            microstate.index-=1

class Microstate():


    def __init__(self, name):

        self.name=None
        self.index=None

        self.weight=0.0
        self.probability=0.0

        self.transition=TransitionsDict()
        self.n_transitions=0

        self.basin=None
        self.component=None

        self.coordinates=None
        self.color=None
        self.size=None
        self.frames=[]

    def add_transition(self, transition):

        if transition.end.index in self.transition:
            raise ValueError("The transition is already defined in this network.")

        self.transition.add_transition(transition)
        self.weight+=transition.weight
        self.n_transitions+=1

    def most_likely_transition(self):

        output=None
        probability=0.0

        for transition in self.transition.values():
            if transition.probability > probability:
                probability=transition.probability
                output=transition

        return transition

