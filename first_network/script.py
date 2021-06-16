import nest
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

def create_network(dead_signal, constant_signal, exponential_signal, weight = 1.0, p = .003):
    nest.ResetKernel()
    #network setting
    n = 300 #neurons
    #p = connection probability
    n_excited = 20 #neuron excited by input
    conn_dict = {"rule": "pairwise_bernoulli", "p": p}
    #simulation setting
    scale_size = 1000.0
    time = 15.0 * scale_size
    #neuron model
    params = {
        "t_ref": 1.59,
        "C_m": 14.6,
        "V_th": -60.0,
        "V_reset": -78.0,
        "E_L": -66.0,
        "tau_syn_ex": 0.64,
        "tau_syn_in": 2.0
    }
    nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)
    #input
    input_dict = {"rate": 300.0, "stop": scale_size}
    input_conn = {"rule": "fixed_total_number", "N": n_excited}

    nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)

    #building network
    input_curr = nest.Create("poisson_generator", params = input_dict)
    neuron_pop = nest.Create("leaky_i_f", n, params = params)

    nest.Connect(input_curr, neuron_pop, input_conn) #input
    nest.Connect(neuron_pop, neuron_pop, conn_dict) #inter-network connections
    #recording
    spikeDet = nest.Create("spike_detector", params = {"withgid": True, "withtime": True})
    nest.Connect(neuron_pop, spikeDet)
    #simulating
    nest.Simulate(time)

    #recording vars
    var = nest.GetStatus(spikeDet, keys = "events")
    spikes = np.array(var[0]["senders"])
    spike_freq = np.array(spikes * scale_size / time)
    t = np.array(var[0]["times"])

    indexes_10s = np.nonzero((10 * scale_size) < t) #indexes of all spikes after 10s
    indexes_1s = np.nonzero((scale_size) < t) #indexes of all spikes after 1s
    spikes_10s = spike_freq[indexes_10s[0]] if spike_freq[indexes_10s[0]] != [] else 0 #first spike frequency after 10s
    spikes_1s = spike_freq[indexes_1s[0]] if spike_freq[indexes_1s[0]] != [] else 0 #first spike frequency after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

    if ratio == 0:
        dead_signal = np.append(dead_signal, np.sum(spike_freq))
    elif ratio < 2.0 and ratio > 0:
        constant_signal = np.append(constant_signal, np.sum(spike_freq))
    elif ratio > 2.0:
        exponential_signal = np.append(exponential_signal, np.sum(spike_freq))
    return dead_signal, constant_signal, exponential_signal


def plot_add(plot, x_val, y_val, color_graph, name_trace):
    plot.add_trace(go.Scatter(x= x_val, y= y_val, mode= "markers", marker=dict(color=color_graph), name= name_trace))

w = 1.0
dead_signal = np.array([]) #if the outcome doesn't propagate for 9 seconds after the initial pulse
constant_signal = np.array([]) #if the outcome propagates for at least 9 seconds after the initial pulse
exponential_signal = np.array([]) #if the outcome at least duplicates itself after 9 seconds after the initial pulse
weights = []
while w <= 101.0:
    dead_signal, constant_signal, exponential_signal = create_network(dead_signal, constant_signal, exponential_signal, w)
    weights.append(w)
    w += w

#plotting
pio.templates.default = "simple_white" # Sets the plotly default theme
plot = px.scatter()
step_1 = []
for x in range(1, len(dead_signal)):
    step_1.append(x) #from 1 to dead signal lenght
step_2 = []
for x in range(len(dead_signal), len(dead_signal) + len(constant_signal)):
    step_2.append(x) #from dead signal lenght to constant signal lenght
step_3 = []
for x in range(len(dead_signal) + len(constant_signal), len(dead_signal) + len(constant_signal) + len(exponential_signal)):
    step_3.append(x) #from constant signal length to exponential signal lenght

plot_add(plot, step_1, dead_signal, "rgba(38, 250, 1, .8)", "dead signal")
plot_add(plot, step_2, constant_signal, "rgba(250, 220, 0, .8)", "constant signal")
plot_add(plot, step_3, exponential_signal, "rgba(255, 16, 0, .8)", "exploded signal")
plot.update_layout(xaxis_title="Weight (pS)", yaxis_title= "Spikes frequency (Hz)")
plot.show()
plot.write_image("prova.png")
np.savetxt('weights.csv', np.c_[dead_signal, constant_signal, exponential_signal, weights])