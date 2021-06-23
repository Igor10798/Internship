import simulation as sim
import pickle

#data to save
p_conn_dead = np.array([])
p_conn_constant = np.array([])
p_conn_exploded = np.array([])

#variables for loops
set_weights = range(1, 100)
p_conn = range(.003, .103, .001)

for w in set_weights:
    for p in p_conn:
        nest.ResetKernel()
        input_curr, neuron_pop, spikeDet = sim.create_network(w, p) #running simulation
        nest.Simulate(time)
        p_conn_dead, p_conn_constant, p_conn_exploded = sim.label_net_stacked_area(spikeDet, p, p_conn_dead, p_conn_constant, p_conn_exploded)
