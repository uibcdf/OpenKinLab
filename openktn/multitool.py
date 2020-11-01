import numpy as np
import simtk.unit as unit
from .utils.targets import to_singular as singular_target
from .utils.indices import intersection_indices

# Classes

from .forms.classes import dict_is_form as dict_classes_is_form, \
        dict_new as dict_classes_new, \
        dict_add_microstate as dict_classes_add_microstate, \
        dict_add_transition as dict_classes_add_transition, \
        dict_microstate_in as dict_classes_microstate_in, \
        dict_transition_in as dict_classes_transition_in, \
        dict_update_weights as dict_classes_update_weights, \
        dict_update_probabilities as dict_classes_update_probabilities, \
        dict_symmetrize as dict_classes_symmetrize, \
        dict_select as dict_classes_select, \
        dict_get as dict_classes_get

# Files

from .forms.files import dict_is_form as dict_files_is_form, \
        dict_new as dict_files_new, \
        dict_add_microstate as dict_files_add_microstate, \
        dict_add_transition as dict_files_add_transition, \
        dict_microstate_in as dict_files_microstate_in, \
        dict_transition_in as dict_files_transition_in, \
        dict_update_weights as dict_files_update_weights, \
        dict_update_probabilities as dict_files_update_probabilities, \
        dict_symmetrize as dict_files_symmetrize, \
        dict_select as dict_files_select, \
        dict_get as dict_files_get

dict_is_form = {**dict_classes_is_form, **dict_files_is_form}
dict_new = {**dict_classes_new, **dict_files_new}
dict_add_microstate = {**dict_classes_add_microstate, **dict_files_add_microstate}
dict_add_transition = {**dict_classes_add_transition, **dict_files_add_transition}
dict_microstate_in = {**dict_classes_microstate_in, **dict_files_microstate_in}
dict_transition_in = {**dict_classes_transition_in, **dict_files_transition_in}
dict_update_weights = {**dict_classes_update_weights, **dict_files_update_weights}
dict_update_probabilities = {**dict_classes_update_probabilities, **dict_files_update_probabilities}
dict_symmetrize = {**dict_classes_symmetrize, **dict_files_symmetrize}
dict_select = {**dict_classes_select, **dict_files_select}
dict_get = {**dict_classes_get, **dict_files_get}

def get_form(ktn):

    try:
        return dict_is_form[type(ktn)]
    except:
        try:
            return dict_is_form[ktn]
        except:
            raise NotImplementedError("This KTN's form has not been implemented yet")

def kinetic_transition_network(form='openktn.KineticTransitionNetwork', n_microstates=0, temperature=0.0*unit.kelvin, time_step=0.0*unit.nanoseconds):

    tmp_ktn = dict_new[form](temperature=temperature, time_step=time_step)

    return tmp_ktn

def add_microstate(ktn, name=None, index=None):

    form = get_form(ktn)

    return dict_add_microstate[form](ktn, name=name, index=index)

def add_transition(ktn, origin, end, weight=1.0, origin_index=False, end_index=False):

    form = get_form(ktn)

    return dict_add_transition[form](ktn, origin, end, weight=weight, origin_index=origin_index, end_index=end_index)

def microstate_in(ktn, name=None, index=None):

    form = get_form(ktn)

    return dict_microstate_in[form](ktn, name=name, index=index)

def transition_in(ktn, origin, end, origin_index=False, end_index=False):

    form = get_form(ktn)

    return dict_transition_in[form](ktn, origin, end, origin_index=False, end_index=False)

def transitions_out(ktn, origin, with_name=False):

    raise NotImplementedError

def transitions_in(ktn, end, with_name=False):

    raise NotImplementedError

def update_weights(ktn):

    form = get_form(ktn)

    return dict_update_weights[form](ktn)

def update_probabilities(ktn):

    form = get_form(ktn)

    return dict_update_probabilities[form](ktn)

def select(ktn, selection='all', target='microstate', mask=None):

    form = get_form(ktn)

    if type(selection)==str:
        if selection in ['all', 'All', 'ALL']:
            n_microstates = dict_get[form]['network']['n_microstates'](ktn)
            microstate_indices = np.arange(n_microstates, dtype='int64')
        else:
            microstate_indices = dict_selector[form](ktn, selection)
    elif type(selection) in [int, _int64, _int]:
        microstate_indices = np.array([selection], dtype='int64')
    elif hasattr(selection, '__iter__'):
        microstate_indices = np.array(selection, dtype='int64')
    else :
        microstate_indices = None

    output_indices = None

    if target=='microstate':
        output_indices = microstate_indices
    elif target=='component':
        output_indices = get(item, target='microstate', indices=microstate_indices, component_index=True)
        output_indices = _unique(output_indices)
    elif target=='basin':
        output_indices = get(item, target='microstate', indices=microstate_indices, basin_index=True)
        output_indices = _unique(output_indices)
    elif target=='transition':
        output_indices = get(item, target='microstate', indices=microstate_indices, inner_transition_index=True)

    if mask is not None:
        output_indices = intersection_indices(output_indices,mask)

    return output_indices

def get(ktn, target='microstate', indices=None, selection='all', **kwargs):

    form = get_form(ktn)
    target = singular_target(target)
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
        target = singular_target(target)

        if target=='microstate':

            if get(ktn, target='network', symmetrized=True):

                index, name, weight, probability, degree, component_index, basin_index = get(ktn, target=target,
                    microstate_index=True, microstate_name=True, weight=True, probability=True, degree=True,
                    component_index=True, basin_index=True)

                tmp_df = df({'index':index, 'name':name, 'weight':weight, 'probability':probability,
                            'degree':degree, 'component_index':component_index, 'basin_index':basin_index})

            else:

                index, name, weight, probability, out_degree, in_degree, component_index, basin_index = get(ktn, target=target,
                    microstate_index=True, microstate_name=True, weight=True, probability=True, out_degree=True, in_degree=True,
                    component_index=True, basin_index=True)

                tmp_df = df({'index':index, 'name':name, 'weight':weight, 'probability':probability,
                    'out_degree':out_degree, 'in_degree':in_degree, 'component_index':component_index,
                    'basin_index':basin_index})

            n_components, n_basins = get(ktn, target='network', n_components=True, n_basins=True)
            if n_components==0: tmp_df.drop(columns=['component_index'], inplace=True)
            if n_basins==0: tmp_df.drop(columns=['basin_index'], inplace=True)

            return tmp_df.style.hide_index()

        elif target=='transition':

            index, origin_index, end_index, weight, probability, symmetrized = get(ktn, target=target,
                    transition_index=True, origin_index=True, end_index=True,
                    transition_weight=True, transition_probability=True, symmetrized=True)

            tmp_df = df({'index':index, 'origin_index':origin_index, 'end_index':end_index, 'weight':weight,
                'probability':probability, 'symmetrized':symmetrized})

            return tmp_df.style.hide_index()

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

            if n_components==0: tmp_df.drop(columns=['n_components'], inplace=True)
            if n_basins==0: tmp_df.drop(columns=['n_basins'], inplace=True)

            return tmp_df.style.hide_index()

        else:

            raise ValueError('"target" needs one of the following strings: "network", "microstate",\
                             "transition", "component", "basin"')

