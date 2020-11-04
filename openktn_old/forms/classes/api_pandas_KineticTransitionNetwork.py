from os.path import basename as _basename
from openktn.foreign import Pandas_KineticTransitionNetwork as pandas_KineticTransitionNetwork
from openktn.forms.classes import api_pandas_MicrostatesDataFrame as api_microstates
from openktn.forms.classes import api_pandas_TransitionsDataFrame as api_transitions
from simtk.unit import kelvin, nanoseconds
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    pandas_KineticTransitionNetwork : form_name,
    'pandas.KineticTransitionNetwork' : form_name
}

info=["",""]

# Multitool

def new(temperature=None, time_step=None):

    ktn = pandas_KineticTransitionNetwork(temperature=temperature, time_step=time_step)

    return ktn

def add_microstate(ktn, name=None, index=None):

    return api_microstates.add_microstate(ktn.microstates, name=name, index=index)

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    if origin_index:
        if not microstate_is_in(ktn, index=origin):
            add_microstate(ktn, index=origin)
    else:
        if not microstate_is_in(ktn, name=origin):
            add_microstate(ktn, name=origin)
        origin=api_microstates.microstate_name_to_index(ktn.microstates, [origin])[0]
    if end_index:
        if not microstate_is_in(ktn, index=end):
            add_microstate(ktn, index=end)
    else:
        if not microstate_is_in(ktn, name=end):
            add_microstate(ktn, name=end)
        end=api_microstates.microstate_name_to_index(ktn.microstates, [end])[0]

    api_transitions.add_transition(ktn.transitions, origin, end, weight=weight, origin_index=True, end_index=True)

    ktn.microstates.at[origin,'weight']+=weight

def microstate_is_in(ktn, name=None, index=None):

    return api_microstates.microstate_is_in(ktn.microstates, name=name, index=index)

def transition_is_in(ktn, origin, end, origin_index=False, end_index=False):

    if origin_index:
        if not microstate_is_in(ktn, index=origin):
            return False
    else:
        if not microstate_is_in(ktn, name=origin):
            return False
        origin=api_microstates.microstate_name_to_index(ktn.microstates, origin)

    if end_index:
        if not microstate_is_in(ktn, index=end):
            return False
    else:
        if not microstate_is_in(ktn, name=end):
            return False
        end=api_microstates.microstate_name_to_index(ktn.microstates, end)

    return api_transitions.transition_is_in(ktn.transitions, origin, end, origin_index=True,
            end_index=True)

def update_weights(ktn):

    ktn.microstates['weight']=0.0

    aux = ktn.transitions.groupby(by='origin_index')['weight'].sum()
    for index, weight in aux.items():
        ktn.microstates.at[index, 'weight']=weight

def update_probabilities(ktn):

    update_weights(ktn)
    api_transitions.update_probabilities(ktn.transitions)
    api_microstates.update_probabilities(ktn.microstates)

def symmetrize(ktn):

    api_transitions.symmetrize(ktn.transitions)
    update_probabilities(ktn)

def select(ktn, selection):

    raise NotImplementedError

# Convert

# Get

## Aux

## from microstate

def get_index_from_microstate(ktn, indices='all'):

    return get_microstate_index_from_microstate(ktn, indices=indices)

def get_name_from_microstate(ktn, indices='all'):

    return get_microstate_name_from_microstate(ktn, indices=indices)

def get_weight_from_microstate(ktn, indices='all'):

    return get_microstate_weight_from_microstate(ktn, indices=indices)

def get_probability_from_microstate(ktn, indices='all'):

    return get_microstate_probability_from_microstate(ktn, indices=indices)

def get_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_out_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_in_degree_from_microstate(ktn, indices='all'):

    return get_microstate_in_degree_from_microstate(ktn, indices=indices)

def get_microstate_index_from_microstate(ktn, indices='all'):

    return api_microstates.get_microstate_index_from_microstate(ktn.microstates, indices=indices)

def get_microstate_name_from_microstate(ktn, indices='all'):

    return api_microstates.get_microstate_name_from_microstate(ktn.microstates, indices=indices)

def get_microstate_weight_from_microstate(ktn, indices='all'):

    return api_microstates.get_microstate_weight_from_microstate(ktn.microstates, indices=indices)

