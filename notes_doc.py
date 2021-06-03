#=========================#
#<==== SINGLE NEURON ====>#
#=========================#
import pylab
import nest

neuron = nest.Create("iaf_psc_alpha") #create neuron
nest.GetStatus(neuron, ["V_reset"]) #dictionary with all neuron settings or specified setting
nest.SetStatus(neuron, {"I_e": 376.0}) #changing dictionary value

multimeter = nest.Create("multimeter") #it is a device, it records the membrane voltage over time
nest.GetStatus(multimeter) #getting modificable value of device
nest.GetStatus(neuron, "recordables") #check variables that can be recorded
nest.SetStatus(multimeter, {"withtime": True, "record_from":["V_m"]})   #withtime records the points in time at which it samples the membrane voltage
#SetStatus() is less efficient than params in Create()                                                                        #record_from expects a list of the names of the variables we would like to record

spikeDet = nest.Create("spike_detector", params={"withgid": True, "withtime": True}) #withgid indicates whether the spike detector is to record the source id from which it received the event

nest.Connect(multimeter, neuron) #connecting different nodes
nest.Connect(neuron, spikeDet) # <==ORDER MATTERS==>multimeter asks for membrane potential to neuron, and when neuron spikes, it sends the event to de detector

nest.Simulate(1000.0) #running simulation


import plotly.express as px
#getting data for membrane potential
dmm = nest.GetStatus(multimeter)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
#plotting graph
plot1 = px.line(x=ts, y=Vms, labels={'x': 't', 'y': 'Vm'})
plot1.show()

#repeating the same procedure for spykes, using keys to extract only the event dictionary
dSD = nest.GetStatus(spikeDet, keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
plot2 = px.scatter(x=ts, y=evs, labels={'x': 't', 'y': 'Spikes'})
plot2.show()


#========================#
#<==== MORE NEURONS ====>#
#========================#
import pylab
import nest

neuron1, neuron2 = nest.Create("iaf_psc_alpha", 2, params={"I_e": 370.0})

nest.Connect(multimeter, neuron2) #connecting at the same device

pylab.figure(2) #?
Vms1 = dmm["events"]["V_m"][::2] # start at index 0: till the end: each second entry
ts1 = dmm["events"]["times"][::2]
pylab.plot(ts1, Vms1)
Vms2 = dmm["events"]["V_m"][1::2] # start at index 1: till the end: each second entry
ts2 = dmm["events"]["times"][1::2]
pylab.plot(ts2, Vms2)

#======================================================#
#<==== CONNECTING NODES WITH SPECIFIC CONNECTIONS ====>#
#======================================================#
import nest

neuron = nest.Create("ias_psc_alpha", params={"I_e": 0.0})
noise_ex = nest.Create("poisson_generator", params={"rate": 80000.0}) #excitatory spike train
noise_in = nest.Create("poisson_generator", params={"rate": 15000.0}) #inhibitory spike train

#setting weights of spike trains
syn_dict_ex = {"weight": 1.2} #post-sinaptic current of 1.2pA
syn_dict_in = {"weight": -2.0} #post-sinaptic current of -2pA
nest.Connect([noise_ex], neuron, syn_spec=syn_dict_ex) #synapse's parameters speficied in synapse dictionary
nest.Connect([noise_in], neuron, syn_spec=syn_dict_in) #that will be integrated with syn_spec
    #synapse parameters: "model", "weight", "delay", "receptor_type" and parameters specific to the chosen synapse model


#<===============================>#
#<==== POPULATION OF NEURONS ====>#
#<===============================>#
import nest
import numpy as np

alphaParams = {"I_e": 200.0, "tau_m": 20.0}
nest.GetDefauls("iaf_psc_alpha") #return default params of the model
nest.SetDefaults("iaf_psc_alpha", alphaParams) #modify default params

neuroPop0 = nest.Create("iaf_psc_alpha", 100) #gives the new params

#copying model to create different branches
edict = {"I_e": 200.0, "tau_m": 20.0}
idict = {"I_e": 300.0}
nest.CopyModel("iaf_psc_alpha", "ex_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "in_iaf_psc_alpha", params=idict)
customParams = [{"I_e": 200.0, "tau_m": 20.0}, {"I_e": 150.0, "tau_m": 30.0}]
exPop0 = nest.Create("exc_iaf_psc_alpha", 100)
inPop0 = nest.Create("inh_iaf_psc_alpha", 30)
exPop1 = nest.Create("exc_iaf_psc_alpha", 5, customParams) #customizing customized model

#creating a dictionary to add randomic values in pop
vTh = -55
vRest = -70
dVms = [{"V_m": vRest+(vTh-vRest)*np.random.rand()} for x in exPop0]
nest.SetStatus(exPop0, dVms) #exPop0 = nest.Create("exc_iaf_psc_alpha", 100, params=dVms)


#<=============================================================>#
#<==== POPULATION OF NEURONS WITH DETERMINISTIC CONNECTIONS ====>#
#<=============================================================>#
import pylab
import nest
pop0 = nest.Create("iaf_psc_alpha", 10, params= {"I_e": 376.0})
pop1 = nest.Create("iaf_psc_alpha", 10)
multimeter = nest.Create("multimeter", 10)
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})

