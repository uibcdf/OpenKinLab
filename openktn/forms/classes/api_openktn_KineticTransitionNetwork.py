from os.path import basename as _basename
from openktn.native import KineticTransitionNetwork as openktn_KineticTransitionNetwork
from simtk.unit import kelvin, nanoseconds
from openktn.native.network import attributes as network_attributes
from openktn.native.microstate import attributes as microstate_attributes
from openktn.native.transition import attributes as transition_attributes
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    openktn_KineticTransitionNetwork : form_name,
    'openktn.KineticTransitionNetwork' : form_name
}

info=["",""]

# Multitool

def new_empty_ktn(n_microstates=0, temperature=None, time_step=None):

    return openktn_KineticTransitionNetwork(n_microstates=n_microstates, temperature=temperature, time_step=time_step)

def add_microstate(ktn, name=None):

    return ktn.add_microstate(name=name)

def add_transition(ktn, origin, end, weight=1.0, origin_index=False, end_index=False):

    raise NotImplementedError

def microstate_in_ktn(ktn, name):

    raise NotImplementedError

def transition_in_ktn(ktn, origin, end, origin_index=False, end_index=False):

    raise NotImplementedError

def update_weights(ktn):

    raise NotImplementedError

def update_probabilities(ktn):

    raise NotImplementedError

def symmetrize(ktn):

    raise NotImplementedError

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

def get_microstate_index_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = get_microstate_index_from_network(ktn)
    else:
        output = indices

    return output

def get_microstate_name_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = get_microstate_name_from_network(ktn)
    else:
        raise NotImplementedError

    return output

def get_microstate_weight_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError
    else:
        raise NotImplementedError

    return output

def get_microstate_probability_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError
    else:
        raise NotImplementedError

    return output


## from network

def get_microstate_index_from_network(ktn, indices='all'):

    n_microstates=get_n_microstates_from_network(ktn)
    return np.arange(n_microstates)

def get_microstate_name_from_network(ktn, indices='all'):

    raise NotImplementedError

def get_component_index_from_network(ktn, indices='all'):

    output = None
    n_components=get_n_components_from_network(ktn)
    if n_components is not None:
        return np.arange(n_components)

def get_basin_index_from_network(ktn, indices='all'):

    output = None
    n_basins=get_n_basins_from_network(ktn)
    if n_basins is not None:
        return np.arange(n_basins)

def get_symmetrized_from_network(ktn, indices='all'):

    return ktn.symmetrized

def get_weight_from_network(ktn, indices='all'):

    return ktn.weight

def get_temperature_from_network(ktn, indices='all'):

    return ktn.temperature

def get_time_step_from_network(ktn, indices='all'):

    return ktn.time_step

def get_n_microstates_from_network(ktn, indices='all'):

    return ktn.n_microstates()

def get_n_transitions_from_network(ktn, indices='all'):

    return ktn.n_transitions()

def get_n_components_from_network(ktn, indices='all'):

    return ktn.n_components()

def get_n_basins_from_network(ktn, indices='all'):

    return ktn.n_basins()

def get_form_from_network(ktn, indices='all'):

    return form_name

