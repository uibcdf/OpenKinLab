
def complementary_indices(item, indices):

    from numpy import array,ones
    from numpy import where
    from openKTN import get

    n_microstates = get(item, target='network', n_microstates=True)

    mask = ones(n_atoms,dtype=bool)
    mask[indices]=False
    return array(list(where(mask)[0]))

