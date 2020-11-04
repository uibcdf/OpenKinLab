from pandas import DataFrame as Pandas_DataFrame

class Pandas_MicrostatesDataFrame(Pandas_DataFrame):

    def __init__(self):

        from openktn.native.microstate import attributes as microstate_attributes

        super().__init__(columns=microstate_attributes.keys())

