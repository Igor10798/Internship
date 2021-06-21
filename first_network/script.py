import nest
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

def create_network(weight = 1.0, p = .003, isPlastic = False, isFirst = True):
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
    if isFirst:
        nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)

    #input
    input_dict = {"rate": 300.0, "stop": one_sec}
    input_conn = {"rule": "fixed_total_number", "N": n_excited}
    syn_conn = { "weight" : weight, "model": "stdp_synapse" } if isPlastic else { "weight": weight }

    #building network
    input_curr = nest.Create("poisson_generator", params = input_dict)
    neuron_pop = nest.Create("leaky_i_f", n)

    nest.Connect(input_curr, neuron_pop, input_conn) #input
    nest.Connect(neuron_pop, neuron_pop, conn_dict, syn_conn) #inter-network connections
    #recording
    spikeDet = nest.Create("spike_detector", params = {"withgid": True, "withtime": True})
    nest.Connect(neuron_pop, spikeDet)
    return input_curr, neuron_pop, spikeDet

def record_vars(spikeDet):
    #recording vars
    var = nest.GetStatus(spikeDet, keys = "events")
    spikes = np.array(var[0]["senders"])
    spike_freq = np.array(spikes * one_sec / time)
    t = np.array(var[0]["times"])
    return spike_freq, t

def label_network(spikeDet, var, dead_sig = None, step_one = None, const_sign = None, step_two = None, exp_sign = None, step_three = None):
    #modifying global vars if customized are not inserted
    if dead_sig is None and step_one is None and const_sign is None and step_two is None and exp_sign is None and step_three is None:    
        global step_1
        global step_2
        global step_3
        global dead_signal
        global constant_signal
        global exploded_signal
    else:
        step_1 = step_one
        step_2 = step_two
        step_3 = step_three
        dead_signal = dead_signal
        constant_signal = const_sign
        exploded_signal = exp_sign

    spike_freq, t = record_vars(spikeDet) #getting output and associated time

    mask_10s = (10 * one_sec) < t
    mask_1s = one_sec < t
    spikes_10s = spike_freq[mask_10s][0] if spike_freq[mask_10s].size != 0 else 0 #indexes of all spikes after 10s
    spikes_1s = spike_freq[mask_1s][0] if spike_freq[mask_1s].size != 0 else 0 #indexes of all spikes after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

    #labelling the network in base of its growth
    if ratio == 0:
        dead_signal = np.append(dead_signal, np.sum(spike_freq))
        step_1.append(var)
    elif ratio < 2.0 and ratio > 0:
        constant_signal = np.append(constant_signal, np.sum(spike_freq))
        step_2.append(var)
    elif ratio >= 2.0:
        exploded_signal = np.append(exploded_signal, np.sum(spike_freq))
        step_3.append(var)
    #returning customized vars
    if dead_sig is not None and step_one is not None and const_sign is not None and step_two is not None and exp_sign is not None and step_three is not None:    
        return step_1, step_2, step_3, dead_signal, constant_signal, exploded_signal

def multiple_nets(w, probs_1 = None, probs_20 = None, probs_40 = None, probs_60 = None, probs_80 = None, probs_100 = None):
    #modifying global vars if customized are not inserted
    if probs_1 is None and probs_20 is None and probs_40 is None and probs_60 is None and probs_80 is None and probs_100 is None:    
        global probs_at_1
        global probs_at_20
        global probs_at_40
        global probs_at_60
        global probs_at_80
        global probs_at_100
    else:
        probs_at_1 = probs_1
        probs_at_20 = probs_20
        probs_at_40 = probs_40
        probs_at_60 = probs_60
        probs_at_80 = probs_80
        probs_at_100 = probs_100
        
    spike_freq, t = record_vars(spikeDet) #getting output and associated time

    #inserting the output in the right array
    if w == 1:
        probs_at_1.append(spike_freq)
    elif w == 20:
        probs_at_20.append(spike_freq)
    elif w == 40:
        probs_at_40.append(spike_freq)
    elif w == 60:
        probs_at_60.append(spike_freq)
    elif w == 80:
        probs_at_80.append(spike_freq)
    elif w == 100:
        probs_at_100.append(spike_freq)
    #returning customized vars
    if probs_1 is not None and probs_20 is not None and probs_40 is not None and probs_60 is not None and probs_80 is not None and probs_100 is not None:    
        return probs_at_1, probs_at_20, probs_at_40, probs_at_60, probs_at_80, probs_at_100

