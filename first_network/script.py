import nest
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

def create_network(weight = 1.0, p = .003):
    #network setting
    n = 300 #neurons
    #p = connection probability
    n_excited = 20 #neuron excited by input
    conn_dict = {"rule": "pairwise_bernoulli", "p": p}

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
    input_dict = {"rate": 300.0, "stop": one_sec}
    input_conn = {"rule": "fixed_total_number", "N": n_excited}
    syn_conn = {"weight": weight}

    #building network
    input_curr = nest.Create("poisson_generator", params = input_dict)
    neuron_pop = nest.Create("leaky_i_f", n)

    nest.Connect(input_curr, neuron_pop, input_conn) #input
    nest.Connect(neuron_pop, neuron_pop, conn_dict, syn_conn) #inter-network connections
    #recording
    spikeDet = nest.Create("spike_detector", params = {"withgid": True, "withtime": True})
    nest.Connect(neuron_pop, spikeDet)
    return input_curr, neuron_pop, spikeDet

def label_network(spikeDet, p):
    global step_1
    global step_2
    global step_3
    global dead_signal
    global constant_signal
    global exponential_signal
    #recording vars
    var = nest.GetStatus(spikeDet, keys = "events")
    spikes = np.array(var[0]["senders"])
    spike_freq = np.array(spikes * one_sec / time)
    t = np.array(var[0]["times"])

    mask_10s = (10 * one_sec) < t
    mask_1s = one_sec < t
    spikes_10s = spike_freq[mask_10s][0] if spike_freq[mask_10s].size != 0 else 0 #indexes of all spikes after 10s
    spikes_1s = spike_freq[mask_1s][0] if spike_freq[mask_1s].size != 0 else 0 #indexes of all spikes after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

    if ratio == 0:
        dead_signal = np.append(dead_signal, np.sum(spike_freq))
        step_1.append(p)
    elif ratio < 2.0 and ratio > 0:
        constant_signal = np.append(constant_signal, np.sum(spike_freq))
        step_2.append(p)
    elif ratio >= 2.0:
        exponential_signal = np.append(exponential_signal, np.sum(spike_freq))
        step_3.append(p)


def plot_add(plot, x_val, y_val, color_graph, name_trace):
    plot.add_trace(go.Scatter(x= x_val, y= y_val, mode= "markers", marker=dict(color=color_graph), name= name_trace))

#simulation setting
one_sec = 1000.0
time = 15.0 * one_sec
w = 1.0
p = .003
#data to be exported
dead_signal = np.array([]) #if the outcome doesn't propagate for 9 seconds after the initial pulse
constant_signal = np.array([]) #if the outcome propagates for at least 9 seconds after the initial pulse
exponential_signal = np.array([]) #if the outcome at least duplicates itself after 9 seconds after the initial pulse
weights = []

#data for the plot
step_1 = []
step_2 = []
step_3 = []
while w < 101.0:
    nest.ResetKernel()    
    input_curr, neuron_pop, spikeDet = create_network(w)
    nest.Simulate(time)
    label_network(spikeDet, w)
    weights.append(w)
    w += w
    
# while p < .104:
#     nest.ResetKernel()    
#     input_curr, neuron_pop, spikeDet = create_network(w, p)
#     nest.Simulate(time)
#     label_network(spikeDet, p)
#     p = .001 + p
#plotting

pio.templates.default = "simple_white" # Sets the plotly default theme
plot = px.scatter()

plot_add(plot, step_1, dead_signal, "rgba(38, 250, 1, .8)", "dead signal")
plot_add(plot, step_2, constant_signal, "rgba(250, 220, 0, .8)", "constant signal")
plot_add(plot, step_3, exponential_signal, "rgba(255, 16, 0, .8)", "exploded signal")
plot.update_layout(xaxis_title="Weight (pS)", yaxis_title= "Spikes frequency (Hz)")
plot.show()
plot.write_image("weight.png")