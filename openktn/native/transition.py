from pandas import DataFrame as Pandas_DataFrame

attributes = {'index':None, 'weight':0.0, 'probability':0.0, 'symmetrized':False}

class TransitionsDataFrame(Pandas_DataFrame):

    def __init__(self):

        transitions_columns = ['transition_index', 'origin_index', 'end_index', 'transition_weight', 'transition_probability', 'symmetrized']

        super().__init__(columns=transitions_columns)

