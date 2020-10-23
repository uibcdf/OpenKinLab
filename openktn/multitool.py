
# Classes

from .forms.classes import dict_is_form as _dict_classes_is_form, \
        dict_ktn as _dict_classes_ktn, \
        dict_add_microstate as _dict_classes_add_microstate, \
        dict_add_transition as _dict_classes_add_transition

# Files

from .forms.files import dict_is_form as _dict_files_is_form, \
        dict_ktn as _dict_files_ktn, \
        dict_add_microstate as _dict_add_microstate, \
        dict_add_transition as _dict_add_transition

_dict_ktn = {**_dict_classes_ktn, **_dict_files_ktn}
_dict_add_microstate = {**_dict_classes_add_microstate, **_dict_files_add_microstate}
_dict_add_transition = {**_dict_classes_add_transition, **_dict_files_add_transition}

def get_form(ktn):

    try:
        return _dict_is_form[type(item)]
    except:
        try:
            return _dict_is_form[item]
        except:
            raise NotImplementedError("This KTN's form has not been implemented yet")

def kinetic_transition_network(form='networkx.DiGraph', temperature=0.0*unit.kelvin, time_step=0.0*unit.nanoseconds):

    item = _dict_network[form](temperature=temperature, time_step=time_step)

    return item

def add_microstate(ktn, name):

    form = get_form(ktn)

    item = _dict_add_microstate[form](temperature=temperature, time_step=time_step)

    return item

def add_transition(ktn, origin, end, weight=0.0):

    form = get_form(ktn)

    item = _dict_add_transition[form](temperature=temperature, time_step=time_step)

    return item

def get(ktn, target='microstate', indices=None, selection='all', **kwargs):

    form = get_form(ktn)
    target = _singular(target)
    attributes = [ key for key in kwargs.keys() if kwargs[key] ]

    if type(indices)==str:
        if indices in ['all', 'All', 'ALL']:
            indices = 'all'
        else:
            raise ValueError()
    elif type(indices) in [int, _int64, _int]:
        indices = _array([indices], dtype='int64')
    elif hasattr(indices, '__iter__'):
        indices = _array(indices, dtype='int64')