def get_microstate_probability_from_microstate(ktn, indices='all'):

    return api_microstates.get_microstate_probability_from_microstate(ktn.microstates, indices=indices)

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    if indices is 'all':
        output=np.zeros(ktn.microstates.shape[0], dtype=int)
        aux=ktn.transitions.groupby(by='origin_index')['end_index'].count()
        output[aux.keys()]=aux
    else:
        output = api_transitions.get_microstate_out_degree_from_microstate(ktn.transitions,indices)

    return output

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    if indices is 'all':
        output=np.zeros(ktn.microstates.shape[0], dtype=int)
        aux=ktn.transitions.groupby(by='end_index')['origin_index'].count()
        output[aux.keys()]=aux
    else:
        output = api_transitions.get_microstate_in_degree_from_microstate(ktn.transitions,indices)

    return output

def get_component_index_from_microstate(ktn, indices='all'):

    return api_microstates.get_component_index_from_microstate(ktn.microstates, indices=indices)

def get_basin_index_from_microstate(ktn, indices='all'):

    return api_microstates.get_basin_index_from_microstate(ktn.microstates, indices=indices)

def get_n_microstates_from_microstate(ktn, indices='all'):

    return api_microstates.get_n_microstates_from_microstate(ktn.microstates, indices=indices)

## from transition

def get_index_from_transition(ktn, indices='all'):

    return get_transition_index_from_transition(ktn, indices='all')

def get_origin_index_from_transition(ktn, indices='all'):

    return get_transition_origin_index_from_transition(ktn, indices='all')

def get_end_index_from_transition(ktn, indices='all'):

    return get_transition_end_index_from_transition(ktn, indices='all')

def get_weight_from_transition(ktn, indices='all'):

    return get_transition_weight_from_transition(ktn, indices='all')

def get_probability_from_transition(ktn, indices='all'):

    return get_transition_probability_from_transition(ktn, indices='all')

def get_symmetrized_from_transition(ktn, indices='all'):

    return get_transition_symmetrized_from_transition(ktn, indices='all')

def get_transition_index_from_transition(ktn, indices='all'):

    return api_transitions.get_transition_index_from_transition(ktn.transitions, indices=indices)

def get_transition_origin_index_from_transition(ktn, indices='all'):

    return api_transitions.get_origin_index_from_transition(ktn.transitions, indices=indices)

def get_transition_end_index_from_transition(ktn, indices='all'):

    return api_transitions.get_end_index_from_transition(ktn.transitions, indices=indices)

def get_transition_weight_from_transition(ktn, indices='all'):

    return api_transitions.get_transition_weight_from_transition(ktn.transitions, indices=indices)

def get_transition_probability_from_transition(ktn, indices='all'):

    return api_transitions.get_transition_probability_from_transition(ktn.transitions, indices=indices)

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    return api_transitions.get_transition_symmetrized_from_transition(ktn.transitions, indices=indices)

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    return api_microstates.get_microstate_index_from_network(ktn.microstates)

def get_microstate_name_from_network(ktn, indices='all'):

    return api_microstates.get_microstate_name_from_network(ktn.microstates)

def get_component_index_from_network(ktn, indices='all'):

    return api_microstates.get_component_index_from_network(ktn.microstates)

def get_basin_index_from_network(ktn, indices='all'):

    return api_microstates.get_basin_index_from_network(ktn.microstates)

def get_symmetrized_from_network(ktn, indices='all'):

    return api_transitions.get_symmetrized_from_network(ktn.transitions)

def get_weight_from_network(ktn, indices='all'):

    return api_transitions.get_weight_from_network(ktn.transitions)

def get_temperature_from_network(ktn, indices='all'):

    return ktn.temperature

def get_time_step_from_network(ktn, indices='all'):

    return ktn.time_step

def get_n_microstates_from_network(ktn, indices='all'):

    return api_microstates.get_n_microstates_from_network(ktn.microstates)

def get_n_transitions_from_network(ktn, indices='all'):

    return api_transitions.get_n_transitions_from_network(ktn.transitions)

def get_n_components_from_network(ktn, indices='all'):

    return api_microstates.get_n_components_from_network(ktn.microstates)

def get_n_basins_from_network(ktn, indices='all'):

    return api_microstates.get_n_basins_from_network(ktn.microstates)

def get_form_from_network(ktn, indices='all'):

    return form_name

