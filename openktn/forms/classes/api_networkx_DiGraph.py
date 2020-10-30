from os.path import basename as _basename
from networkx import DiGraph as _networkx_DiGraph
from simtk.unit import kelvin, nanoseconds
from openktn.native.network import attributes as network_attributes
from openktn.native.microstate import attributes as microstate_attributes
from openktn.native.transition import attributes as transition_attributes
import numpy as np
import networkx as nx

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _networkx_DiGraph : form_name,
    'networkx.DiGraph' : form_name
}

info=["",""]

# Multitool

def new(n_microstates=0, time_step=None, temperature=None):

    from networkx import set_node_attributes, set_edge_attributes

    ktn = _networkx_DiGraph()

    for attribute, value in network_attributes.items():
        ktn.graph[attribute]=value

    for attribute, value in microstate_attributes.items():
        set_node_attributes(ktn, value, attribute)

    for attribute, value in transition_attributes.items():
        set_edge_attributes(ktn, value, attribute)

    aux = time_step.in_units_of(nanoseconds)
    aux._value = np.round(aux._value, 6)
    ktn.graph['time_step']=aux

    aux=temperature.in_units_of(kelvin)
    aux._value = np.round(aux._value, 3)
    ktn.graph['temperature']=aux

    ktn.__setattr__('index_to_name',[])
    ktn.__setattr__('index_to_origin_end',[])

    return ktn

def add_microstate(ktn, name=None, index=None):

    n_nodes = ktn.number_of_nodes()

    if name is None:
        if index is None:
            microstate_attributes['index']=n_nodes
            microstate_attributes['name']=n_nodes
            ktn.add_node(n_nodes, **microstate_attributes)
            ktn.index_to_name.append(n_nodes)
        else:
            for ii in range(n_nodes, index):
                microstate_attributes['index']=ii
                microstate_attributes['name']=ii
                ktn.add_node(ii, **microstate_attributes)
                ktn.index_to_name.append(ii)
    else:

        microstate_attributes['index']=n_nodes
        microstate_attributes['name']=name
        ktn.add_node(name, **microstate_attributes)
        ktn.index_to_name.append(name)

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    if origin_index:
        origin = get_microstate_name_from_microstate(ktn, indices=[origin])[0]
    else:
        if not microstate_in_ktn(ktn, origin):
            add_microstate(ktn, origin)

    if end_index:
        end = get_microstate_name_from_microstate(ktn, indices=[end])[0]
    else:
        if not microstate_in_ktn(ktn, end):
            add_microstate(ktn, end)

    if not transition_in_ktn(ktn, origin, end):

        index = ktn.number_of_edges()
        transition_attributes['index']=index
        transition_attributes['weight']=weight
        ktn.add_edge(origin, end, **transition_attributes)
        ktn.nodes[origin]['weight']+=weight
        ktn.graph['weight']+=weight
        ktn.index_to_origin_end.append([origin,end])

    else:

        ktn[origin][end]['weight']+=weight
        ktn.nodes[origin]['weight']+=weight
        ktn.graph['weight']+=weight

def microstate_in_ktn(ktn, name):

    return (name in ktn.nodes)

def transition_in_ktn(ktn, origin, end, origin_index=False, end_index=False):

    if origin_index:
        origin = get_microstate_name_from_microstate(ktn, indices=origin)

    if end_index:
        end = get_microstate_name_from_microstate(ktn, indices=end)

    return ([origin, end] in ktn.edges)

def update_weights(ktn):

    ktn.graph['weight']=0.0
    nx.set_node_attributes(ktn, 0.0, 'weight')
    for origin, end, weight in ktn.edges(data='weight'):
        ktn.nodes[origin]['weight']+=weight
        ktn.graph['weight']+=weight

def update_probabilities(ktn):

    nx.set_node_attributes(ktn, 0.0, 'probability')
    nx.set_edge_attributes(ktn, 0.0, 'probability')

    weight_ktn=ktn.graph['weight']
    for origin, weight_node in ktn.nodes(data='weight'):
        ktn.nodes[origin]['probability']=weight_node/weight_ktn
        for end, transition_attributes in ktn[origin].items():
            transition_attributes['probability']=transition_attributes['weight']/weight_node

def symmetrize(ktn):

    ktn.edges(data='symmetrized', default=False)

    for origin, end, symmetrized in ktn.edges(data='symmetrized'):
        if not symmetrized:
            if not transition_in_ktn(ktn, end, origin):
                add_transition(ktn, end, origin, weight=0.0)
            weight = 0.5*(ktn[origin][end]['weight']+ktn[end][origin]['weight'])
            ktn[origin][end]['weight']=weight
            ktn[end][origin]['weight']=weight
            ktn[origin][end]['symmetrized']=True
            ktn[end][origin]['symmetrized']=True

    update_weights(ktn)
    update_probabilities(ktn)

    ktn.graph['symmetrized']=True

def select(ktn, selection):

    raise NotImplementedError

# Convert

# Get

## Aux

def microstate_index_to_attribute(ktn, attr, microstate_index):

    microstate_name = ktn.index_to_name[microstate_index]
    output = ktn.nodes(attr)[microstate_name]
    return output

