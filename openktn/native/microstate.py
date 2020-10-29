from pandas import DataFrame as Pandas_DataFrame

attributes = {'index':None, 'name':None, 'weight':0.0, 'probability':0.0, 'component_index':None,
              'basin_index':None, 'coordinates':None, 'color':None, 'size':None}

class MicrostatesDataFrame(Pandas_DataFrame):

    def __init__(self):

        microstates_columns = ['microstate_index', 'microstate_name', 'microstate_weight',
                'microstate_probability', 'component_index', 'basin_index', 'coordinates', 'color',
                'size']

        super().__init__(columns=microstates_columns)

