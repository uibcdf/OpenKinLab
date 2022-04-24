from pandas import DataFrame

class PandasMicrostates(DataFrame):

    def __init__(self):

        columns = ['index', 'origin', 'end', 'weight', 'probability', 'color', 'size']

        self.origin  = None
        self.end = None
        self.weight = 0.0
        self.probability = 0.0

        self.color = None
        self.size = None

        super().__init__(columns=columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['origin', 'end', 'weight', 'probability', 'color', 'size']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

