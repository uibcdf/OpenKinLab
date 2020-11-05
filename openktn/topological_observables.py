from .multitool import get, get_form, select
from .utils.targets import to_singular as singular_target, to_plural as plural_target
from .utils.free_energy import probability_to_free_energy
import numpy as np

def most_likely(ktn, target='microstate', names=None, top=1, output_free_energies=False):

    form = get_form(ktn)
    target = singular_target(target)

    output_elements = None
    output_values = None

    if target=='microstate':

        if name is None:
            names = get(ktn, target='microstate', microstate_name=True)

        probabilities = get(ktn, target='microstate', name=name, probability=True)
        aux=np.argsort(probabilities)[-top:][::-1]
        output_elements = np.take(names, aux)
        output_values = np.take(probabilities, aux)
        if output_free_energies:
            temperature = get(ktn, target='network', temperature=True)
            output_values = probability_to_free_energy(output_values, temperature)

    else:

        raise NotImplementedError

    return output_elements, output_values

def global_minimum(ktn, names=None, output_free_energies=False):

    output_microstate, output_value = most_likely(ktn, target='microstate', top=1, output_free_energies=output_free_energies)

    return output_microstate[0], output_value[0]

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
                if output_names:
                    output_microstates.append(name)
                else:
                    output_microstates.append(index)
                output_values.append(probability)

    elif form=='pandas.KineticTransitionNetwork':

        raise NotImplementedError

    if output_free_energies:

        temperature = get(ktn, selection='network', temperature=True)
        output_values = probability_to_free_energy(output_values, temperature)

    return output_microstates, output_values

