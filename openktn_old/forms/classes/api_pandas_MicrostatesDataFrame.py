from os.path import basename as _basename
from openktn.foreign import Pandas_MicrostatesDataFrame as pandas_MicrostatesDataFrame
from simtk.unit import kelvin, nanoseconds
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    pandas_MicrostatesDataFrame : form_name,
    'pandas.MicrostatesDataFrame' : form_name
}

info=["",""]

# Multitool

def new(temperature=None, time_step=None):

    ktn = pandas_MicrostatesDataFrame()

    return ktn

def add_microstate(ktn, name=None):

    n_microstates=ktn.shape[0]

    if name is None:
        name = n_microstates

    ktn.at[n_microstates, 'name']=name
    ktn.at[n_microstates, 'weight']=0.0
    ktn.at[n_microstates, 'probability']=0.0

def add_transition(ktn, origin, end, weight=0.0):

    raise NotImplementedError("This method does not apply for this KTN form.")

def microstate_is_in(ktn, name):

    return (ktn.name.to_numpy()==name).any()

def transition_is_in(ktn, origin, end):

    return ((ktn.origin.to_numpy()==origin)*(ktn.end.to_numpy()==end)) .any()

def update_weights(ktn):

    raise NotImplementedError("This method does not apply for this KTN form.")

def update_probabilities(ktn):

    weight = get_weight_from_network(ktn)
    if weight:
        ktn['probability']=ktn['weight']/weight

def symmetrize(ktn):

    raise NotImplementedError("This method does not apply for this KTN form.")

def select(ktn, selection):

    raise NotImplementedError

# Convert

# Get

# Aux

def _microstate_name_to_index(ktn, name):

    return ktn[ktn['name']==name].index[0]

microstate_name_to_index = np.vectorize(_microstate_name_to_index, excluded=[0])

## from microstate

def get_index_from_microstate(ktn, names=None):

    return get_microstate_index_from_microstate(ktn, names=names)

def get_name_from_microstate(ktn, names=None):

    return get_microstate_name_from_microstate(ktn, names=names)

def get_weight_from_microstate(ktn, names=None):

    return get_microstate_weight_from_microstate(ktn, names=names)

def get_probability_from_microstate(ktn, names=None):

    return get_microstate_probability_from_microstate(ktn, names=names)

def get_degree_from_microstate(ktn, names=None):

    return get_microstate_out_degree_from_microstate(ktn, names=names)

def get_out_degree_from_microstate(ktn, names=None):

    return get_microstate_out_degree_from_microstate(ktn, names=names)

def get_in_degree_from_microstate(ktn, names=None):

    return get_microstate_in_degree_from_microstate(ktn, names=names)

def _vf(array_names, name):
    output=np.argwhere(array_names==name)[0][0]
    return output

vf = np.vectorize(_vf, excluded[0])

def get_microstate_index_from_microstate(ktn, names=None):

    if names is None:
        return ktn.index.to_numpy()
    else:
        return vf(ktn.name.to_numpy(), names)

def get_microstate_name_from_microstate(ktn, names=None):

    if names is 'all':
        return ktn.name.to_numpy()
    else:
        return names

def get_microstate_weight_from_microstate(ktn, names=None):

    if names is 'all':
        return ktn.weight.to_numpy()
    else:
        indices = get_microstate_index_from_microstate(ktn, names=names)
        output = ktn.loc[indices,'weight'].to_numpy()

def get_microstate_probability_from_microstate(ktn, names=None):

    if names is 'all':
        return = ktn.probability.to_numpy()
    else:
        indices = get_microstate_index_from_microstate(ktn, names=names)
        return ktn.probability[indices].to_numpy()

def get_microstate_degree_from_microstate(ktn, names=None):

    return get_microstate_out_degree_from_microstate(ktn, names=names)

def get_microstate_out_degree_from_microstate(ktn, names=None):

    if names is None:
        return np.fill(np.nan, ktn.shape[0])
    else:
        return np.fill(np.nan, names.shape[0])

def get_microstate_in_degree_from_microstate(ktn, names=None):

    if names is None:
        return np.fill(np.nan, ktn.shape[0])
    else:
        return np.fill(np.nan, names.shape[0])

def get_component_from_microstate(ktn, names=None):

    if indices is 'all':
        return ktn.component.to_numpy()
    else:
        indices = get_microstate_index_from_microstate(ktn, names=names)
        return ktn.component[indices].to_numpy()

def get_basin_index_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'basin_index'].to_numpy()
    else:
        output = ktn.loc[indices,'basin_index'].to_numpy()
    return output

def get_n_microstates_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output=get_n_microstates_from_network(ktn)
    else:
        output=indices.shape[0]
    return output

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

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_transition_origin_index_from_transition(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_transition_end_index_from_transition(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_transition_weight_from_transition(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_transition_probability_from_transition(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    return get_microstate_index_from_microstate(ktn, indices='all')

def get_microstate_name_from_network(ktn, indices='all'):

    return get_microstate_name_from_microstate(ktn, indices='all')

def get_component_index_from_network(ktn, indices='all'):

    return get_component_index_from_microstate(ktn, indices='all')

def get_basin_index_from_network(ktn, indices='all'):

    return get_basin_index_from_microstate(ktn, indices='all')

def get_symmetrized_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_weight_from_network(ktn, indices='all'):

    return ktn['weight'].sum()

def get_temperature_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_time_step_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_microstates_from_network(ktn, indices='all'):

    return ktn.shape[0]

def get_n_transitions_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_components_from_network(ktn, indices='all'):

    return ktn.groupby('component_index').ngroups

def get_n_basins_from_network(ktn, indices='all'):

    return ktn.groupby('basin_index').ngroups

def get_form_from_network(ktn, indices='all'):

    return form_name