microstate_index_to_attribute_vect = np.vectorize(microstate_index_to_attribute, excluded=[0,1])

def transition_index_to_attribute(ktn, attr, transition_index):

    origin,end = ktn.index_to_origin_end[transition_index]
    output = ktn.edges(attr)[origin,end]
    return output

transition_index_to_attribute_vect = np.vectorize(transition_index_to_attribute, excluded=[0,1])

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
        output = get_microstate_index_from_network(ktn)
    else:
        output = indices

    return output

def get_microstate_name_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = get_microstate_name_from_network(ktn)
    else:
        output = np.array([ktn.index_to_name[ii] for ii in indices], dtype=object)

    return output

def get_microstate_weight_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':

        output = np.array([ktn.nodes[ii]['weight'] for ii in ktn.index_to_name])

    else:

        output = microstate_index_to_attribute_vect(ktn, 'weight', indices)

    return output

def get_microstate_probability_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = np.array([ktn.nodes[ii]['probability'] for ii in ktn.index_to_name])
    else:
        output = microstate_index_to_attribute_vect(ktn, 'probability', indices)

    return output

def get_microstate_degree_from_microstate(ktn, indices='all'):

    return get_microstate_out_degree_from_microstate(ktn, indices=indices)

def get_microstate_out_degree_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        names = get_microstate_name_from_network(ktn)
        output = np.array(ktn.out_degree(names))[:,1]
    else:
        names = get_microstate_name_from_microstate(ktn, indices)
        output = np.array(ktn.out_degree(names))[:,1]

    return output

def get_microstate_in_degree_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        names = get_microstate_name_from_network(ktn)
        output = np.array(ktn.in_degree(names))[:,1]
    else:
        names = get_microstate_name_from_microstate(ktn, indices)
        output = np.array(ktn.in_degree(names))[:,1]

    return output

def get_component_index_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = np.array([ktn.nodes[ii]['component_index'] for ii in ktn.index_to_name])
    else:
        output = microstate_index_to_attribute_vect(ktn, 'component_index', indices)

    return output

def get_basin_index_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':
        output = np.array([ktn.nodes[ii]['basin_index'] for ii in ktn.index_to_name])
    else:
        output = microstate_index_to_attribute_vect(ktn, 'basin_index', indices)

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
        output = [ii[0] for ii in ktn.index_to_origin_end]
    else:
        output = [ktn.index_to_origin_end[ii][0] for ii in indices]
    output = [ktn.nodes[ii]['index'] for ii in output]
    return output

def get_transition_end_index_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = [ii[1] for ii in ktn.index_to_origin_end]
    else:
        output = [ktn.index_to_origin_end[ii][1] for ii in indices]
    output = [ktn.nodes[ii]['index'] for ii in output]
    return output

def get_transition_weight_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = np.array([ktn[ii][jj]['weight'] for ii,jj in ktn.index_to_origin_end])
    else:
        output = transition_index_to_attributes_vect(indices, 'weight')
    return output

def get_transition_probability_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = np.array([ktn[ii][jj]['probability'] for ii,jj in ktn.index_to_origin_end])
    else:
        output = transition_index_to_attributes_vect(indices, 'probability')
    return output

def get_transition_symmetrized_from_transition(ktn, indices='all'):

    output = None
    if indices is 'all':
        output = np.array([ktn[ii][jj]['symmetrized'] for ii,jj in ktn.index_to_origin_end])
    else:
        output = transition_index_to_attributes_vect(indices, 'symmetrized')
    return output

## from network

def get_microstate_index_from_network(ktn, indices='all'):

    n_microstates=get_n_microstates_from_network(ktn)
    return np.arange(n_microstates)

def get_microstate_name_from_network(ktn, indices='all'):

    return np.array(ktn.index_to_name, dtype=object)

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

    return False not in nx.get_edge_attributes(ktn, 'symmetrized').values()

def get_weight_from_network(ktn, indices='all'):

    return ktn.graph['weight']

def get_temperature_from_network(ktn, indices='all'):

    return ktn.graph['temperature']

def get_time_step_from_network(ktn, indices='all'):

    from simtk.unit import nanoseconds

    output = None
    if 'time_step' in ktn.graph:
        output = ktn.graph['time_step']
        output = output.in_units_of(nanoseconds)
    else:
        output = None

    return output

def get_n_microstates_from_network(ktn, indices='all'):

    return ktn.number_of_nodes()

def get_n_transitions_from_network(ktn, indices='all'):

    return ktn.number_of_edges()

def get_n_components_from_network(ktn, indices='all'):

    output=None
    try:
        aux = np.unique(get_component_index_from_microstate(ktn, indices='all'))
        output = aux.shape[0]
    except:
        aux = set(get_component_index_from_microstate(ktn, indices='all'))
        output = len(aux)
    if None in aux:
        output -= 1
    return output

def get_n_basins_from_network(ktn, indices='all'):

    output=None
    try:
        aux = np.unique(get_basin_index_from_microstate(ktn, indices='all'))
        output = aux.shape[0]
    except:
        aux = set(get_basin_index_from_microstate(ktn, indices='all'))
        output = len(aux)
    if None in aux:
        output -= 1
    return output

def get_form_from_network(ktn, indices='all'):

    return form_name

