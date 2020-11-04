#from .lib import landscapes as lib_landscapes
from .lib import network as lib_network
import numpy as np
import simtk.unit as unit

def bottom_up_1D(network):

    if not network.Ts:
        network.update_Ts()

    if network.temperature is None:
        raise ValueError("A temperature value is needed in the network.")

    kB=unit.BOLTZMANN_CONSTANT_kB * unit.AVOGADRO_CONSTANT_NA
    kBT=(kB*network.temperature).in_units_of(unit.kilocalories_per_mole)

    coord_x = np.zeros(network.n_nodes)
    coord_y = -kBT*np.log(network.Ts.pn)

    order = lib_network.sorted_nodes_by_probability(network.Ts.pn, network.n_nodes)

    basin=[]
    basin_lim=[]
    basin_coin=[]
    belongs_to = np.zeros(network.n_nodes, dtype=int)
    n_basins=0
    increment=[-1,1]

    visited = np.zeros(network.n_nodes, dtype=bool)

    for ii in order:

        connection=[]

        for jj in network.node[ii].edge:
            if visited[jj]:
                connection.append(belongs_to[jj])

        connection=np.unique(connection)

        if connection.shape[0]==0:

            belongs_to[ii]=n_basins
            basin.append([ii])
            basin_lim.append([0,0])
            basin_coin.append(True)
            n_basins+=1

        else:

            min_basin=connection[0]
            basin[min_basin].append(ii)
            belongs_to[ii]=min_basin

            coin=basin_coin[min_basin]
            int_coin=int(coin)
            basin_coin[min_basin]= not coin
            basin_lim[min_basin][int_coin]+=increment[int_coin]
            coord_x[ii]=basin_lim[min_basin][int_coin]

            for basin_to_merge in connection[1:]:

                nodes_to_merge = basin.pop(basin_to_merge)
                lims = basin_lim.pop(basin_to_merge)
                _ = basin_coin.pop(basin_to_merge)

                coin=basin_coin[min_basin]
                int_coin=int(coin)
                int_no_coin=int(not coin)
                basin_coin[min_basin]= not coin

                shift = basin_lim[min_basin][int_coin] - lims[int_no_coin] + int_coin
                basin_lim[min_basin][int_coin]+=increment[int_coin]*len(nodes_to_merge)
                coord_x[nodes_to_merge]+=shift
                belongs_to[nodes_to_merge]=min_basin
                basin[min_basin].extend(nodes_to_merge)
                for nodes_to_relabel in basin[basin_to_merge:]:
                    belong_to[nodes_to_relabel]-=1
                n_basins-=1

        visited[ii]=True

    return coord_x, coord_y

