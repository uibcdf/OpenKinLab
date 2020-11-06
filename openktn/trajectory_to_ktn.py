def series_to_ktn(series, temperature=None, time_step=None, to_form='pandas.KineticTransitionNetwork'):

    from openktn import KTN, add_transition, update_microstates_weights, update_probabilities

    ktn = KTN(to_form, temperature=temperature, time_step=time_step)

    if len(series[0])>1:

        for aa in series:
            for origin, end in zip(aa[:-1],aa[1:]):
                add_transition(ktn, origin, end, weight=1.0)

    else:

        for origin, end in zip(series[:-1],series[1:]):
            add_transition(ktn, origin, end, weight=1.0)

    update_microstates_weights(ktn)
    update_probabilities(ktn)

    return ktn

