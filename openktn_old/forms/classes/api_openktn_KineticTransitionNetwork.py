from os.path import basename as _basename
from openktn.native import KineticTransitionNetwork as openktn_KineticTransitionNetwork
from openktn.forms.classes import api_pandas_KineticTransitionNetwork as api
from simtk.unit import kelvin, nanoseconds
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    openktn_KineticTransitionNetwork : form_name,
    'openktn.KineticTransitionNetwork' : form_name
}

info=["",""]

# Multitool

def new(temperature=None, time_step=None):

    ktn = openktn_KineticTransitionNetwork(temperature=temperature, time_step=time_step)

    return ktn

def add_microstate(ktn, name=None, index=None):

    return api.add_microstate(ktn, name=name, index=index)

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    return api.add_transition(ktn, origin, end, weight=weight, origin_index=origin_index,
                              end_index=end_index)

def microstate_is_in(ktn, name=None, index=None):

    return api.microstate_in(ktn, name=name, index=index)

def transition_is_in(ktn, origin, end, origin_index=False, end_index=False):

    return api.transition_in(ktn, origin, end, origin_index=origin_index, end_index=end_index)

def update_weights(ktn):

    return api.update_weights(ktn)

def update_probabilities(ktn):

    return api.update_probabilities(ktn)

def symmetrize(ktn):

    return api.symmetrize(ktn)

def select(ktn, selection):

    raise NotImplementedError

# Convert

# Get

## Aux

## from microstate

def get_index_from_microstate(ktn, indices='all'):

    return api.get_index_from_microstate(ktn, indices=indices)

def get_name_from_microstate(ktn, indices='all'):

    return api.get_name_from_microstate(ktn, indices=indices)

def get_weight_from_microstate(ktn, indices='all'):

    return api.get_weight_from_microstate(ktn, indices=indices)

def get_probability_from_microstate(ktn, indices='all'):

    return api.get_probability_from_microstate(ktn, indices=indices)

def get_degree_from_microstate(ktn, indices='all'):

    return api.get_degree_from_microstate(ktn, indices=indices)

def get_out_degree_from_microstate(ktn, indices='all'):

    return api.get_out_degree_from_microstate(ktn, indices=indices)

def get_in_degree_from_microstate(ktn, indices='all'):

    return api.get_in_degree_from_microstate(ktn, indices=indices)

def get_microstate_index_from_microstate(ktn, indices='all'):

    return api.get_microstate_index_from_microstate(ktn, indices=indices)

def get_microstate_name_from_microstate(ktn, indices='all'):

    return api.get_microstate_name_from_microstate(ktn, indices=indices)

def get_microstate_weight_from_microstate(ktn, indices='all'):

    return api.get_microstate_weight_from_microstate(ktn, indices=indices)

def get_microstate_probability_from_microstate(ktn, indices='all'):

    return api.get_microstate_probability_from_microstate(ktn, indices=indices)

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return api.get_microstate_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    return api.get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    return api.get_microstate_in_degree_from_microstate(ktn, indices=indices)

def get_component_index_from_microstate(ktn, indices='all'):

    return api.get_component_index_from_microstate(ktn, indices=indices)

def get_basin_index_from_microstate(ktn, indices='all'):

    return api.get_basin_index_from_microstate(ktn, indices=indices)

def get_n_microstates_from_microstate(ktn, indices='all'):

    return api.get_n_microstates_from_microstate(ktn, indices=indices)

## from transition

def get_index_from_transition(ktn, indices='all'):

    return api.get_index_from_transition(ktn, indices=indices)

def get_origin_index_from_transition(ktn, indices='all'):

    return api.get_origin_index_from_transition(ktn, indices=indices)

def get_end_index_from_transition(ktn, indices='all'):

    return api.get_end_index_from_transition(ktn, indices=indices)

def get_weight_from_transition(ktn, indices='all'):

    return api.get_weight_from_transition(ktn, indices=indices)

def get_probability_from_transition(ktn, indices='all'):

    return api.get_probability_from_transition(ktn, indices=indices)

def get_symmetrized_from_transition(ktn, indices='all'):

    return api.get_symmetrized_from_transition(ktn, indices=indices)

def get_transition_index_from_transition(ktn, indices='all'):

    return api.get_transition_index_from_transition(ktn, indices=indices)

def get_transition_origin_index_from_transition(ktn, indices='all'):

    return api.get_transition_origin_index_from_transition(ktn, indices=indices)

def get_transition_end_index_from_transition(ktn, indices='all'):

    return api.get_transition_end_index_from_transition(ktn, indices=indices)

def get_transition_weight_from_transition(ktn, indices='all'):

    return api.get_transition_weight_index_from_transition(ktn, indices=indices)

def get_transition_probability_from_transition(ktn, indices='all'):

    return api.get_transition_probability_index_from_transition(ktn, indices=indices)

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    return api.get_transition_symmetrized_index_from_transition(ktn, indices=indices)

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    return api.get_microstate_index_from_network(ktn, indices=indices)

def get_microstate_name_from_network(ktn, indices='all'):

    return api.get_microstate_name_from_network(ktn, indices=indices)

def get_component_index_from_network(ktn, indices='all'):

    return api.get_component_index_from_network(ktn, indices=indices)

def get_basin_index_from_network(ktn, indices='all'):

    return api.get_basin_index_from_network(ktn, indices=indices)

def get_symmetrized_from_network(ktn, indices='all'):

    return api.get_symmetrized_from_network(ktn, indices=indices)

def get_weight_from_network(ktn, indices='all'):

    return api.get_weight_from_network(ktn, indices=indices)

def get_temperature_from_network(ktn, indices='all'):

    return api.get_temperature_from_network(ktn, indices=indices)

def get_time_step_from_network(ktn, indices='all'):

    return api.get_time_step_from_network(ktn, indices=indices)

def get_n_microstates_from_network(ktn, indices='all'):

    return api.get_n_microstates_from_network(ktn, indices=indices)

def get_n_transitions_from_network(ktn, indices='all'):

    return api.get_n_transitions_from_network(ktn, indices=indices)

def get_n_components_from_network(ktn, indices='all'):

    return api.get_n_components_from_network(ktn, indices=indices)

def get_n_basins_from_network(ktn, indices='all'):

    return api.get_n_basins_from_network(ktn, indices=indices)

def get_form_from_network(ktn, indices='all'):

    return form_name

