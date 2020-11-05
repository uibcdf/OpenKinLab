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

    index_origin = _microstate_index(ktn, origin)
    index_end = _microstate_index(ktn, end)

    new=False

    if index_origin is None:
        add_microstate(ktn, origin)
        new=True

    if index_end is None:
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
        index = _transition_index(ktn, origin, end)
        if index is None:
            n_transitions=ktn.transitions.shape[0]
            ktn.transitions.at[n_transitions, 'origin']=origin
            ktn.transitions.at[n_transitions, 'end']=end
            ktn.transitions.at[n_transitions, 'weight']=weight
            ktn.transitions.at[n_transitions, 'probability']=0.0
            ktn.transitions.at[n_transitions, 'symmetrized']=False
        else:
            ktn.transitions.at[index,'weight']+=weight

def _microstate_index(ktn, name):

    mask = (ktn.microstates.name.to_numpy()==name)
    index = np.nonzero(mask)[0]
    if index.size:
        return index[0]
    else:
        return None

def _transition_index(ktn, origin, end):

    mask = (ktn.transitions.origin.to_numpy()==origin)*(ktn.transitions.end.to_numpy()==end)
    index = np.nonzero(mask)[0]
    if index.size:
        return index[0]
    else:
        return None

microstate_index = np.vectorize(_microstate_index, excluded=[0])
transition_index = np.vectorize(_transition_index, excluded=[0])

def update_microstates_weights(ktn):

    groups_weights = ktn.transitions.groupby(by='origin')['weight'].sum()
    ktn.microstates.weight = groups_weights[ktn.microstates.name].to_numpy()

def update_probabilities(ktn):

    ktn.transitions['probability']=ktn.transitions['weight']/ktn.transitions.groupby(by='origin')['weight'].transform('sum')
    ktn.microstates['probability']=ktn.microstates['weight']/ktn.microstates['weight'].sum()

def symmetrize(ktn):

    ktn.transitions['symmetrized']=False

    n_transitions = ktn.transitions.shape[0]

    for index in range(n_transitions):
        if not ktn.transitions.at[index,'symmetrized']:
            origin = ktn.transitions.at[index,'origin']
            end = ktn.transitions.at[index,'end']
            back_index = _transition_index(ktn, end, origin)
            if back_index:
                weight=0.5*(ktn.transitions.at[index,'weight']+ktn.transitions.at[back_index,'weight'])
                ktn.transitions.at[index,'weight']=weight
                ktn.transitions.at[back_index,'weight']=weight
            else:
                weight=0.5*ktn.transitions.at[index,'weight']
                ktn.transitions.at[index,'weight']=weight
                back_index=ktn.transitions.shape[0]
                ktn.transitions.at[back_index, 'origin']=end
                ktn.transitions.at[back_index, 'end']=origin
                ktn.transitions.at[back_index, 'weight']=weight
            ktn.transitions.at[index,'symmetrized']=True
            ktn.transitions.at[back_index,'symmetrized']=True

    update_microstates_weights(ktn)
    update_probabilities(ktn)

def select(ktn, selection):

    raise NotImplementedError

## Convert

## Get

### Aux

### from microstate

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

    if indices is 'all':
        return ktn.microstates.index.to_numpy()
    else:
        return indices

def get_microstate_name_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.name.to_numpy()
    else:
        return ktn.microstates.loc[indices,'name'].to_numpy()

def get_microstate_weight_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.weight.to_numpy()
    else:
        return ktn.microstates.loc[indices,'weight'].to_numpy()

def get_microstate_probability_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.probability.to_numpy()
    else:
        return ktn.microstates.loc[indices,'probability'].to_numpy()

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    if indices is 'all':
        aux=ktn.transitions.groupby(by='origin')['end'].count()
        return aux[ktn.microstates.name].to_numpy()
    else:
        names = get_microstate_name_from_microstate(ktn, indices=indices)
        aux=ktn.transitions.groupby(by='origin')['end'].count()
        return aux[names].to_numpy()

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    if indices is 'all':
        aux=ktn.transitions.groupby(by='end')['origin'].count()
        return aux[ktn.microstates.name].to_numpy()
    else:
        names = get_microstate_name_from_microstate(ktn, indices=indices)
        aux=ktn.transitions.groupby(by='end')['origin'].count()
        return aux[names].to_numpy()

def get_component_name_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.component.to_numpy()
    else:
        return ktn.microstates.loc[indices,'component'].to_numpy()

def get_basin_name_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.basin.to_numpy()
    else:
        return ktn.microstates.loc[indices,'basin'].to_numpy()

def get_n_microstates_from_microstate(ktn, indices='all'):

    if indices is 'all':
        return ktn.microstates.shape[0]
    else:
        return indices.shape[0]

## from transition

def get_index_from_transition(ktn, indices='all'):

    return get_transition_index_from_transition(ktn, indices='all')

def get_weight_from_transition(ktn, indices='all'):

    return get_transition_weight_from_transition(ktn, indices='all')

def get_probability_from_transition(ktn, indices='all'):

    return get_transition_probability_from_transition(ktn, indices='all')

def get_symmetrized_from_transition(ktn, indices='all'):

    return get_transition_symmetrized_from_transition(ktn, indices='all')

def get_transition_index_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.index.to_numpy()
    else:
        return indices

def get_origin_name_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.origin.to_numpy()
    else:
        return ktn.transitions.loc[indices, 'origin'].to_numpy()

def get_end_name_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.end.to_numpy()
    else:
        return ktn.transitions.loc[indices, 'end'].to_numpy()

def get_transition_weight_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.weight.to_numpy()
    else:
        return ktn.transitions.loc[indices, 'weight'].to_numpy()

def get_transition_probability_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.probability.to_numpy()
    else:
        return ktn.transitions.loc[indices, 'probability'].to_numpy()

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    if indices is 'all':
        return ktn.transitions.symmetrized.to_numpy()
    else:
        return ktn.transitions.loc[indices, 'symmetrized'].to_numpy()

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    return get_microstate_index_from_microstate(ktn, indices='all')

def get_microstate_name_from_network(ktn, indices='all'):

    return get_microstate_name_from_microstate(ktn, indices='all')

def get_component_index_from_network(ktn, indices='all'):

    return get_component_index_from_microstate(ktn, indices='all')

def get_basin_index_from_network(ktn, indices='all'):

    return get_component_index_from_microstate(ktn, indices='all')

def get_symmetrized_from_network(ktn, indices='all'):

    return (ktn.transitions['symmetrized'].to_numpy()==True).all()

def get_weight_from_network(ktn, indices='all'):

    return ktn.transitions['weight'].sum()

def get_temperature_from_network(ktn, indices='all'):

    return ktn.temperature

def get_time_step_from_network(ktn, indices='all'):

    return ktn.time_step

def get_n_microstates_from_network(ktn, indices='all'):

    return ktn.microstates.shape[0]

def get_n_transitions_from_network(ktn, indices='all'):

    return ktn.transitions.shape[0]

def get_n_components_from_network(ktn, indices='all'):

    return ktn.microstates.groupby('component').ngroups

def get_n_basins_from_network(ktn, indices='all'):

    return ktn.microstates.groupby('basin').ngroups

def get_form_from_network(ktn, indices='all'):

    return form_name

