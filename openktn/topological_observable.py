import numpy as np
from .utils.nodes import digest_indices as _digest_node_indices
from .utils.edges import digest_indices as _digest_edge_indices

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

def components(network):

    pass
