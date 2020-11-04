from os.path import basename as _basename
from openktn.foreign import Pandas_TransitionsDataFrame as pandas_TransitionsDataFrame
from simtk.unit import kelvin, nanoseconds
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    pandas_TransitionsDataFrame : form_name,
    'pandas.TransitionsDataFrame' : form_name
}

info=["",""]

# Multitool

def new(time_step=None, temperature=None):

    ktn = pandas_TransitionsDataFrame()

    return ktn

def add_microstate(ktn, name=None):

    raise NotImplementedError("This method does not apply for this KTN form.")

def add_transition(ktn, origin, end, weight=0.0):

    if not transition_is_in(ktn, origin, end):

        n_transitions = ktn.shape[0]

        ktn.at[n_transitions, 'index']=n_transitions
        ktn.at[n_transitions, 'origin_index']=origin
        ktn.at[n_transitions, 'end_index']=end
        ktn.at[n_transitions, 'weight']=weight
        ktn.at[n_transitions, 'probability']=0.0
        ktn.at[n_transitions, 'symmetrized']=False

    else:

        index = transition_origin_end_to_index(ktn,origin,end)
        ktn.at[index,'weight']+=weight

def microstate_is_in(ktn, name):

    raise NotImplementedError("This method does not apply for this KTN form.")

def transition_is_in(ktn, origin, end):

    if ktn.shape[0]==0:
        return False
    else:
        return (ktn['origin_index'].isin([origin]) & ktn['end_index'].isin([end])).any()

def update_weights(ktn):

    raise NotImplementedError("This method does not apply for this KTN form.")

def update_probabilities(ktn):

    ktn['probability']=ktn['weight']/ktn.groupby(by='origin_index')['weight'].transform('sum')

def symmetrize(ktn):

    ktn['symmetrized']=False

    for index in range(ktn.shape[0]):
        if not ktn.at[index,'symmetrized']:
            origin = ktn.at[index,'origin_index']
            end = ktn.at[index,'end_index']
            if transition_is_in(ktn, end, origin):
                back_index = transition_origin_end_to_index(ktn, end, origin)
                weight=0.5*(ktn.at[index,'weight']+ktn.at[back_index,'weight'])
                ktn.at[index,'weight']=weight
                ktn.at[back_index,'weight']=weight
            else:
                weight=0.5*ktn.at[index,'weight']
                ktn.at[index,'weight']=weight
                back_index=ktn.shape[0]
                add_transition(ktn, end, origin, weight=weight)
            ktn.at[index,'symmetrized']=True
            ktn.at[back_index,'symmetrized']=True

    update_probabilities(ktn)

def select(ktn, selection):

    raise NotImplementedError

# Convert

# Get

## Aux

#def transition_origin_end_to_index(ktn, origin, end):
#
#    return ktn.loc[(ktn['origin_index']==origin) & (ktn['end_index']==end)].index[0]
#
#def _microstate_out_degree_from_microstate(ktn, index):
#
#    return ktn['origin_index'].isin([index]).sum()
#
#_microstate_out_degree_from_microstate_vect = np.vectorize(_microstate_out_degree_from_microstate, excluded=[0])
#
#def _microstate_in_degree_from_microstate(ktn, index):
#
#    return ktn['end_index'].isin([index]).sum()
#
#_microstate_in_degree_from_microstate_vect = np.vectorize(_microstate_in_degree_from_microstate, excluded=[0])
#
#
#def _microstate_weight_from_microstate(ktn, index):
#
#    return ktn[ktn['end_index'].isin([index])]['weight'].sum()
#
#_microstate_weight_from_microstate_vect = np.vectorize(_microstate_weight_from_microstate, excluded=[0])


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

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_microstate_name_from_microstate(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_microstate_weight_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError("This method does not apply for this KTN form.")
    else:
        output = _microstate_weight_from_microstate_vect(ktn,indices)

    return output

def get_microstate_probability_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError("This method does not apply for this KTN form.")
    else:
        weight = get_weight_from_network(ktn)
        output = _microstate_weight_from_microstate_vect(ktn,indices)/weight

    return output

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError("This method does not apply for this KTN form.")
    else:
        output = _microstate_out_degree_from_microstate_vect(ktn,indices)

    return output

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        raise NotImplementedError("This method does not apply for this KTN form.")
    else:
        output = _microstate_in_degree_from_microstate_vect(ktn,indices)

    return output

def get_component_index_from_microstate(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_basin_index_from_microstate(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_microstates_from_microstate(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

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

    output = None
    if indices is 'all':
        n_transitions = get_n_transitions_from_network(ktn)
        output=np.arange(n_transitions)
    else:
        output=indices
    return output

def get_transition_origin_index_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'origin_index'].to_numpy()
    else:
        output = ktn.loc[indices,'origin_index'].to_numpy()
    return output

def get_transition_end_index_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'end_index'].to_numpy()
    else:
        output = ktn.loc[indices,'end_index'].to_numpy()
    return output

def get_transition_weight_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'weight'].to_numpy()
    else:
        output = ktn.loc[indices,'weight'].to_numpy()
    return output

def get_transition_probability_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'probability'].to_numpy()
    else:
        output = ktn.loc[indices,'probability'].to_numpy()
    return output

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = ktn.loc[:,'symmetrized'].to_numpy()
    else:
        output = ktn.loc[indices,'symmetrized'].to_numpy()
    return output

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_microstate_name_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_component_index_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_basin_index_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_symmetrized_from_network(ktn, indices='all'):

    return ktn['symmetrized'].isin([True]).all()

def get_weight_from_network(ktn, indices='all'):

    return ktn['weight'].sum()

def get_temperature_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_time_step_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_microstates_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_transitions_from_network(ktn, indices='all'):

    return ktn.shape[0]

def get_n_components_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_n_basins_from_network(ktn, indices='all'):

    raise NotImplementedError("This method does not apply for this KTN form.")

def get_form_from_network(ktn, indices='all'):

    return form_name

