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

def new(n_microstates=0, temperature=None, time_step=None):

    ktn = pandas_MicrostatesDataFrame()

    if n_microstates>0:
        add_microstate(ktn, index=n_microstates)

    return ktn

def add_microstate(ktn, name=None, index=None):

    n_microstates=ktn.shape[0]

    if index is None:
        ktn.at[n_microstates, 'index']=n_microstates
        ktn.at[n_microstates, 'name']=name
        ktn.at[n_microstates, 'weight']=0.0
        ktn.at[n_microstates, 'probability']=0.0
    elif name is not None:
        ktn.at[index, 'index']=index
        ktn.at[index, 'name']=name
        ktn.at[index, 'weight']=0.0
        ktn.at[index, 'probability']=0.0
    else:
        for ii in range(n_microstates, index+1):
            ktn.at[ii, 'index']=ii
            ktn.at[ii, 'weight']=0.0
            ktn.at[ii, 'probability']=0.0

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    raise NotImplementedError("This method does not apply for this KTN form.")

def microstate_in(ktn, name=None, index=None):

    if name is not None:
        output = ktn['name'].isin([name]).any()
    elif index is not None:
        output = ktn['index'].isin([index]).any()
    else:
        raise ValueError

    return output

def transition_in(ktn, origin, end, origin_index=False, end_index=False):

    raise NotImplementedError("This method does not apply for this KTN form.")

def update_weights(ktn):

    raise NotImplementedError("This method does not apply for this KTN form.")

def update_probabilities(ktn):

    weight = get_network_weight_from_network(ktn)
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

    output = None
    if indices is 'all':
        output = ktn.loc[:,'index'].to_numpy()
    else:
        output = ktn.loc[indices,'index'].to_numpy()
    return output

def get_microstate_name_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'name'].to_numpy()
    else:
        output = ktn.loc[indices,'name'].to_numpy()
    return output

def get_microstate_weight_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'weight'].to_numpy()
    else:
        output = ktn.loc[indices,'weight'].to_numpy()
    return output

def get_microstate_probability_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'probability'].to_numpy()
    else:
        output = ktn.loc[indices,'probability'].to_numpy()
    return output

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    ouput=None
    if indices is 'all':
        output = np.fill(np.nan, ktn.shape[0])
    else:
        output = np.fill(np.nan, indices.shape[0])

    return output

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    ouput=None
    if indices is 'all':
        output = np.fill(np.nan, ktn.shape[0])
    else:
        output = np.fill(np.nan, indices.shape[0])

    return output

def get_component_index_from_microstate(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'component_index'].to_numpy()
    else:
        output = ktn.loc[indices,'component_index'].to_numpy()
    return output

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

