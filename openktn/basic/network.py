
def network(time=None, temperature=None, form='openktn.KTN'):

    tmp_ktn = dict_network[form](temperature=temperature, time_step=time_step)

    return tmp_ktn

