from .multitool import get, get_form
from .utils.targets import singular as singular_target

def most_likely(ktn, target='microstate', selection=None, top=1, name=False):

    form = get_form(ktn)
    target = singular_target()

    output = None

    if target=='microstate':

        indices = select(ktn, target='microstate', selection=selection)

        if form=='networkx.DiGraph':

            weights = get(ktn, target='microstate', indices=indices, weight=True)
            aux=np.argsort(weights)[-top:][::-1]
            output_target = np.take(indices, aux)
            output_weight = np.take(weights, aux)
            output = [output_target, output_weigh]

    return output


