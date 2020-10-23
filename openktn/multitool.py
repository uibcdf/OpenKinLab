import numpy as np
import simtk.unit as unit
from .utils.targets import singular as targets_singular

# Classes

from .forms.classes import dict_is_form as dict_classes_is_form, \
        dict_new_empty_ktn as dict_classes_new_empty_ktn, \
        dict_add_microstate as dict_classes_add_microstate, \
        dict_add_transition as dict_classes_add_transition, \
        dict_get as dict_classes_get

# Files

from .forms.files import dict_is_form as dict_files_is_form, \
        dict_new_empty_ktn as dict_files_new_empty_ktn, \
        dict_add_microstate as dict_files_add_microstate, \
        dict_add_transition as dict_files_add_transition, \
        dict_get as dict_files_get

dict_is_form = {**dict_classes_is_form, **dict_files_is_form}
dict_new_empty_ktn = {**dict_classes_new_empty_ktn, **dict_files_new_empty_ktn}
dict_add_microstate = {**dict_classes_add_microstate, **dict_files_add_microstate}
dict_add_transition = {**dict_classes_add_transition, **dict_files_add_transition}
dict_get = {**dict_classes_get, **dict_files_get}

def get_form(ktn):

    try:
        return dict_is_form[type(ktn)]
    except:
        try:
            return dict_is_form[ktn]
        except:
            raise NotImplementedError("This KTN's form has not been implemented yet")

def kinetic_transition_network(form='networkx.DiGraph', temperature=0.0*unit.kelvin, time_step=0.0*unit.nanoseconds):

    tmp_ktn = dict_new_empty_ktn[form](temperature=temperature, time_step=time_step)

    return tmp_ktn

def add_microstate(ktn, name=None):

    form = get_form(ktn)

    return dict_add_microstate[form](ktn, name=name)

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    form = get_form(ktn)

    return dict_add_transition[form](ktn, origin, end, weight=weight, origin_index=origin_index,
            end_index=end_index)

def get(ktn, target='microstate', indices=None, selection='all', **kwargs):

    form = get_form(ktn)
    target = targets_singular(target)
    attributes = [ key for key in kwargs.keys() if kwargs[key] ]

    if type(indices)==str:
        if indices in ['all', 'All', 'ALL']:
            indices = 'all'
        else:
            raise ValueError()
    elif type(indices) in [int, np.int64, np.int]:
        indices = np.array([indices], dtype='int64')
    elif hasattr(indices, '__iter__'):
        indices = np.array(indices, dtype='int64')

    if indices is None:
        if selection is not 'all':
            indices = select(ktn, target=target, selection=selection)
        else:
            indices = 'all'

    results = []
    for attribute in attributes:
        result = dict_get[form][target][attribute](ktn, indices=indices)
        results.append(result)

    if len(results)==1:
        return results[0]
    else:
        return results

