from pandas import DataFrame as Pandas_DataFrame

class Pandas_TransitionsDataFrame(Pandas_DataFrame):

    def __init__(self):

        from openktn.native.transition import attributes as transition_attributes

        super().__init__(columns=transition_attributes.keys())
        self["index"] = self["index"].astype('int')
        self["origin_index"] = self["origin_index"].astype('int')
        self["end_index"] = self["end_index"].astype('int')
        self["weight"] = self["weight"].astype('float')
        self["probability"] = self["probability"].astype('float')
        self["symmetrized"] = self["symmetrized"].astype('bool')
