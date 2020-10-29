import numpy as np
from simtk.unit import kelvin, nanoseconds

attributes = {'temperature':None, 'time_step':None, 'weight':0.0}

class KineticTransitionNetwork():


    def __init__(self, n_microstates=0, temperature=None, time_step=None):

        from openktn.native.microstate import MicrostatesDataFrame
        from openktn.native.transition import TransitionsDataFrame

        self.microstates_dataframe=MicrostatesDataFrame()
        self.transitions_dataframe=TransitionsDataFrame()

        self.temperature=temperature.in_units_of(kelvin)
        self.temperature._value = np.round(self.temperature._value,6)
        self.time_step=time_step.in_units_of(nanoseconds)
        self.time_step._value = np.round(self.time_step._value,6)

        self.weight=0.0

        for _ in range(n_microstates):
            self.add_microstate()

    def n_microstates(self):

        return self.microstates_dataframe.shape[0]

    def n_transitions(self):

        return self.transitions_dataframe.shape[0]

    def n_components(self):

        self.microstates_dataframe.groupby(by="component_index").ngroups

    def n_basins(self):

        self.microstates_dataframe.groupby(by="basin_index").ngroups

    def get_microstate_index_from_name(self, name):

        return self.microstate_dataframe[self.microstate_dataframe.name==name].index

    def get_microstate_name_from_index(self, index):

        return self.microstate_dataframe.iloc[index, 1]

    def get_transition_index(origin, end, origin_index=False, end_index=False):

        if not origin_index:
            origin = get_microstate_index_from_name(origin)
        if not origin_end:
            end = get_microstate_index_from_name(end)

        return net.transitions_dataframe[net.transitions_dataframe['origin_index']==origin & net.transitions_dataframe['end_index']==end].index

    def microstate_is_in(self, microstate, microstate_index=False):

        return net.microstates_dataframe['name'].isin([name]).any()

    def transition_is_in(self, origin, end, origin_index=False, end_index=False):

        if not origin_index:
            origin = get_microstate_index_from_name(origin)
        if not origin_end:
            end = get_microstate_index_from_name(end)

        return (net.transitions_dataframe['origin_index']==origin & net.transitions_dataframe['end_index']==end ).any()

    def add_microstate(self, name=None, index=None):

        if index is None:
            index = self.microstates_dataframe.shape[0]

        self.microstates_dataframe.at[index, 'microstate_index']=index
        self.microstates_dataframe.at[index, 'microstate_name']=name
        self.microstates_dataframe.at[index, 'microstate_weight']=0.0
        self.microstates_dataframe.at[index, 'microstate_probability']=0.0

    def add_transition(self, origin, end, weight=1.0, origin_index=False, end_index=False):

        try:
            transition_index = get_transition_index(origin, end, origin_index=origin_index, end_index=end_index)
            self.transitions_dataframe.transition_weight[transition_index] += weight
        except:
            if not microstate_is_in(origin, microstate_index=origin_index):
                self.add_microstate()

        new_index = self.transitions_dataframe.shape[0]

        if not origin_index:
            origin=get_microstate_index_from_name(origin)

        if not end_index:
            end=get_microstate_index_from_name(origin)

        self.microstates_dataframe.at[new_index, 'transition_index'] = new_index
        self.microstates_dataframe.at[new_index, 'origin'] = origin
        self.microstates_dataframe.at[new_index, 'end'] = end

