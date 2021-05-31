"""
<=====================>
<==== BASIC LEVEL ====>
<=====================>
"""
"""
import nest

#setting params
edict = {"I_e": 200.0, "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha")
exc_syn_dic = {"weight": 20.0}
inh_syn_dic = {"weight": -30.0}

#inputs
input_dict = {"weight": 1.2}
noise_exc1 = nest.Create("poisson_generator", params={"rate": 80000.0})
noise_exc2 = nest.Create("poisson_generator", params={"rate": 80000.0})

#populations
excNeuronPop1 = nest.Create("exc_iaf_psc_alpha", 30) 
excNeuronPop2 = nest.Create("exc_iaf_psc_alpha", 30)
inhNeuronPop = nest.Create("inh_iaf_psc_alpha", 15)
#Even changin input of exc pops, I couldn't find any dinamics

#connections
nest.Connect(noise_exc1, excNeuronPop1, "all_to_all", syn_spec= input_dict)
nest.Connect(noise_exc2, excNeuronPop2, "all_to_all", syn_spec= input_dict)

nest.Connect(excNeuronPop1, inhNeuronPop, syn_spec= exc_syn_dic)
nest.Connect(excNeuronPop2, inhNeuronPop, syn_spec= exc_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop1, syn_spec= inh_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop2, syn_spec= inh_syn_dic)

#recordings && simulation
spikeDet1 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet2 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet_inh = nest.Create("spike_detector", 15, params={"withgid": True, "withtime": True})
nest.Connect(excNeuronPop1, spikeDet1)
nest.Connect(excNeuronPop2, spikeDet2)
nest.Connect(inhNeuronPop, spikeDet_inh)

nest.Simulate(1000.0)

#plots
import plotly.express as px

dmm1 = nest.GetStatus(spikeDet1, keys= "events")[0]
spikes1 = dmm1['senders']
ts1 = dmm1["times"]
plot1 = px.scatter(x=ts1, y=spikes1, labels={'x': 't', 'y': 'spikes 1'})
plot1.show()

dmm2 = nest.GetStatus(spikeDet2, keys= "events")[0]
spikes2 = dmm2["senders"]
ts2 = dmm2["times"]
plot2 = px.scatter(x=ts2, y=spikes2, labels={'x': 't', 'y': 'spikes 2'})
plot2.show()

dmm_inh = nest.GetStatus(spikeDet_inh, keys= "events")[0]
spikes_inh = dmm_inh["senders"]
ts_inh = dmm_inh["times"]
plot3 = px.scatter(x=ts_inh, y=spikes_inh, labels={'x': 't', 'y': 'inh spikes'})
plot3.show()

"""
"""
<===============================>
<==== ALEATORY CONNECTIVITY ====>
<===============================>
"""
"""

import nest
import numpy as np

#setting params
edict = { "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha")

#inputs
def createInputs(param):
    return nest.Create("poisson_generator", params= param)
input_syn_dict = {"weight": 1.2}
input_dict = {"rate": 80000.0, "stop": 700.0}
noise_exc1 = createInputs(input_dict)
noise_exc2 = createInputs(input_dict)
input_dict_late = {"rate": 30000.0, "start": 500.0}
noise_exc1_late = createInputs(input_dict_late)
noise_exc2_late = createInputs(input_dict_late)

#populations
excNeuronPop1 = nest.Create("exc_iaf_psc_alpha", 30) 
inhNeuronPop = nest.Create("inh_iaf_psc_alpha", 15)

    #randomizing potentials
def ranzomizePotentials(pop):
    return [{"V_m": vRest+(vTh-vRest)*np.random.rand(), "I_e": 200*np.random.rand()} for x in pop]
vTh = -55
vRest = -70
randomizedVs = ranzomizePotentials(excNeuronPop1)
randomizedVs_inh = ranzomizePotentials(inhNeuronPop)

excNeuronPop2 = nest.Create("exc_iaf_psc_alpha", 30, params= randomizedVs)
nest.SetStatus(excNeuronPop1, randomizedVs)
nest.SetStatus(inhNeuronPop, randomizedVs_inh)

#connections
d = 1.0
Je = 12.0
Ji = -20.0
conn_dict_ex_str = {"rule": "pairwise_bernoulli", "p": .5}
conn_dict_ex_weak = {"rule": "pairwise_bernoulli", "p": .4}
conn_dict_in = {"rule": "pairwise_bernoulli", "p": .6}
exc_syn_dic = {"delay": d, "weight": Je}
inh_syn_dic = {"delay": d, "weight": Ji}

nest.Connect(noise_exc1, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc1_late, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2_late, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)

nest.Connect(excNeuronPop1, inhNeuronPop, conn_dict_ex_str, syn_spec= exc_syn_dic)
nest.Connect(excNeuronPop2, inhNeuronPop, conn_dict_ex_weak, syn_spec= exc_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop1, conn_dict_in, syn_spec= inh_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop2, conn_dict_in, syn_spec= inh_syn_dic)

#recordings && simulation
spikeDet1 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet2 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet_inh = nest.Create("spike_detector", 15, params={"withgid": True, "withtime": True})
nest.Connect(excNeuronPop1, spikeDet1)
nest.Connect(excNeuronPop2, spikeDet2)
nest.Connect(inhNeuronPop, spikeDet_inh)

nest.Simulate(1000.0)

#plots
import plotly.express as px

dmm1 = nest.GetStatus(spikeDet1, keys= "events")[0]
spikes1 = dmm1['senders']
ts1 = dmm1["times"]
plot1 = px.scatter(x=ts1, y=spikes1, labels={'x': 't', 'y': 'spikes 1'})
plot1.show()

dmm2 = nest.GetStatus(spikeDet2, keys= "events")[0]
spikes2 = dmm2["senders"]
ts2 = dmm2["times"]
plot2 = px.scatter(x=ts2, y=spikes2, labels={'x': 't', 'y': 'spikes 2'})
plot2.show()

dmmInh = nest.GetStatus(spikeDet_inh, keys= "events")[0]
spikes_inh = dmmInh["senders"]
ts_inh = dmmInh["times"]
plot3 = px.scatter(x=ts_inh, y=spikes_inh, labels={'x': 't', 'y': 'inh spikes'})
plot3.show()
"""

