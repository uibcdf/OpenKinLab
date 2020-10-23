names=["network", "microstate", "transition", "component", "basin"]

def singular(argument):

    if argument.endswith('s'):
        if argument=="networks":
            return "network"
        elif argument=="microstates":
            return "microstate"
        elif argument=="transitions":
            return "transition"
        elif argument=="components":
            return "component"
        elif argument=="basins":
            return "basin"

    return argument

