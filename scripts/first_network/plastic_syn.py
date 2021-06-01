import nest
import numpy as np

nest.ResetKernel()

#setting params
edict = { "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params=edict)

#inputs
def createInputs(param):
    return nest.Create("poisson_generator", params= param)
input_syn_dict = {"weight": 1.5}
input_dict = {"rate": 60000.0, "stop": 700.0}
noise_exc1 = createInputs(input_dict)
noise_exc2 = createInputs(input_dict)
input_dict_late = {"rate": 40000.0, "start": 500.0}
noise_exc1_late = createInputs(input_dict_late)
noise_exc2_late = createInputs(input_dict_late)

#populations
excNeuronPop1 = nest.Create("exc_iaf_psc_alpha", 30) 
inhNeuronPop = nest.Create("inh_iaf_psc_alpha", 15)

    #randomizing potentials
def ranzomizeParams(pop):
    return [{"V_m": vRest+(vTh-vRest)*np.random.rand(), "I_e": 100+100*np.random.rand(), "tau_syn_in": 5.0} for x in pop]
vTh = -55
vRest = -70
randomizedVs = ranzomizeParams(excNeuronPop1)
randomizedVs_inh = ranzomizeParams(inhNeuronPop)

excNeuronPop2 = nest.Create("exc_iaf_psc_alpha", 30, params= randomizedVs)
nest.SetStatus(excNeuronPop1, randomizedVs)
nest.SetStatus(inhNeuronPop, randomizedVs_inh)

#synapses
alpha_min = .1
alpha_max = 3.
w_mean = 12.0
w_dev = 3.0
ratio = -5.0 #inh/exc weigth ratio

syn_dict_ex =   {
    "model": "stdp_synapse",
    "alpha": {"distribution": "uniform", "low": alpha_min, "high": alpha_max},
    "weight": {"distribution": "normal", "mu": w_mean, "sigma": w_dev}
}
print(nest.GetDefaults("stdp_synapse"))
syn_dict_in =   {
    "model": "stdp_synapse",
    "alpha": {"distribution": "uniform", "low": alpha_min, "high": alpha_max},
    "weight": {"distribution": "normal", "mu": ratio*w_mean, "sigma": w_dev},
    "Wmax": -100.0
}

#connections
conn_dict_ex_str = {"rule": "pairwise_bernoulli", "p": .6}
conn_dict_ex_weak = {"rule": "pairwise_bernoulli", "p": .4}
conn_dict_in = {"rule": "pairwise_bernoulli", "p": .6}

nest.Connect(noise_exc1, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc1_late, excNeuronPop1, "all_to_all", syn_spec= input_syn_dict)
nest.Connect(noise_exc2_late, excNeuronPop2, "all_to_all", syn_spec= input_syn_dict)

nest.Connect(excNeuronPop1, inhNeuronPop, conn_dict_ex_str, syn_spec= syn_dict_ex)
nest.Connect(excNeuronPop2, inhNeuronPop, conn_dict_ex_weak, syn_spec= syn_dict_ex)
nest.Connect(inhNeuronPop, excNeuronPop1, conn_dict_in, syn_spec= syn_dict_in)
nest.Connect(inhNeuronPop, excNeuronPop2, conn_dict_in, syn_spec= syn_dict_in)

#recordings && simulation
def createDevice(n):
    return nest.Create("spike_detector", n, params={"withgid": True, "withtime": True})

spikeDet1 = createDevice(30)
spikeDet2 = createDevice(30)
spikeDet_inh = createDevice(15)
nest.Connect(excNeuronPop1, spikeDet1)
nest.Connect(excNeuronPop2, spikeDet2)
nest.Connect(inhNeuronPop, spikeDet_inh)

nest.Simulate(1000.0)

#plots
import plotly.express as px

dmm1 = nest.GetStatus(spikeDet1, keys= "events")[0]
spikes1 = dmm1['senders']
ts1 = dmm1["times"]
plot1 = px.scatter(x=ts1, y=spikes1, labels={'x': 't', 'y': 'spikes 1 -plasticity'})
plot1.show()

dmm2 = nest.GetStatus(spikeDet2, keys= "events")[0]
spikes2 = dmm2["senders"]
ts2 = dmm2["times"]
plot2 = px.scatter(x=ts2, y=spikes2, labels={'x': 't', 'y': 'spikes 2 -plasticity'})
plot2.show()

dmmInh = nest.GetStatus(spikeDet_inh, keys= "events")[0]
spikes_inh = dmmInh["senders"]
ts_inh = dmmInh["times"]
plot3 = px.scatter(x=ts_inh, y=spikes_inh, labels={'x': 't', 'y': 'inh spikes -plasticity'})
plot3.show()