import pickle
import numpy as np
import modules.graphs as graph
from collect_data import set_weights
from collect_data import p_conn
from glob import glob
from modules.models import LineForChart

def graph_raw():
    time_bin_width = 5
    for pkl_path in glob("offline_analysis/sim_pkl/*.pkl"):
        print("Analyzing", pkl_path)
        with open(pkl_path, "rb") as f:
            w, p, spike_matrix = pickle.load(f)
        time = spike_matrix[:,1]
        time_bin = int(( np.amax(time) - np.amin(time) )/ time_bin_width)
        sig_time = np.histogram(time, time_bin)
        fig = graph.raw_histogram(spike_matrix[:,0], sig_time)
        
        fig.write_image(f'{pkl_path}_raw.png')
        fig.write_html(f'{pkl_path}_raw.html')

w_gen = np.array([])
w_dead = np.array([])
w_dead_all = np.array([])
w_const = np.array([])
w_const_all = np.array([])
w_exploded = np.array([])
w_exploded_all = np.array([])
p_gen = np.array([])
p_dead = np.array([])
p_dead_all = np.array([])
p_const = np.array([])
p_const_all = np.array([])
p_exploded = np.array([])
p_exploded_all = np.array([])
freq_gen = np.array([])

for pkl_path in glob("offline_analysis/sim_pkl/*.pkl"):
    with open(pkl_path, "rb") as f:
        w, p, spike_matrix = pickle.load(f)
    spike_t = spike_matrix[:,1]
    spike_freq = spike_matrix[:,0]
    #saving max spikes for further analysis with R
    total_interval = np.amax(spike_t) / 1000
    total_freq = np.sum(spike_freq) / total_interval
    #arrays to update and will be pushed in np.savetext
    w_gen = np.append(w_gen, w)
    p_gen = np.append(p_gen, p)
    freq_gen = np.append(freq_gen, total_freq)

    #masking for labelling network (dead, constant, exploded)
    mask_10s = (10 * 1000) < spike_t
    mask_1s = 1000 < spike_t
    spikes_10s = spike_freq[mask_10s][0] if spike_freq[mask_10s].size != 0 else 0 #indexes of all spikes after 10s
    spikes_1s = spike_freq[mask_1s][0] if spike_freq[mask_1s].size != 0 else 0 #indexes of all spikes after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0
    
    #labelling the network in base of its growth
    if ratio == 0:
        w_dead_all = np.append(w_dead_all, w)
        p_dead_all = np.append(p_dead_all, p)
    elif ratio < 2.0 and ratio > 0:
        w_const_all = np.append(w_const_all, w)
        p_const_all = np.append(p_const_all, p)
    elif ratio >= 2.0:
        w_exploded_all = np.append(w_exploded_all, w)
        p_exploded_all = np.append(p_exploded_all, p)

#mask to get max p for every w value (for the stacked graph)
def apply_maxValue(final_p, p_val, w_val):
    for i, w in enumerate(w_val):
        if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
            final_p = np.append(final_p, p_val[i])
    return final_p

def apply_differentValue(final_w, w_val):
    for i, w in enumerate(w_val):
        if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
            final_w = np.append(final_w, w_val[i])
    return final_w

p_dead = apply_maxValue(p_dead, p_dead_all, w_dead_all)
p_const = apply_maxValue(p_const, p_const_all, w_const_all)
p_exploded = apply_maxValue(p_exploded, p_exploded_all, w_exploded_all)
w_dead = apply_differentValue(w_dead, w_dead_all)
w_const = apply_differentValue(w_const, w_const_all)
w_exploded = apply_differentValue(w_exploded, w_exploded_all)

#creating and saving data
save_tot_freq = np.c_[w_gen, p_gen, freq_gen]
dead_signal = np.c_[w_dead, p_dead]
dead_signal = np.sort(dead_signal, axis = 0)
constant_signal = np.c_[w_const, p_const]
constant_signal = np.sort(constant_signal, axis = 0)
exploded_signal = np.c_[w_exploded, p_exploded]
exploded_signal = np.sort(exploded_signal, axis = 0)
np.savetxt('offline_analysis/data/dead_stacked.csv', dead_signal)
np.savetxt('offline_analysis/data/constant_stacked.csv', constant_signal)
np.savetxt('offline_analysis/data/exploded_stacked.csv', exploded_signal)
np.savetxt('offline_analysis/data/not_labelled_data.csv', save_tot_freq)

d_sig = LineForChart(dead_signal[:,0], dead_signal[:,1])
c_sig = LineForChart(constant_signal[:,0], constant_signal[:,1])
e_sig = LineForChart(exploded_signal[:,0], exploded_signal[:,1])

#stacked graph
fig_2 = graph.stacked_area(d_sig, c_sig, e_sig)
fig_2.write_image('offline_analysis/params_interaction/stacked.png')
fig_2.write_html('offline_analysis/params_interaction/stacked.html')