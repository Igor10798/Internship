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

data_backup =  [md.DataBackup(sim.time) for i in range(1, int(sim.time) + 1)]


#variables for loops
set_weights = np.arange(1, 81, 40)
p_conn = np.arange(1, 121, 30)
#collecting data
for w in set_weights:
    w = float(w)
    for p in p_conn:
        p = p / 1000
        nest.ResetKernel()
        #running simulation
        input_curr, neuron_pop, spikeDet = sim.create_network(w, p)
        nest.Simulate(sim.time)
        #labelling data in base of output
        p_conn_dead, p_conn_constant, p_conn_exploded = sim.label_net_stacked_area(spikeDet, p, p_conn_dead, p_conn_constant, p_conn_exploded)
        p = p * 1000
        mask = set_weights < w
        index = int((np.amax(set_weights[mask]) * 100) + p ) - 1 if set_weights[mask].size > 0 else int(p) - 1
        data_backup[index].dict["dead"] = p_conn_dead
        data_backup[index].dict["constant"] = p_conn_constant
        data_backup[index].dict["exploded"] = p_conn_exploded
        #slicing time array in order to fit the data
        dead_len = data_backup[index].dict["dead"].size
        constant_len = data_backup[index].dict["constant"].size
        exploded_len = data_backup[index].dict["exploded"].size

        data_backup[index].dict["time_dead"][:dead_len]
        data_backup[index].dict["time_constant"][:constant_len]
        data_backup[index].dict["time_exploded"][:exploded_len]
    #data to save
    if p_conn_dead.size != 0:
        dead_prop.y.append(np.amax(p_conn_dead))
        dead_prop.x.append(w)
    if p_conn_constant.size != 0:
        constant_prop.y.append(np.amax(p_conn_constant))
        constant_prop.x.append(w)
    if p_conn_exploded.size != 0:
        exploded_prop.y.append(np.amax(p_conn_exploded))
        exploded_prop.x.append(w)


path = "offline_analysis/"
with open("{}chart.pkl".format(path), "wb") as f:
    data = data_chart
    pickle.dump(data, f)

# with open("{}backup.pkl".format(path), "wb") as b:
#     data = data_backup
#     pickle.dump(data, b)