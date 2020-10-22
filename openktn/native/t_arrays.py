import numpy as np

class TArrays():

    def __init__(self, ktn):

        n_microstates = ktn.n_microstates
        n_transitions = ktn.n_transitions

        self.ind=np.empty(n_transitions, dtype=int)
        self.start=np.empty(n_microstates+1, dtype=int)
        self.pi=np.empty(n_microstates, dtype=float)
        self.pij=np.empty(n_transitions, dtype=float)

        kk=0

        for ii in range(n_microstates):
            microstate = ktn.node[ii]
            self.pi[ii] = microstate.probability
            self.start[ii]=kk
            for jj, transition in microstate.transition.items():
                self.ind[kk]=jj+1
                self.pij[kk]=transition.probability
                kk+=1

        self.start[n_transitions]=kk

