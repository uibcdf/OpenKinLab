from pandas import DataFrame as Pandas_DataFrame

class Pandas_MicrostatesDataFrame(Pandas_DataFrame):

    def __init__(self):

        from openktn.native.microstate import attributes as microstate_attributes

        super().__init__(columns=microstate_attributes.keys())
        self["index"] = self["index"].astype('int')
        self["name"] = self["name"].astype('object')
        self["weight"] = self["weight"].astype('float')
        self["probability"] = self["probability"].astype('float')
        self["component_index"] = self["component_index"].astype('int')
        self["basin_index"] = self["basin_index"].astype('int')

