import numpy as np
import simtk.unit as unit
from .utils.targets import singular as targets_singular

# Classes

from .forms.classes import dict_is_form as dict_classes_is_form, \
        dict_new_empty_ktn as dict_classes_new_empty_ktn, \
        dict_add_microstate as dict_classes_add_microstate, \
        dict_add_transition as dict_classes_add_transition, \
        dict_microstate_in_ktn as dict_classes_microstate_in_ktn, \
        dict_transition_in_ktn as dict_classes_transition_in_ktn, \
        dict_update_weights as dict_classes_update_weights, \
        dict_update_probabilities as dict_classes_update_probabilities, \
        dict_symmetrize as dict_classes_symmetrize, \
        dict_get as dict_classes_get

# Files

from .forms.files import dict_is_form as dict_files_is_form, \
        dict_new_empty_ktn as dict_files_new_empty_ktn, \
        dict_add_microstate as dict_files_add_microstate, \
        dict_add_transition as dict_files_add_transition, \
        dict_microstate_in_ktn as dict_files_microstate_in_ktn, \
        dict_transition_in_ktn as dict_files_transition_in_ktn, \
        dict_update_weights as dict_files_update_weights, \
        dict_update_probabilities as dict_files_update_probabilities, \
        dict_symmetrize as dict_files_symmetrize, \
        dict_get as dict_files_get

dict_is_form = {**dict_classes_is_form, **dict_files_is_form}
dict_new_empty_ktn = {**dict_classes_new_empty_ktn, **dict_files_new_empty_ktn}
dict_add_microstate = {**dict_classes_add_microstate, **dict_files_add_microstate}
dict_add_transition = {**dict_classes_add_transition, **dict_files_add_transition}
dict_microstate_in_ktn = {**dict_classes_microstate_in_ktn, **dict_files_microstate_in_ktn}
dict_transition_in_ktn = {**dict_classes_transition_in_ktn, **dict_files_transition_in_ktn}
dict_update_weights = {**dict_classes_update_weights, **dict_files_update_weights}
dict_update_probabilities = {**dict_classes_update_probabilities, **dict_files_update_probabilities}
dict_symmetrize = {**dict_classes_symmetrize, **dict_files_symmetrize}
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

def add_transition(ktn, origin, end, weight=1.0, origin_index=False, end_index=False):

    form = get_form(ktn)

    return dict_add_transition[form](ktn, origin, end, weight=weight, origin_index=origin_index, end_index=end_index)

def microstate_in_ktn(ktn, name):

    form = get_form(ktn)

    return dict_microstate_in_ktn[form](ktn, name)

def transition_in_ktn(ktn, origin, end, origin_index=False, end_index=False):

    form = get_form(ktn)

    return dict_transition_in_ktn[form](ktn, origin, end, origin_index=False, end_index=False)

def update_weights(ktn):

    form = get_form(ktn)

    return dict_update_weights[form](ktn)

def update_probabilities(ktn):

    form = get_form(ktn)

    return dict_update_probabilities[form](ktn)

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

def symmetrize(ktn):

    form = get_form(ktn)

    return dict_symmetrize[form](ktn)

def info(ktn, target='network', indices=None, selection='all', output='dataframe'):

    if output=='dataframe':

        from pandas import DataFrame as df
        form = get_form(ktn)
        target = targets_singular(target)

        if target=='microstate':

            raise NotImplementedError

        elif target=='transition':

            raise NotImplementedError

        elif target=='component':

            raise NotImplementedError

        elif target=='basin':

            raise NotImplementedError

        elif target=='network':

            form, n_microstates, n_transitions, n_components, n_basins, weight, symmetrized, temperature, time_step = get(ktn, target=target,
                    form=True, n_microstates=True, n_transitions=True, n_components=True, n_basins=True,
                    weight=True, symmetrized=True, temperature=True, time_step=True)

            tmp_df = df({'form':form, 'n_microstates':n_microstates, 'n_transitions':n_transitions, 'n_components':n_components,
                         'n_basins':n_basins, 'weight':weight, 'symmetrized':symmetrized,
                         'temperature':temperature, 'time_step':time_step}, index=[0])

            if n_components==None: tmp_df.drop(columns=['n_components'], inplace=True)
            if n_basins==None: tmp_df.drop(columns=['n_basins'], inplace=True)

            return tmp_df.style.hide_index()

        else:

            raise ValueError('"target" needs one of the following strings: "network", "microstate",\
                             "transition", "component", "basin"')

