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

def new_empty_ktn(time_step=0.0*nanoseconds, temperature=0.0*kelvin):

    from networkx import set_node_attributes, set_edge_attributes

    ktn = _networkx_DiGraph()

    for attribute, value in network_attributes.items():
        ktn.graph[attribute]=value

    for attribute, value in microstate_attributes.items():
        set_node_attributes(ktn, value, attribute)

    for attribute, value in transition_attributes.items():
        set_edge_attributes(ktn, value, attribute)

    ktn.graph['time_step']=time_step.in_units_of(nanoseconds)
    ktn.graph['temperature']=temperature.in_units_of(kelvin)

    ktn.__setattr__('index_to_name',[])

    return ktn

def add_microstate(ktn, name=None):

    index=ktn.number_of_nodes()
    microstate_attributes['index']=index

    if name is None:
        name=index

    microstate_attributes['name']=name

    ktn.add_node(name, **microstate_attributes)
    ktn.index_to_name.append(name)

def add_transition(ktn, origin, end, weight=0.0, origin_index=False, end_index=False):

    index = ktn.number_of_edges()

    transition_attributes['index']=index
    transition_attributes['weight']=weight

    if origin_index:
        origin = get_microstate_name_from_microstate(ktn, indices=origin)

    if end_index:
        end = get_microstate_name_from_microstate(ktn, indices=end)

    ktn.add_edge(origin, end, **transition_attributes)

# Convert

# Get

## Aux

def microstate_index_to_attribute(ktn, attr, microstate_index):

    microstate_name = ktn.index_to_name[microstate_index]
    output = ktn.nodes(attr)[microstate_name]
    return output

microstate_index_to_attribute_vect = np.vectorize(microstate_index_to_attribute, excluded=[0,1])

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
        output = np.take(ktn.index_to_name,indices)

    return output

def get_microstate_weight_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':

        output = np.array(list(nx.get_node_attributes(ktn, 'weight').values()))

    else:

        output = microstate_index_to_attribute_vect(ktn, 'weight', indices)

    return output

def get_microstate_probability_from_microstate(ktn, indices='all'):

    output = None

    if indices is 'all':

        output = np.array(list(nx.get_node_attributes(ktn, 'probability').values()))

    else:

        output = microstate_index_to_attribute_vect(ktn, 'probability', indices)

    return output


## from network

def get_microstate_index_from_network(ktn, indices='all'):

    n_microstates=get_n_microstates_from_network(ktn)
    return np.arange(n_microstates)

def get_microstate_name_from_network(ktn, indices='all'):

    return np.array(ktn.index_to_name)

def get_temperature_from_network(ktn, indices='all'):

    from simtk.unit import kelvin

    output = None
    if 'temperature' in ktn.graph:
        output = ktn.graph['temperature']
        output = output.in_units_of(kelvin)
    else:
        output = None

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

def get_form_from_network(ktn, indices='all'):

    return form_name

