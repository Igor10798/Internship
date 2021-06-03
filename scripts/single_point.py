import nest
import plotly.express as px
import numpy as np
import os

#setting working directory path
root= r"C:\Users\Utente\GIT\internship\images\single_point_Vm"
if not os.path.exists(root):
    os.mkdir(root)
os. chdir(root)

def create(param= None):
    return nest.Create("basket_cell", params= param)

#setting parameter
time = 1000.0
trials = range(1001)
frequencies = []

params = {
    "t_ref": 1.59,
    "C_m": 14.6,
    "V_th": -53.0,
    "V_reset": -78.0,
    "E_L": -68.0,  
    "I_e": 24.05,
    "tau_syn_ex": 0.64,
    "tau_syn_in": 2.0,
    "g_L": 1.6
}

syn_params = {
}

for trial in trials:
    nest.ResetKernel()
    #creating neuron
    nest.CopyModel("iaf_cond_alpha", "basket_cell", params=params)
    neuron = create({"I_e": .0, "g_L": 1.4})
    #input
    input_current = nest.Create("poisson_generator", params={"rate": float(trial)})
    nest.Connect(input_current, neuron)
    #recording
    spikeDet = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    nest.Connect(neuron, spikeDet)
    #simulating
    nest.Simulate(time)
    
    #collecting spykes/s (here total number)
    ni = len(nest.GetStatus(spikeDet, keys="events")[0]["senders"])
    #frequency
    ni = ni / (time / 1000)
    frequencies.append(ni)
#plot
plot2 = px.scatter(x=trials, y=frequencies, labels={'x': 'frequency input', 'y': 'Spikes per second'})
plot2.show()
