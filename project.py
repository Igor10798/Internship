"""
<=====================>
<==== BASIC LEVEL ====>
<=====================>
"""
import nest

#setting params
edict = {"I_e": 200.0, "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha")
exc_syn_dic = {"weight": 20.0}
inh_syn_dic = {"weight": -30.0}

#populations
excNeuronPop1 = nest.Create("exc_iaf_psc_alpha", 30) 
excNeuronPop2 = nest.Create("exc_iaf_psc_alpha", 30)
inhNeuronPop = nest.Create("inh_iaf_psc_alpha", 15)
#Even changin input of exc pops, I couldn't find any dinamics

#connections
Ke = .5
Ki = 2.0
conn_dict_ex = {"rule": "fixed_indegree", "indegree": Ke}
conn_dict_in = {"rule": "fixed_indegree", "indegree": Ki}

nest.Connect(excNeuronPop1, inhNeuronPop, syn_spec= exc_syn_dic)
nest.Connect(excNeuronPop2, inhNeuronPop, syn_spec= exc_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop1, syn_spec= inh_syn_dic)
nest.Connect(inhNeuronPop, excNeuronPop2, syn_spec= inh_syn_dic)

#recordings && simulation
multimeter1 = nest.Create("multimeter", params= {"withtime": True, "record_from":["V_m"]})
multimeter2 = nest.Create("multimeter", params= {"withtime": True, "record_from":["V_m"]})
multimeter_inh = nest.Create("multimeter", params= {"withtime": True, "record_from":["V_m"]})
nest.Connect(multimeter1, excNeuronPop1)
nest.Connect(multimeter2, excNeuronPop2)
nest.Connect(multimeter_inh, inhNeuronPop)

nest.Simulate(1000.0)

#plots
import plotly.express as px

dmm1 = nest.GetStatus(multimeter1, keys= "events")[0]
Vms1 = dmm1['V_m']
ts1 = dmm1["times"]
plot1 = px.line(x=ts1, y=Vms1, labels={'x': 't', 'y': 'Vm1'})
plot1.show()

dmm2 = nest.GetStatus(multimeter2, keys= "events")[0]
Vms2 = dmm2["V_m"]
ts2 = dmm2["times"]
plot2 = px.line(x=ts2, y=Vms2, labels={'x': 't', 'y': 'Vm2'})
plot2.show()

dmm_inh = nest.GetStatus(multimeter_inh, keys= "events")[0]
Vms_inh = dmm_inh["V_m"]
ts_inh = dmm_inh["times"]
plot3 = px.line(x=ts_inh, y=Vms_inh, labels={'x': 't', 'y': 'Vm_inh'})
plot3.show()