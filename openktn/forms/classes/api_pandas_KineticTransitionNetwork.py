from os.path import basename as _basename
from openktn.foreign import Pandas_KineticTransitionNetwork
from simtk.unit import kelvin, nanoseconds
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    Pandas_KineticTransitionNetwork : form_name,
    'pandas.KineticTransitionNetwork' : form_name
}

info=["",""]

# Multitool

def new(temperature=None, time_step=None):

    ktn = Pandas_KineticTransitionNetwork(temperature=temperature, time_step=time_step)

    return ktn

def add_microstate(ktn, name=None):

    n_microstates=ktn.microstates.shape[0]

    if name is None:
        name = n_microstates

    ktn.microstates.at[n_microstates, 'name']=name
    ktn.microstates.at[n_microstates, 'weight']=0.0
    ktn.microstates.at[n_microstates, 'probability']=0.0

def add_transition(ktn, origin, end, weight=0.0):

    index_origin = np.nonzero(ktn.microstates.name.to_numpy()==origin)[0]
    with_end = np.any(ktn.microstates.name.to_numpy()==end)

    new=False

    if not index_origin.size:
        index_origin=ktn.microstates.shape[0]
        add_microstate(ktn, origin)
        new=True
    else:
        index_origin=index_origin[0]

    if not with_end:
        add_microstate(ktn, end)
        new=True

    if new:
        n_transitions=ktn.transitions.shape[0]
        ktn.transitions.at[n_transitions, 'origin']=origin
        ktn.transitions.at[n_transitions, 'end']=end
        ktn.transitions.at[n_transitions, 'weight']=weight
        ktn.transitions.at[n_transitions, 'probability']=0.0
        ktn.transitions.at[n_transitions, 'symmetrized']=False
    else:
        mask = (ktn.transitions.origin.to_numpy()==origin)*(ktn.transitions.end.to_numpy()==end)
        index = np.nonzero(mask)[0]
        if index.size:
            ktn.transitions.at[index[0],'weight']+=weight
        else:
            n_transitions=ktn.transitions.shape[0]
            ktn.transitions.at[n_transitions, 'origin']=origin
            ktn.transitions.at[n_transitions, 'end']=end
            ktn.transitions.at[n_transitions, 'weight']=weight
            ktn.transitions.at[n_transitions, 'probability']=0.0
            ktn.transitions.at[n_transitions, 'symmetrized']=False

    ktn.microstates.at[index_origin, 'weight']+=weight

def update_probabilities(ktn):

    ktn.transitions['probability']=ktn.transitions['weight']/ktn.transitions.groupby(by='origin')['weight'].transform('sum')
    ktn.microstates['probability']=ktn.microstates['weight']/ktn.microstates['weight'].sum()

