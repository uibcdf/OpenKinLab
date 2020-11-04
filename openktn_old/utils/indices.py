def intersection_indices(indices1,indices2):

    from numpy import intersect1d

    output_indices = intersect1d(indices1, indices2, assume_unique=True)

    return output_indices

