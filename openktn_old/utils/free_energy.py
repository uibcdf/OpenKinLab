import numpy as np
import simtk.unit as unit

kB=unit.BOLTZMANN_CONSTANT_kB * unit.AVOGADRO_CONSTANT_NA

def probability_to_free_energy(probability, temperature):

    kBT=(kB*temperature).in_units_of(unit.kilocalories_per_mole)

    return -kBT*np.log(probability)
