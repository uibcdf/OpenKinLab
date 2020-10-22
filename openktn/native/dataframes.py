from pandas import DataFrame as Pandas_DataFrame

class Microstates_DataFrame(Pandas_DataFrame):

    def __init__(self):

        microstates_columns = ['microstate_index', 'microstate_name', 'weight', 'probability', 'component_index',
                            'component_name', 'basin_index', 'basin_name']

        super().__init__(columns=microstates_columns)

class Transition_DataFrame(Pandas_DataFrame):

    def __init__(self):

        transitions_columns = ['microstate_index', 'microstate_name', 'weight', 'probability', 'component_index',
                            'component_name', 'basin_index', 'basin_name']

        super().__init__(columns=transitions_columns)

