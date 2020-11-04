import numpy as np
from .utils.nodes import digest_indices as _digest_node_indices
from .utils.edges import digest_indices as _digest_edge_indices
from .lib import network as libnetwork

def most_likely():
    pass

def most_weighted_nodes(network, indices='all', top=1):

    output=None

    indices=_digest_node_indices(network, indices=indices)

    weights = np.array([network.node[ii].weight for ii in indices])
    aux=np.argsort(weights)[-top:][::-1]
    output = [network.node[indices[ii]] for ii in aux]

    return output

def most_weighted_edges(network, indices='all', top=1):

    output=None

    indices=_digest_edge_indices(network, indices=indices)

    weights = np.array([network.node[ii].weight for ii in indices])
    aux=np.argsort(weights)[-top:][::-1]
    output = [network.edge[indices[ii]] for ii in aux]

    return output

def global_minimum(network):

    output = None
    weights = np.array([node.weight for node in network.node])
    minimum_index = np.argmax(weights)
    output = network.node[minimum_index]
    return output

def local_minima(network):

    output = []

    for node in network.node:

        is_local_minimum=True
        for edge in node.edge.values():
            if node.weight<edge.end.weight:
                is_local_minimum=False
                break
        if is_local_minimum:
            output.append(node)

    weights = [node.weight for node in output]
    aux = np.argsort(weights)[::-1]
    output = [output[ii] for ii in aux]

    return output

def components(network, node_indices='all', selection=None, in_place=True):

    if network.Ts is None:
        network._update_Ts()

    n_components, component_index_per_node = libnetwork.components(network.Ts.start,
            network.Ts.ind, network.n_nodes, network.n_edges)

    if in_place:

        network.reset_components()

        for _ in range(n_components):
            network.add_component()

        for node in network.node:
            component_index=component_index_per_node[node.index]
            network.component[component_index].add_nodes(node)

    else:

        output=[]
        for _ in range(n_components):
            output.append(set())
        for node in network.node:
            component_index=component_index_per_node[node.index]
            output[component_index].add(node)

        return output

def density_of_states(network, n_bins=100):

    # density of microstates in the Free energy axe

    raise NotImplementedError
