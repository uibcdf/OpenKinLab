from pandas import DataFrame as Pandas_DataFrame

class Pandas_TransitionsDataFrame(Pandas_DataFrame):

    def __init__(self):

        from openktn.native.transition import attributes as transition_attributes

        super().__init__(columns=transition_attributes.keys())
