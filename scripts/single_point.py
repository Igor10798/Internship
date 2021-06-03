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
    return nest.Create("leaky_i_f", params= param)

#setting parameter
time = 1000.0
trials = range(1001)
frequencies = []

params = {
    "t_ref": 1.59,
    "C_m": 14.6,
    "E_L": -65.0,
    "tau_syn_ex": 0.64,
    "tau_syn_in": 2.0
}

for trial in trials:
    nest.ResetKernel()
    #creating neuron
    nest.CopyModel("amat2_psc_exp", "leaky_i_f", params=params)
    neuron = create()
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
