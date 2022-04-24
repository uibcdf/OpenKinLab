
def network(time=None, temperature=None):

    from openktn.native.pandas_ktn import PandasKTN

    return PandasKTN(time=time, temperature=temperature)

