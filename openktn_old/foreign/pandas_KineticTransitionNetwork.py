
class Pandas_KineticTransitionNetwork():

    def __init__(self, temperature=None, time_step=None):

        from . import Pandas_MicrostatesDataFrame, Pandas_TransitionsDataFrame
        from openktn.native.network import attributes as network_attributes

        self.microstates = Pandas_MicrostatesDataFrame()
        self.transitions = Pandas_TransitionsDataFrame()

        for attribute, value in network_attributes.items():
            setattr(self, attribute, value)

        self.temperature=temperature
        self.time_step=time_step

