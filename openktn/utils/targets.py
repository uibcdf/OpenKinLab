names=["network", "microstate", "transition", "component", "basin"]

singular_to_plural={
        "network" : "networks",
        "microstate" : "microstates",
        "transition" : "transitions",
        "component" : "components",
        "basin" : "basins"}

plural_to_singular = {value:key for key,value in singular_to_plural.items()}

def to_singular(target):

    output = target
    if target in plural_to_singular:
        output = plural_to_singular[target]

    return output

def to_plural(target):

    output = target
    if target in singular_to_plural:
        output = singular_to_plural[target]

    return output



