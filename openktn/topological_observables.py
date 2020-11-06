from .multitool import get, get_form, select
from .utils.targets import to_singular as singular_target, to_plural as plural_target
from .utils.free_energy import probability_to_free_energy
import numpy as np

def most_likely(ktn, target='microstate', names=None, top=1, output='weight'):

    # output: 'weight', 'probability', 'free_energy'

    form = get_form(ktn)
    target = singular_target(target)

    output_elements = None
    output_values = None

    if form=='pandas.KineticTransitionNetwork':

        if target=='microstate':

            if names is None:
                serie=net.microstates.weight.nlargest(top, keep='all')
            else:
                serie=net.microstates[net.microstates.name.isin(names)].weight.nlargest(top, keep='all')

            output_elements = net.microstates.loc[serie.index,'name'].to_numpy()
            output_values = serie.to_numpy()

        elif target=='transition':

            if names is None:
                serie=net.transitions.probability.nlargest(top, keep='all')
            else:
                serie=net.microstates[net.microstates.name.isin(names)].weight.nlargest(top, keep='all')

            output_elements = net.microstates.loc[serie.index,'name'].to_numpy()
            output_values = serie.to_numpy()

        else:

            raise NotImplementedError

        if output=='probability':
            output_values = output_values/net.microstates.weight.sum()

        elif output=='free_energy':
            temperature = get(ktn, target='network', temperature=True)
            output_values = probability_to_free_energy(output_values/net.microstates.weight.sum(), temperature)

    else:
            raise NotImplementedError


    return output_elements, output_values

def global_minimum(ktn, names=None, output_free_energies=True):

    output_microstate, output_value = most_likely(ktn, target='microstate', top=1, output_free_energies=output_free_energies)

    if output_microstate.size==1:
        return output_microstate[0], output_value[0]
    else:
        return output_microstate, output_value


def local_minima(ktn, names=None, output_free_energies=True):

    form = get_form(ktn)
    output_microstates=[]
    output_values=[]

    if form=='networks.DiGraph':

        for index in indices:

            is_minimum = True
            name = ktn.index_to_name[index]
            probability = ktn.nodes(name)['probability']
            for ii in ktn.neighbors(name):
                if probability<ktn.nodes(ii)['probability']:
                    is_minimum=False
                    break
            if is_minimum:
                output_microstates.append(name)
                output_values.append(probability)

    elif form=='pandas.KineticTransitionNetwork':

        aux_serie=ktn.transitions.groupby(by='origin')['end'].apply(set)

        for microstate, neighbors in aux_serie.items():
            microstate_probability = ktn.microstates.probability[ktn.microstates.name.isin([microstate])].to_numpy()[0]
            neighbors_probability = ktn.microstates.probability[ktn.microstates.name.isin(neighbors)].to_numpy()
            is_minimum=(microstate_probability>=neighbors_probability).all()
            if is_minimum:
                output_microstates.append(microstate)
                output_values.append(microstate_probability)

    order=np.argsort(output_values)[::-1]
    output_microstates=np.array(output_microstates)[order]
    output_values=np.array(output_values)[order]

    if output_free_energies:

        temperature = get(ktn, target='network', temperature=True)
        output_values = probability_to_free_energy(output_values, temperature)

    return output_microstates, output_values

def components(ktn, names=None):

    form = get_form(ktn)
    output = []

    if form=='networks.Digraph':

        raise NotImplementedError

    elif form=='pandas.KineticTransitionNetwork':

        from pandas import isnull

        aux_dict=ktn.transitions.groupby(by='origin')['end'].apply(set)
        n_components=0

        while len(aux_dict):
            ii = aux_dict.keys()[0]
            ii_neighbors = aux_dict.pop(ii)
            ii_component = ktn.microstates.component[ktn.microstates.name.isin([ii])].to_numpy()[0]
            if isnull(ii_component):
                box = ii_neighbors
                in_component = box.union({ii})
                while len(box):
                    jj=box.pop()
                    in_component.add(jj)
                    jj_neighbors=aux_dict.pop(jj)
                    box.update(jj_neighbors-in_component)
                ktn.microstates.loc[ktn.microstates.name.isin(in_component),'component']=n_components
                output.append(in_component)
                n_components+=1

        groups_by_components = ktn.microstates.groupby(by='component')
        names_components = ktn.microstates.loc[ktn.microstates.groupby(by='component').weight.idxmax(),'name']
        for indices, name in zip(groups_by_components.groups.values(), names_components):
            ktn.microstates.at[indices,'component']=name

    return output
