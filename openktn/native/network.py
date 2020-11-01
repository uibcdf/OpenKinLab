import numpy as np
from simtk.unit import kelvin, nanoseconds
from openktn.forms.classes import api_pandas_KineticTransitionNetwork as api

attributes = {'temperature':None, 'time_step':None}

class KineticTransitionNetwork():


    def __init__(self, temperature=None, time_step=None):

        from openktn.foreign import Pandas_MicrostatesDataFrame as MicrostatesDataFrame
        from openktn.foreign import Pandas_TransitionsDataFrame as TransitionsDataFrame

        self.microstates=MicrostatesDataFrame()
        self.transitions=TransitionsDataFrame()

        self.temperature=temperature.in_units_of(kelvin)
        self.temperature._value = np.round(self.temperature._value,6)
        self.time_step=time_step.in_units_of(nanoseconds)
        self.time_step._value = np.round(self.time_step._value,6)

    def add_microstate(self, name=None, index=None):

        return api.add_microstate(self, name=name, index=index)

    def add_transition(self, origin, end, weight=1.0, origin_index=False, end_index=False):

        return api.add_transition(self, origin, end, weight=weight, origin_index=origin_index,
                                  end_index=end_index)