#nest.Connect(pop1, pop2, syn_spec={"weight": 20.0})
nest.Connect(pop1, pop2, "one_to_one", syn_spec={"weight": 20.0}) #nth-neuron of pop1 is connected to nth-neuron of pop2
nest.Connect(multimeter, pop2)                                    #default: "all_to_all"


#<=============================================================>#
#<==== POPULATION OF NEURONS WITH ALEATORY CONNECTIONS ====>#
#<=============================================================>#
import pylab
import nest
pop0 = nest.Create("iaf_psc_alpha", 10, params= {"I_e": 376.0})
pop1 = nest.Create("iaf_psc_alpha", 10)
multimeter = nest.Create("multimeter", 10)

d = 1.0
Je = 2.0
Ke = 20
Ji = -4.0
Ki = 12
conn_dict_ex = {"rule": "fixed_indegree", "indegree": Ke} #fixed_indegree => create "indegree" random connections for each neuron in the target population
conn_dict_in = {"rule": "fixed_indegree", "indegree": Ki}
syn_dict_ex = {"delay": d, "weight": Je}
syn_dict_in = {"delay": d, "weight": Ji}
syn_dict_stdp = {"model": "stdp_synapse", "alpha": 1.0} #models can be inserted in connestion routine too
nest.Connect(pop1, pop0, conn_dict_ex, syn_dict_ex)
nest.Connect(pop0, pop1, conn_dict_in, syn_dict_in)
#"outdegree" works the same, but the connections are randomly selected from the post-sinaptic pop
#indegree more efficient

#fixed_total_numbers creates N connections taking randomly neuron from pre and post sinaptic pop

#pairwise_bernoulli creates every possible connection with a p probability

#autapses => boolean, self connection
#multapses => boolean, multiple connection between 2 neurons


#<=========================>#
#<==== DEVICE BEHAVIOR ====>#
#<=========================>#

#to_memory => data stored over the parameters
#to_file => data stored in an external file, named "label"
recdict = {"to_memory" : False, "to_file" : True, "label" : "epop_mp"}
mm1 = nest.Create("multimeter", params=recdict)

nest.ResetKernel() #gets rid of all nodes you have created, any customised models you created, and resets the internal clock to 0.
nest.ResetNetwork() #resets all nodes to their default configuration and wipes the data from recording devices.


#<======================================>#
#<==== PARAMETRISING SYNAPSE MODELS ====>#
#<======================================>#
import nest
nest.Models(synapses) #available Models
#like neuron models
nest.SetDefaults("stdp_synapse",{"tau_plus": 15.0})
nest.CopyModel("stdp_synapse","layer1_stdp_synapse",{"Wmax": 90.0})

#spike-timing dependent plastic synapsis params can't be setted with setDefaults => params of pre-post synaptic neurons
nest.Create("iaf_psc_alpha", params={"tau_minus": 30.0})

#distributing params
alpha_min = 0.1
alpha_max = 2.
w_min = 0.5
w_max = 5.
#they go to the syn dictionary, then in the connect routine
syn_dict = {"model": "stdp_synapse",
            "alpha": {"distribution": "uniform", "low": alpha_min, "high": alpha_max}, #different distribution, each with its key
            "weight": {"distribution": "uniform", "low": w_min, "high": w_max}, #see docs
            "delay": 1.0}
nest.Connect(epop1, neuron, "all_to_all", syn_dict)

#querying synapses
#nest.GetConnections(presynaptic pop, postsynaptic pop, synaptic model) => returns a list of connection identifiers that match the given specifications
import pylab
import nest
pop0 = nest.Create("iaf_psc_alpha", 10, params= {"I_e": 376.0})
pop1 = nest.Create("iaf_psc_alpha", 10)

syn_dict = {"model": "stdp_synapse",
            "alpha": {"distribution": "uniform", "low": alpha_min, "high": alpha_max}, #different distribution, each with its key
            "weight": {"distribution": "uniform", "low": w_min, "high": w_max}, #see docs
            "delay": 1.0}

nest.Connect(pop1, pop0, "all_to_all", syn_dict)

conns = nest.GetConnections(pop1, synapse_model="stdp_synapse")
conn_vals = nest.GetStatus(conns, ["target", "weight"]) #nest.GetStatus is used to extract data from the GetConnections array (in this case only the "target" and "weight")

#<==============================>#
#<==== NEST TOPOLOGY MODULE ====>#
#<==============================>#
