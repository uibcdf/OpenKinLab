import numpy as np

def digest_indices (ktn, indices):

    output = None

    if indices is 'all':
        output = np.arange(ktn.n_nodes, dtype=int)
    else:
        output = np.array(indices)

    return output

