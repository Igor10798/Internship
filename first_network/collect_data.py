import pickle
import numpy as np
import nest

import modules.simulation as sim
import modules.models as md

#array for online analysis
p_conn_dead = np.array([])
p_conn_constant = np.array([])
p_conn_exploded = np.array([])

#data to save
dead_prop = md.LineForChart()
constant_prop = md.LineForChart()
exploded_prop = md.LineForChart()
data_chart = {
    "dead": dead_prop,
    "constant": constant_prop,
    "exploded": exploded_prop
}

data_backup =  md.LineForChart()

#variables for loops
set_weights = np.logspace(0, 7, 8, base = 2.0)
p_conn = np.linspace(.03, .15, 8)
path = "offline_analysis/sim_pkl/"

def main():
    #collecting data
    for i, w in enumerate(set_weights):
        w = float(w)
        for j, p in enumerate(p_conn):
            nest.ResetKernel()
            sim.initKernel()
            #running simulation
            input_curr, neuron_pop, spikeDet = sim.create_network(w, p)
            nest.Simulate(sim.time)
            #labelling data in base of output
            spikes = sim.extract_spikes(spikeDet)
            with open(f"{path}{i}_{j}.pkl", "wb") as f:
                data = (w, p, spikes)
                pickle.dump(data, f)

if __name__ == "__main__":
    main()