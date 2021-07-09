import pickle
import numpy as np
import modules.graphs as graph
from collect_data import set_weights
from collect_data import p_conn
from modules.simulation import time
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
        sig_time, histo_edges = np.histogram(time, time_bin, density = True)
        fig = graph.raw_histogram(histo_edges, sig_time)
        #printing for check
        if pkl_path == "offline_analysis/sim_pkl/7_7.pkl":
            np.savetxt('offline_analysis/data/7_7.csv', spike_matrix)
            print(histo_edges, sig_time)
        elif pkl_path == "offline_analysis/sim_pkl/1_3.pkl":
            np.savetxt('offline_analysis/data/1_3.csv', spike_matrix)
        elif pkl_path == "offline_analysis/sim_pkl/4_4.pkl":
            np.savetxt('offline_analysis/data/4_4.csv', spike_matrix)
        fig.write_image(f'{pkl_path}_raw.png')

#graph_raw()

n_pkl = len(glob("offline_analysis/sim_pkl/*.pkl"))
label_net = np.zeros(n_pkl)
w_list = np.zeros(n_pkl)
p_list = np.zeros(n_pkl)
freq_list = np.zeros(n_pkl)

#variables to save and plot
p_dead = []
p_const = []
p_exploded = []
w_dead = []
w_const = []
w_exploded = []

for i, pkl_path in enumerate(glob("offline_analysis/sim_pkl/*.pkl")):
    with open(pkl_path, "rb") as f:
        w, p, spike_matrix = pickle.load(f)
    spike_t = spike_matrix[:,1]
    spike_freq = spike_matrix[:,0].size / time
    #arrays to update and will be pushed in np.savetext
    w_list[i] = w
    p_list[i] = p
    freq_list[i] = spike_freq.size

    #masking for labelling network (dead, constant, exploded)
    mask_10s = (10 * 1000) < spike_t
    mask_1s = 1000 < spike_t
    spikes_10s = spike_freq[mask_10s].size #indexes of all spikes after 10s
    spikes_1s = spike_freq[mask_1s].size #indexes of all spikes after 1s
    ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

    #labelling the network in base of its growth
    if ratio == 0:
        label_net[i] = 1
    elif ratio >= 1.5:
        label_net[i] = 3
    elif ratio < 1.5 and ratio > 0:
        label_net[i] = 2
    else:
        print("Che cazzo succede?", spikes_1s)
        print("Non lo so", spikes_10s)

#mask to get max p for every w value (for the stacked graph)
def apply_maxValue(final_p, p_val, w_val, label, type_label):
    if type_label == 1:
        mask = (label_net == 1)
    elif type_label == 2:
        mask = (label_net == 2)
    elif type_label == 3:
        mask = (label_net == 3)
    p_val = p_val[mask]
    w_val = w_val[mask]

    for i, w in enumerate(w_val):
        if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
            final_p.append(p_val[i])
    return final_p

def apply_differentValue(final_w, w_val, label, type_label):
    if type_label == 1:
        mask = (label_net == 1)
    elif type_label == 2:
        mask = (label_net == 2)
    elif type_label == 3:
        mask = (label_net == 3)
    w_val = w_val[mask]

    for i, w in enumerate(w_val):
        if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
            final_w.append(w_val[i])
    return final_w

p_dead = apply_maxValue(p_dead, p_list, w_list, label_net, 1)
p_const = apply_maxValue(p_const, p_list, w_list, label_net, 2)
p_exploded = apply_maxValue(p_exploded, p_list, w_list, label_net, 3)
w_dead = apply_differentValue(w_dead, w_list, label_net, 1)
w_const = apply_differentValue(w_const, w_list, label_net, 2)
w_exploded = apply_differentValue(w_exploded, w_list, label_net, 3)

#save data
np.savetxt('offline_analysis/data/dead_stacked.csv', np.c_[w_list[label_net == 1], p_list[label_net == 1]])
np.savetxt('offline_analysis/data/constant_stacked.csv', np.c_[w_list[label_net == 2], p_list[label_net == 2]])
np.savetxt('offline_analysis/data/exploded_stacked.csv', np.c_[w_list[label_net == 3], p_list[label_net == 3]])
np.savetxt('offline_analysis/data/not_labelled_data.csv', np.c_[w_list, p_list, freq_list, label_net])

d_sig = LineForChart(w_dead, p_dead)
c_sig = LineForChart(w_const, p_const)
e_sig = LineForChart(w_exploded, p_exploded)

