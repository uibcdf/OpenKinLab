import numpy as np
from .microstate import MicrostatesList, Microstate
from .transition import TransitionsList, Transition
from .basin import BasinsList, Basin
from .component import ComponentsList, Component
from .t_arrays import TArrays
import simtk.unit as unit

class KTN():

    def __init__(self, n_microstates=0, microstate_names=None, time_step=None, temperature=None):

        self.n_microstates=0
        self.n_transitions=0
        self.n_basins=0
        self.n_components=0
        self.time_step=None
        self.temperature=None

        self.microstate=MicrostatesList()
        self.edge=TransitionsList()
        self.basin=BasinsList()
        self.component=ComponentsList()

        self.weight=0

        self.symmetrized=False
        self.Ts = None

        if n_microstates>0:

            for ii in range(n_microstates):
                self.add_microstate(ii)

        elif microstate_names is not None:

            for name in microstate_names:
                self.add_microstate(name)

        if time_step is not None:
            self.time_step = time_step.in_units_of(unit.nanoseconds)

        if temperature is not None:
            self.temperature = temperature.in_units_of(unit.kelvin)

    def update_weights(self):

        self.weight = 0.0
        for microstate in self.microstate:
            microstate.weight = 0.0
        for transition in self.transition:
            transition.origin.weight += transition.weight
            self.weight += transition.weight

    def update_probabilities(self):

        self.update_weights()
        if self.weight>0.0:
            for microstate in self.microstate:
                microstate.probability=microstate.weight/self.weight
            for transition in self.transition:
                edge.probability=transition.weight/transition.origin.weight

        self._update_Ts()

    def _update_Ts(self):

        self.Ts = TArrays(self)

    def info(self):

        print('# Kinetic Transition Network:')
        print('{} microstates'.format(self.n_microstates))
        print('{} transitions'.format(self.n_transitions))
        print('{} weight'.format(self.weight))

    def add_microstate(self, name):

        microstate = Microstate(name)
        self.node.append_microstate(microstate)
        self.n_nodes+=1

    def remove_microstates(self, indices=None):

        raise NotImplementedError

    def add_transition(self, origin=None, end=None, weight=0.0, with_names=False):

        if with_names:
            origin = self.microstate(origin)
            end = self.microstate(end)
        else:
            if type(origin) is not Microstate:
                origin=self.node[origin]
            if type(end) is not Microstate:
                end=self.node[end]

        if end.index not in self.node[origin].edge:
            transition = Transition(origin, end, weight=weight)
            self.transition.append_transition(transition)
            self.node[origin.index].add_transition(transition)
            self.n_edges+=1
        else:
            self.node[origin].edge[end].weight+=weight
            self.node[origin].weight+=weight

        self.weight+=weight

    def remove_transitions(self, indices=None):

        raise NotImplementedError

    def add_component(self, microstate_indices=None):

        raise NotImplementedError
        #component_index=self.n_components
        #tmp_component=Component(nodes, component_index)
        #self.component.append(tmp_component)
        #self.n_components+=1

    def remove_components(self, indices=None):

        raise NotImplementedError

    def add_basin(self, microstate_indices=None):

        raise NotImplementedError

    def remove_basins(self, indices=None):

        raise NotImplementedError

    def symmetrize(self):

        for transition in self.transition:

            if not transition.symmetrized:

                if transition.origin.index not in transition.end.edge:
                    self.add_transition(origin=transition.end, end=transition.origin)

                transition_back = transition.end.edge[transition.origin.index]

                new_weight = 0.5*(transition.weight+transition_back.weight)
                transition.weight = new_weight
                transition_back.weight = new_weight
                transition.symmetrized = True
                transition_back.symmetrized = True

        self.symmetrized = True
        self.update_probabilities()

    def select():

        raise NotImplementedError

    def copy(self):

        from copy import deepcopy
        ktn=deepcopy(self)
        return ktn

    def extract(self, microstate_indices='all', selection=None):

        if selection is not None:
            microstate_indices = self.selection(target='microstate', selection=selection, output='indices')

        ktn = KTN()

        aux_dict = {}

        for ii in range(len(microstate_indices)):
            index = microstate_indices[ii]
            aux_dict[index] = ii
            ktn.add_microstate(self.microstate[index].name)

        ktn.symmetrized = self.symmetrized
        for origin_index in microstate_indices:
            microstate=self.microstate[origin_index]
            for end_index in microstate.transition:
                if end_index in microstate_indices:
                    ktn.add_transition(origin=aux_dict[origin_index], end=aux_dict[end_index], weight=weight)

        ktn.update_probabilities()

        return ktn

    def merge(self, ktn):

        aux = np.empty(ktn.n_microstates, dtype=int)

        for outside_microstate in ktn.microstate:

            if outside_microstate.name in self.microstate.name_to_index:

                inside_microstate = self.microstate(outside_microstate.name)
                aux[outside_microstate.index]=inside_microstate.index

            else:

                aux[outside_microstate.index]=self.n_microstate
                self.add_node(outside_microstate.name)

        for transition in ktn.transition:

                self.add_transition(origin=aux[transition.origin.index], end=aux[transition.end.index], weight=transition.weight)

    def to_dataframes():

        raise NotImplementedError

    def to_networkx():

        raise NotImplementedError

    #def get_most_likely(self, target='node', indices='all', selection=None, output='node', top=1):
    #    raise NotImplementedError

    #def select(self):
    #    raise NotImplementedError

    def __call__(self):

        return self.info()

