from pandas import DataFrame as Pandas_DataFrame

class Microstates_DataFrame(Pandas_DataFrame):

    def __init__(self):

        microstates_columns = ['microstate_name', 'weight', 'probability',
                'transition_indices', 'component_index', 'component_name', 'basin_index', 'basin_name']

        super().__init__(columns=microstates_columns)

    def add_microstate(microstate):

        raise NotImplementedError

    def remove_microstate(microstate_index):

        raise NotImplementedError

    def add_component(microstate_index):

        raise NotImplementedError

    def remove_component(component_index):

        raise NotImplementedError

    def add_basin(microstate_index):

        raise NotImplementedError

    def remove_basin(basin_index):

        raise NotImplementedError



class Transition_DataFrame(Pandas_DataFrame):

    def __init__(self):

        transitions_columns = ['origin_index', 'end_index', 'weight', 'probability']

        super().__init__(columns=transitions_columns)

    def add_transition(transition):

        raise NotImplemented