#def symmetrize(ktn):
#
#    api_transitions.symmetrize(ktn.transitions)
#    update_probabilities(ktn)
#
#def select(ktn, selection):
#
#    raise NotImplementedError
#
## Convert
#
## Get
#
### Aux
#
### from microstate
#
#def get_index_from_microstate(ktn, indices='all'):
#
#    return get_microstate_index_from_microstate(ktn, indices=indices)
#
#def get_name_from_microstate(ktn, indices='all'):
#
#    return get_microstate_name_from_microstate(ktn, indices=indices)
#
#def get_weight_from_microstate(ktn, indices='all'):
#
#    return get_microstate_weight_from_microstate(ktn, indices=indices)
#
#def get_probability_from_microstate(ktn, indices='all'):
#
#    return get_microstate_probability_from_microstate(ktn, indices=indices)
#
#def get_degree_from_microstate(ktn, indices='all'):
#
#    return get_microstate_out_degree_from_microstate(ktn, indices=indices)
#
#def get_out_degree_from_microstate(ktn, indices='all'):
#
#    return get_microstate_out_degree_from_microstate(ktn, indices=indices)
#
#def get_in_degree_from_microstate(ktn, indices='all'):
#
#    return get_microstate_in_degree_from_microstate(ktn, indices=indices)
#
#def get_microstate_index_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_microstate_index_from_microstate(ktn.microstates, indices=indices)
#
#def get_microstate_name_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_microstate_name_from_microstate(ktn.microstates, indices=indices)
#
#def get_microstate_weight_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_microstate_weight_from_microstate(ktn.microstates, indices=indices)
#
#def get_microstate_probability_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_microstate_probability_from_microstate(ktn.microstates, indices=indices)
#
#def get_microstate_degree_from_microstate(ktn, indices='all'):
#
#    return get_microstate_out_degree_from_microstate(ktn, indices=indices)
#
#def get_microstate_out_degree_from_microstate(ktn, indices='all'):
#
#    if indices is 'all':
#        output=np.zeros(ktn.microstates.shape[0], dtype=int)
#        aux=ktn.transitions.groupby(by='origin_index')['end_index'].count()
#        output[aux.keys()]=aux
#    else:
#        output = api_transitions.get_microstate_out_degree_from_microstate(ktn.transitions,indices)
#
#    return output
#
#def get_microstate_in_degree_from_microstate(ktn, indices='all'):
#
#    if indices is 'all':
#        output=np.zeros(ktn.microstates.shape[0], dtype=int)
#        aux=ktn.transitions.groupby(by='end_index')['origin_index'].count()
#        output[aux.keys()]=aux
#    else:
#        output = api_transitions.get_microstate_in_degree_from_microstate(ktn.transitions,indices)
#
#    return output
#
#def get_component_index_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_component_index_from_microstate(ktn.microstates, indices=indices)
#
#def get_basin_index_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_basin_index_from_microstate(ktn.microstates, indices=indices)
#
#def get_n_microstates_from_microstate(ktn, indices='all'):
#
#    return api_microstates.get_n_microstates_from_microstate(ktn.microstates, indices=indices)
#
### from transition
#
#def get_index_from_transition(ktn, indices='all'):
#
#    return get_transition_index_from_transition(ktn, indices='all')
#
#def get_origin_index_from_transition(ktn, indices='all'):
#
#    return get_transition_origin_index_from_transition(ktn, indices='all')
#
#def get_end_index_from_transition(ktn, indices='all'):
#
#    return get_transition_end_index_from_transition(ktn, indices='all')
#
#def get_weight_from_transition(ktn, indices='all'):
#
#    return get_transition_weight_from_transition(ktn, indices='all')
#
#def get_probability_from_transition(ktn, indices='all'):
#
#    return get_transition_probability_from_transition(ktn, indices='all')
#
#def get_symmetrized_from_transition(ktn, indices='all'):
#
#    return get_transition_symmetrized_from_transition(ktn, indices='all')
#
#def get_transition_index_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_transition_index_from_transition(ktn.transitions, indices=indices)
#
#def get_transition_origin_index_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_origin_index_from_transition(ktn.transitions, indices=indices)
#
#def get_transition_end_index_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_end_index_from_transition(ktn.transitions, indices=indices)
#
#def get_transition_weight_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_transition_weight_from_transition(ktn.transitions, indices=indices)
#
#def get_transition_probability_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_transition_probability_from_transition(ktn.transitions, indices=indices)
#
#def get_transition_symmetrized_from_transition(ktn, indices='all'):
#
#    return api_transitions.get_transition_symmetrized_from_transition(ktn.transitions, indices=indices)
#
### from network
#
#def get_microstate_index_from_network(ktn, indices='all'):
#
#    return api_microstates.get_microstate_index_from_network(ktn.microstates)
#
#def get_microstate_name_from_network(ktn, indices='all'):
#
#    return api_microstates.get_microstate_name_from_network(ktn.microstates)
#
#def get_component_index_from_network(ktn, indices='all'):
#
#    return api_microstates.get_component_index_from_network(ktn.microstates)
#
#def get_basin_index_from_network(ktn, indices='all'):
#
#    return api_microstates.get_basin_index_from_network(ktn.microstates)
#
#def get_symmetrized_from_network(ktn, indices='all'):
#
#    return api_transitions.get_symmetrized_from_network(ktn.transitions)
#
#def get_weight_from_network(ktn, indices='all'):
#
#    return api_transitions.get_weight_from_network(ktn.transitions)
#
#def get_temperature_from_network(ktn, indices='all'):
#
#    return ktn.temperature
#
#def get_time_step_from_network(ktn, indices='all'):
#
#    return ktn.time_step
#
#def get_n_microstates_from_network(ktn, indices='all'):
#
#    return api_microstates.get_n_microstates_from_network(ktn.microstates)
#
#def get_n_transitions_from_network(ktn, indices='all'):
#
#    return api_transitions.get_n_transitions_from_network(ktn.transitions)
#
#def get_n_components_from_network(ktn, indices='all'):
#
#    return api_microstates.get_n_components_from_network(ktn.microstates)
#
#def get_n_basins_from_network(ktn, indices='all'):
#
#    return api_microstates.get_n_basins_from_network(ktn.microstates)
#
#def get_form_from_network(ktn, indices='all'):
#
#    return form_name
#