#stacked graph
fig_2 = graph.stacked_area(d_sig, c_sig, e_sig)
fig_2.write_image('offline_analysis/params_interaction/stacked.png')
fig_2.write_html('offline_analysis/params_interaction/stacked.html')

# w_gen = np.array([])
# w_dead = np.array([])
# w_dead_all = np.array([])
# w_const = np.array([])
# w_const_all = np.array([])
# w_exploded = np.array([])
# w_exploded_all = np.array([])
# p_gen = np.array([])
# p_dead = np.array([])
# p_dead_all = np.array([])
# p_const = np.array([])
# p_const_all = np.array([])
# p_exploded = np.array([])
# p_exploded_all = np.array([])
# freq_gen = np.array([])

# for pkl_path in glob("offline_analysis/sim_pkl/*.pkl"):
#     with open(pkl_path, "rb") as f:
#         w, p, spike_matrix = pickle.load(f)
#     spike_t = spike_matrix[:,1]
#     spike_freq = spike_matrix[:,0]
#     saving max spikes for further analysis with R
#     total_interval = np.amax(spike_t) / 1000
#     total_freq = np.sum(spike_freq) / total_interval
#     arrays to update and will be pushed in np.savetext
#     w_gen = np.append(w_gen, w)
#     p_gen = np.append(p_gen, p)
#     freq_gen = np.append(freq_gen, len(spike_matrix) / time)

#     masking for labelling network (dead, constant, exploded)
#     mask_10s = (10 * 1000) < spike_t
#     mask_1s = 1000 < spike_t
#     spikes_10s = spike_freq[mask_10s][0] if spike_freq[mask_10s].size != 0 else 0 #indexes of all spikes after 10s
#     spikes_1s = spike_freq[mask_1s][0] if spike_freq[mask_1s].size != 0 else 0 #indexes of all spikes after 1s
#     ratio = spikes_10s / spikes_1s if spikes_1s != 0 else 0

#     labelling the network in base of its growth
#     if ratio == 0:
#         w_dead_all = np.append(w_dead_all, w)
#         p_dead_all = np.append(p_dead_all, p)
#     elif ratio < 2.0 and ratio > 0:
#         w_const_all = np.append(w_const_all, w)
#         p_const_all = np.append(p_const_all, p)
#     elif ratio >= 2.0:
#         w_exploded_all = np.append(w_exploded_all, w)
#         p_exploded_all = np.append(p_exploded_all, p)

# mask to get max p for every w value (for the stacked graph)
# def apply_maxValue(final_p, p_val, w_val):
#     for i, w in enumerate(w_val):
#         if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
#             final_p = np.append(final_p, p_val[i])
#     return final_p

# def apply_differentValue(final_w, w_val):
#     for i, w in enumerate(w_val):
#         if (w > w_val[i - 1] or i == 0) and w_val.size > 0:
#             final_w = np.append(final_w, w_val[i])
#     return final_w

# p_dead = apply_maxValue(p_dead, p_dead_all, w_dead_all)
# p_const = apply_maxValue(p_const, p_const_all, w_const_all)
# p_exploded = apply_maxValue(p_exploded, p_exploded_all, w_exploded_all)
# w_dead = apply_differentValue(w_dead, w_dead_all)
# w_const = apply_differentValue(w_const, w_const_all)
# w_exploded = apply_differentValue(w_exploded, w_exploded_all)

#creating and saving data
# save_tot_freq = np.c_[w_gen, p_gen, freq_gen]
# dead_signal = np.c_[w_dead, p_dead]
# dead_signal = np.sort(dead_signal, axis = 0)
# constant_signal = np.c_[w_const, p_const]
# constant_signal = np.sort(constant_signal, axis = 0)
# exploded_signal = np.c_[w_exploded, p_exploded]
# exploded_signal = np.sort(exploded_signal, axis = 0)
# np.savetxt('offline_analysis/data/dead_stacked.csv', dead_signal)
# np.savetxt('offline_analysis/data/constant_stacked.csv', constant_signal)
# np.savetxt('offline_analysis/data/exploded_stacked.csv', exploded_signal)
# np.savetxt('offline_analysis/data/not_labelled_data.csv', save_tot_freq)

# d_sig = LineForChart(dead_signal[:,0], dead_signal[:,1])
# c_sig = LineForChart(constant_signal[:,0], constant_signal[:,1])
# e_sig = LineForChart(exploded_signal[:,0], exploded_signal[:,1])

# #stacked graph
# fig_2 = graph.stacked_area(d_sig, c_sig, e_sig)
# fig_2.write_image('offline_analysis/params_interaction/stacked.png')
# fig_2.write_html('offline_analysis/params_interaction/stacked.html')