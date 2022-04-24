from pandas import DataFrame

class PandasMicrostates(DataFrame):

    def __init__(self):

        columns = ['index', 'label', 'weight', 'probability', 'basin', 'coordinates', 'color', 'size']


        super().__init__(columns=columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['label', 'weight', 'probability', 'basin', 'coordinates', 'color', 'size']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

