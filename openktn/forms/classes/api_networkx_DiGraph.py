from os.path import basename as _basename
from networkx import DiGraph as _networkx_DiGraph
from simtk.unit import kelvin, nanoseconds
from openKTN.native.network import attributes as network_attributes
from openKTN.native.microstate import attributes as microstate_attributes
from openKTN.native.transition import attributes as transition_attributes

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _networkx_DiGraph : form_name,
    'networkx.DiGraph' : form_name
}

info=["",""]

# Multitool

def new_empty_network(time_step=0.0*nanoseconds, temperature=0.0*kelvin):

    from networkx import set_node_attributes, set_edge_attributes

    item = _networkx_DiGraph()

    for attribute, value in microstate_attributes.item():
        item.graph[attribute]=value

    for attribute, value in microstate_attributes.item():
        set_node_attributes(item, value, attribute)

    for attribute, value in transition_attributes.item():
        set_edge_attributes(item, value, attribute)

    item.graph['time_step']=time_step.in_units_of(nanoseconds)
    item.graph['temperature']=time_step.in_units_of(kelvin)

def add_microstate(item, name):

    item.add_node(name, **microstate_attributes)

def add_transition(item, origin, end, weight=0.0)

    transition_attributes['weight']=weight

    item.add_edge(origin, end, **transition_attributes)

# Convert

# Get

## from network

def get_temperature_from_network(item, indices='all'):

    from simtk.unit import kelvin

    output = None
    if 'temperature' in item.graph:
        output = item.graph['temperature']
        output = output.in_units_of(kelvin)
    else:
        output = None

def get_time_step_from_network(item, indices='all'):

    from simtk.unit import nanoseconds

    output = None
    if 'time_step' in item.graph:
        output = item.graph['time_step']
        output = output.in_units_of(nanoseconds)
    else:
        output = None

    return output

def get_n_microstates_from_network(item, indices='all'):

    return item.number_of_nodes()

def get_n_transitions_from_network(item, indices='all'):

    return item.number_of_edges()

def get_form_from_network(item, indices='all'):

    return form_name

