from .multitool import get, get_form, select
from .utils.targets import to_singular as singular_target, to_plural as plural_target
from .utils.free_energy import probability_to_free_energy
import numpy as np

def most_likely(ktn, target='microstate', selection='all', top=1, output_names=False, output_free_energies=False):

    form = get_form(ktn)
    target = singular_target(target)

    output_elements = None
    output_values = None

    if target=='microstate':

        if top is 'all':
            top = get(ktn, target='network', n_microstates=True)

        indices = select(ktn, target='microstate', selection=selection)

        if form=='networkx.DiGraph':

            probabilities = get(ktn, target='microstate', indices=indices, probability=True)
            aux=np.argsort(probabilities)[-top:][::-1]
            output_elements = np.take(indices, aux)
            output_values = np.take(probabilities, aux)
            if output_names:
                output_elements = get(ktn, target='microstate', indices=output_elements, name=True)
            if output_free_energies:
                output_values = probability_to_free_energy(output_values, ktn.graph['temperature'])

        else:

            raise NotImplementedError

    return output_elements, output_values

def global_minimum(ktn, selection='all', output_names=False, output_free_energies=False):

    output_microstate, output_value = most_likely(ktn, target='microstate', selection=selection, top=1,
            output_names=output_names, output_free_energies=output_free_energies)

    return output_microstate, output_value

def local_minima(ktn, selection='all', output_names=False, output_free_energies=True):

    form = get_form(ktn)
    indices=select(ktn, target='microstate', selection=selection)
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
                if output_names:
                    output_microstates.append(name)
                else:
                    output_microstates.append(index)
                output_values.append(probability)
    else:

        raise NotImplementedError

    if output_free_energies:

        temperature = get(ktn, selection='network', temperature=True)
        output_values = probability_to_free_energy(output_values, temperature)

    return output_microstates, output_values
