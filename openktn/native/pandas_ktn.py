from pandas import DataFrame

class PandasKTN():

    def __init__(self):

        from .pandas_microstates import PandasMicrostates
        from .pandas_microstates import PandasTransitions

        self.microstates = PandasMicrostates()
        self.transitions = PandasTransitions()

        self.temperature = None
        self.time = None

class Pandas_MicrostatesDataFrame(DataFrame):

    def __init__(self):

        from openktn.native.microstate import attributes as microstate_attributes

        super().__init__(columns=microstate_attributes.keys())

class Pandas_TransitionsDataFrame(DataFrame):

    def __init__(self):

        from openktn.native.transition import attributes as transition_attributes

        super().__init__(columns=transition_attributes.keys())

