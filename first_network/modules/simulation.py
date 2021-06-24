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

def multiple_nets(w,  probabilities = None):
    #modifying global vars if customized are not inserted
    if probabilities is None:    
        global probs
    else:
        probabilities = probs
        
    spike_freq, t = record_vars(spikeDet) #getting output and associated time

    #inserting the output in the right array
    if w == 1:
        probabilities.at_1.append(spike_freq)
    elif w == 20:
        probabilities.at_20.append(spike_freq)
    elif w == 40:
        probabilities.at_40.append(spike_freq)
    elif w == 60:
        probabilities.at_60.append(spike_freq)
    elif w == 80:
        probabilities.at_80.append(spike_freq)
    elif w == 100:
        probabilities.at_100.append(spike_freq)
    #returning customized vars
    if probs is not None:
        return probabilities

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

def label_net_stacked_area(spikeDet, param, dead, constant, exploded):

    spike_freq, t = record_vars(spikeDet) #getting output and associated time

    mask_10s = (10 * one_sec) < t
    mask_1s = one_sec < t
    spikes_10s = spike_freq[mask_10s][0] if spike_freq[mask_10s].size != 0 else 0 #indexes of all spikes after 10s
    spikes_1s = spike_freq[mask_1s][0] if spike_freq[mask_1s].size != 0 else 0 #indexes of all spikes after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

    #labelling the network in base of its growth
    if ratio == 0:
        dead = np.append(dead, param)
    elif ratio < 2.0 and ratio > 0:
        constant = np.append(constant, param)
    elif ratio >= 2.0:
        exploded = np.append(exploded, param)
    
    return dead, constant, exploded

#plotting functions
def plot_add(plot, x_val, y_val, color_graph, name_trace):
    plot.add_trace(go.Scatter(x= x_val, y= y_val, mode= "markers", marker=dict(color=color_graph), name= name_trace))

def plot_variation_loop(step_1, dead_signal, step_2, constant_signal, step_3, exploded_signal, x_axis, file_name, path = "params_variability"):
    #preparing plot
    pio.templates.default = "simple_white"
    plot = px.scatter()

    plot_add(plot, step_1, dead_signal, "rgba(255, 16, 0, .8)", "dead signal")
    plot_add(plot, step_2, constant_signal, "rgba(250, 220, 0, .8)", "constant signal")
    plot_add(plot, step_3, exploded_signal, "rgba(38, 250, 1, .8)", "exploded signal")
    plot.update_layout(xaxis_title= x_axis, yaxis_title= "Spikes frequency (Hz)")
    plot.show()
    plot.write_image("{}/{}.png".format(path, file_name))

def plot_interaction(prob, probabilities, x_axis, file_name, path = "params_interaction"):
    #preparing plot
    pio.templates.default = "simple_white"
    plot = px.scatter()

    plot_add(plot, probabilities, prob.at_1, "rgba(255, 16, 0, .8)", "w = 1 (pS)")
    plot_add(plot, probabilities, prob.at_20, "rgba(255, 16, 0, .8)", "w = 20 (pS)")
    plot_add(plot, probabilities, prob.at_40, "rgba(255, 16, 0, .8)", "w = 40 (pS)")
    plot_add(plot, probabilities, prob.at_60, "rgba(255, 16, 0, .8)", "w = 60 (pS)")
    plot_add(plot, probabilities, prob.at_80, "rgba(255, 16, 0, .8)", "w = 80 (pS)")
    plot_add(plot, probabilities, prob.at_100, "rgba(255, 16, 0, .8)", "w = 100 (pS)")
    plot.update_layout(xaxis_title= x_axis, yaxis_title= "Spikes frequency (Hz)")
    plot.show()
    plot.write_image("{}/{}.png".format(path, file_name))

#simulation settings
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
class Probs_at_w:
    def __init__(self):
        self.at_1 = []
        self.at_20 = []
        self.at_40 = []
        self.at_60 = []
        self.at_80 = []
        self.at_100 = []
probs = Probs_at_w()

#data for the plot
step_1 = []
step_2 = []
step_3 = []