def compare_plasticity(spikeDet, spikeDet_plasticity, var):
    spike_freq, t = record_vars(spikeDet) #getting output and associated times
    spike_freq_plasticity, t_plasticity = record_vars(spikeDet) #getting output and associated times

    #preparing plot
    pio.templates.default = "simple_white" # Sets the plotly default theme
    plot = px.scatter()
    #comparison plot
    plot_add(plot, t, spike_freq, "rgba(250, 220, 0, .8)", "No plasticity")
    plot_add(plot, t_plasticity, spike_freq_plasticity, "rgba(38, 250, 1, .8)", "Plasticity")
    plot.update_layout(xaxis_title= "Time (ms)", yaxis_title= "Spikes frequency (Hz)")
    #no plasticity plot
    plot2 = px.scatter(x= t, y= spike_freq, labels={'x': 'Time (ms)', 'y': 'Spike frequency (Hz)'})
    #plasticity plot
    plot3 = px.scatter(x= t_plasticity, y= spike_freq_plasticity, labels={'x': 'Time (ms)', 'y': 'Spike frequency (Hz)'})
    #saving plots
    plot.show()
    plot2.show()
    plot3.show()
    plot.write_image("plasticity/comparison_plasticity_w{}.png".format(var))
    plot2.write_image("plasticity/no_plasticity_w{}.png".format(var))
    plot3.write_image("plasticity/plasticity_w{}.png".format(var))

#plotting functions
def plot_add(plot, x_val, y_val, color_graph, name_trace):
    plot.add_trace(go.Scatter(x= x_val, y= y_val, mode= "markers", marker=dict(color=color_graph), name= name_trace))

def plot_variation_loop(step_1, dead_signal, step_2, constant_signal, step_3, exploded_signal, x_axis, file_name):
    #preparing plot
    pio.templates.default = "simple_white"
    plot = px.scatter()

    plot_add(plot, step_1, dead_signal, "rgba(255, 16, 0, .8)", "dead signal")
    plot_add(plot, step_2, constant_signal, "rgba(250, 220, 0, .8)", "constant signal")
    plot_add(plot, step_3, exploded_signal, "rgba(38, 250, 1, .8)", "exploded signal")
    plot.update_layout(xaxis_title= x_axis, yaxis_title= "Spikes frequency (Hz)")
    plot.show()
    plot.write_image("{}.png".format(file_name, w))

#simulation setting
one_sec = 1000.0
time = 11.0 * one_sec #simulation time
w = 1.0
p = .003
#data to be exported
dead_signal = np.array([]) #if the outcome doesn't propagate for 9 seconds after the initial pulse
constant_signal = np.array([]) #if the outcome propagates for at least 9 seconds after the initial pulse
exploded_signal = np.array([]) #if the outcome at least duplicates itself after 9 seconds after the initial pulse
weights = [] #weights associated with outcome
probabilities = [] #probabilities associated with outcome
    #interaction weights-connectivity
set_weights = [1, 20, 40, 60, 80, 100]
probs_at_1 = []
probs_at_20 = []
probs_at_40 = []
probs_at_60 = []
probs_at_80 = []
probs_at_100 = []

#data for the plot
step_1 = []
step_2 = []
step_3 = []

    #weights on outcome
# while w < 101.0:
#     nest.ResetKernel()    
#     input_curr, neuron_pop, spikeDet = create_network(w)
#     nest.Simulate(time)
#     label_network(spikeDet, w)
#     weights.append(w)
#     w += w
# plot_variation_loop(step_1, dead_signal, step_2, constant_signal, step_3, exploded_signal, "Weight (pS)", "weights")

    #probability on outcome
# while p < .104:
#     nest.ResetKernel()    
#     input_curr, neuron_pop, spikeDet = create_network(w, p)
#     nest.Simulate(time)
#     label_network(spikeDet, p)
#     probabilities.append(p)
#     p = .001 + p
# plot_variation_loop(step_1, dead_signal, step_2, constant_signal, step_3, exploded_signal, "Connection probability", "probability")

    #relationship weight and probability on outcome
# while p < .104:
#     for w in set_weights:
#         nest.ResetKernel()
#         input_curr, neuron_pop, spikeDet = create_network(w, p)
#         nest.Simulate(time)
#         multiple_nets(w) #y axis
#     probabilities.append(p) #x axis
#     p = .001 + p

    #comparison plasticity & non
for w in set_weights:
    nest.ResetKernel()
    input_curr, neuron_pop, spikeDet = create_network(w)
    input_curr_plasticity, neuron_pop_plasticity, spikeDet_plasticity = create_network(w, p, True, False)
    nest.Simulate(time)
    compare_plasticity(spikeDet, spikeDet_plasticity, w)
    