"""
<==========================>
<==== PLASTIC SYNAPSES ====>
<==========================>
"""

import nest
import numpy as np

#setting params
edict = { "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha")

#inputs
def createInputs(param):
    return nest.Create("poisson_generator", params= param)
input_syn_dict = {"weight": 1.2}
input_dict = {"rate": 80000.0, "stop": 700.0}
noise_exc1 = createInputs(input_dict)
noise_exc2 = createInputs(input_dict)
input_dict_late = {"rate": 30000.0, "start": 500.0}
noise_exc1_late = createInputs(input_dict_late)
noise_exc2_late = createInputs(input_dict_late)

#populations
excNeuronPop1 = nest.Create("exc_iaf_psc_alpha", 30) 
inhNeuronPop = nest.Create("inh_iaf_psc_alpha", 15)

    #randomizing potentials
def ranzomizePotentials(pop):
    return [{"V_m": vRest+(vTh-vRest)*np.random.rand(), "I_e": 200*np.random.rand()} for x in pop]
vTh = -55
vRest = -70
randomizedVs = ranzomizePotentials(excNeuronPop1)
randomizedVs_inh = ranzomizePotentials(inhNeuronPop)

excNeuronPop2 = nest.Create("exc_iaf_psc_alpha", 30, params= randomizedVs)
nest.SetStatus(excNeuronPop1, randomizedVs)
nest.SetStatus(inhNeuronPop, randomizedVs_inh)

#connections
d = 1.0
Je = 12.0
Ji = -20.0
conn_dict_ex_str = {"rule": "pairwise_bernoulli", "p": .5}
conn_dict_ex_weak = {"rule": "pairwise_bernoulli", "p": .4}
conn_dict_in = {"rule": "pairwise_bernoulli", "p": .6}
exc_syn_dic = {"delay": d, "weight": Je}
inh_syn_dic = {"delay": d, "weight": Ji}

nest.Connect(noise_exc1, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc1_late, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2_late, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)

nest.Connect(excNeuronPop1, inhNeuronPop, conn_dict_ex_str, syn_spec= exc_syn_dic)
nest.Connect(excNeuronPop2, inhNeuronPop, conn_dict_ex_weak, syn_spec= exc_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop1, conn_dict_in, syn_spec= inh_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop2, conn_dict_in, syn_spec= inh_syn_dic)

#recordings && simulation
spikeDet1 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet2 = nest.Create("spike_detector", 30, params={"withgid": True, "withtime": True})
spikeDet_inh = nest.Create("spike_detector", 15, params={"withgid": True, "withtime": True})
nest.Connect(excNeuronPop1, spikeDet1)
nest.Connect(excNeuronPop2, spikeDet2)
nest.Connect(inhNeuronPop, spikeDet_inh)

nest.Simulate(1000.0)

#plots
import plotly.express as px

dmm1 = nest.GetStatus(spikeDet1, keys= "events")[0]
spikes1 = dmm1['senders']
ts1 = dmm1["times"]
plot1 = px.scatter(x=ts1, y=spikes1, labels={'x': 't', 'y': 'spikes 1'})
plot1.show()

dmm2 = nest.GetStatus(spikeDet2, keys= "events")[0]
spikes2 = dmm2["senders"]
ts2 = dmm2["times"]
plot2 = px.scatter(x=ts2, y=spikes2, labels={'x': 't', 'y': 'spikes 2'})
plot2.show()

dmmInh = nest.GetStatus(spikeDet_inh, keys= "events")[0]
spikes_inh = dmmInh["senders"]
ts_inh = dmmInh["times"]
plot3 = px.scatter(x=ts_inh, y=spikes_inh, labels={'x': 't', 'y': 'inh spikes'})
plot3.show()