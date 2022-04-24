def get_form(ktn):

    try:
        return dict_is_form[type(ktn)]
    except:
        try:
            return dict_is_form[ktn]
        except:
            raise NotImplementedError("This KTN's form has not been implemented yet")

def KTN(form='pandas.KineticTransitionNetwork', temperature=0.0*unit.kelvin, time_step=0.0*unit.nanoseconds):

    tmp_ktn = dict_new[form](temperature=temperature, time_step=time_step)
    return tmp_ktn

def add_microstate(ktn, name=None):

    form = get_form(ktn)

    return dict_add_microstate[form](ktn, name=name)

def add_transition(ktn, origin, end, weight=1.0):

    form = get_form(ktn)

    return dict_add_transition[form](ktn, origin, end, weight=weight)

def microstate_index(ktn, name):

    form = get_form(ktn)

    return dict_microstate_index[form](ktn, name=name)

def transition_index(ktn, origin, end):

    form = get_form(ktn)

    return dict_microstate_index[form](ktn, origin, end)

def update_microstates_weights(ktn):

    form = get_form(ktn)

    return dict_update_microstates_weights[form](ktn)

def update_probabilities(ktn):

    form = get_form(ktn)

    return dict_update_probabilities[form](ktn)

def symmetrize(ktn):

    form = get_form(ktn)

    return dict_symmetrize[form](ktn)

def select(ktn, selection=None):
    raise NotImplementedError

def get(ktn, target='microstate', names=None, **kwargs):

    form = get_form(ktn)
    target = singular_target(target)
    attributes = [ key for key in kwargs.keys() if kwargs[key] ]

    results = []

    if form in ['pandas.KineticTransitionNetwork']:

        if names is None:
            indices='all'
        elif target=='microstate':
            indices=microstate_index(ktn, name=names)
        elif target=='transition':
            indices=transition_index(ktn, origin=names[:,0], end=names[:,1])

        for attribute in attributes:
            result = dict_get[form][target][attribute](ktn, indices=indices)
            results.append(result)

    else:

        for attribute in attributes:
            result = dict_get[form][target][attribute](ktn, names=names)
            results.append(result)

    if len(results)==1:
        return results[0]
    else:
        return results

def info(ktn, target='network', selection='all', output='dataframe'):

    if output=='dataframe':

        from pandas import DataFrame as df
        form = get_form(ktn)
        target = singular_target(target)

        if target=='microstate':

            if get(ktn, target='network', symmetrized=True):

                index, name, weight, probability, degree, component_name, basin_name = get(ktn, target=target,
                    microstate_index=True, microstate_name=True, weight=True, probability=True, degree=True,
                    component_name=True, basin_name=True)

                tmp_df = df({'index':index, 'name':name, 'weight':weight, 'probability':probability,
                            'degree':degree, 'component':component_name, 'basin':basin_name})

            else:

                index, name, weight, probability, out_degree, in_degree, component_name, basin_name = get(ktn, target=target,
                    microstate_index=True, microstate_name=True, weight=True, probability=True, out_degree=True, in_degree=True,
                    component_name=True, basin_name=True)

                tmp_df = df({'index':index, 'name':name, 'weight':weight, 'probability':probability,
                    'out_degree':out_degree, 'in_degree':in_degree, 'component':component_name,
                    'basin':basin_name})

            n_components, n_basins = get(ktn, target='network', n_components=True, n_basins=True)
            if n_components==0: tmp_df.drop(columns=['component'], inplace=True)
            if n_basins==0: tmp_df.drop(columns=['basin'], inplace=True)

            return tmp_df.style.hide_index()

        elif target=='transition':

            index, origin, end, weight, probability, symmetrized = get(ktn, target=target,
                    transition_index=True, origin_name=True, end_name=True,
                    transition_weight=True, transition_probability=True, symmetrized=True)

            tmp_df = df({'index':index, 'origin':origin, 'end':end, 'weight':weight,
                'probability':probability, 'symmetrized':symmetrized})

            return tmp_df.style.hide_index()

        elif target=='component':

            raise NotImplementedError

        elif target=='basin':

            raise NotImplementedError

        elif target=='network':

            form, n_microstates, n_transitions, n_components, n_basins, weight, symmetrized, temperature, time_step = get(ktn, target=target,
                    form=True, n_microstates=True, n_transitions=True, n_components=True, n_basins=True,
                    weight=True, symmetrized=True, temperature=True, time_step=True)

            tmp_df = df({'form':form, 'n_microstates':n_microstates, 'n_transitions':n_transitions, 'n_components':n_components,
                         'n_basins':n_basins, 'weight':weight, 'symmetrized':symmetrized,
                         'temperature':temperature, 'time_step':time_step}, index=[0])

            if n_components==0: tmp_df.drop(columns=['n_components'], inplace=True)
            if n_basins==0: tmp_df.drop(columns=['n_basins'], inplace=True)

            return tmp_df.style.hide_index()

        else:

            raise ValueError('"target" needs one of the following strings: "network", "microstate",\
                             "transition", "component", "basin"')

