import nest
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

#setting working directory path
root= r"C:\\Users\\Utente\\GIT\\internship\\images"
if not os.path.exists(root):
    os.mkdir(root)
os. chdir(root)

def create(param= None):
    return nest.Create("leaky_i_f", params= param)
def addTrace(y_graph, name_graph, color_graph):
    plot2.add_trace(go.Scatter(x= g_Ls, y=y_graph, name= name_graph, marker=dict(color=color_graph) , mode="markers"))

#setting parameter
time = 1000.0
trials = range(1001)
x= 0
y = 101
rheobase_freqs = []
freqs_350 = []
freqs_500 = []
freqs_750 = []
freqs_1000 = []
g_Ls = []

while x < y:
    frequencies = []
    g_L = 1.0 + x
    params = {
        "t_ref": 1.59,
        "C_m": 14.6,
        "V_th": -60.0,
        "V_reset": -78.0,
        "E_L": -66.0,
        "tau_syn_ex": 0.64,
        "tau_syn_in": 2.0,
        "g_L": g_L
    }

    for trial in trials:
        nest.ResetKernel()
        #creating neuron
        nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)
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
        ni = 1000 * ni / time
        frequencies.append(ni)
    #recording values
    n = 0
    for i in range(len(frequencies)):
        if frequencies[i] != 0.0:
            while n == 0:
                rheobase_freqs.append(i)
                n = len(rheobase_freqs)
                break
        else:
            if i == (len(frequencies) - 1):
                    rheobase_freqs.append(None)

    freq_at_350 = frequencies[350]
    freq_at_500 = frequencies[500]
    freq_at_750 = frequencies[750]
    freq_at_1000 = frequencies[1000]
    freqs_350.append(freq_at_350)
    freqs_500.append(freq_at_500)
    freqs_750.append(freq_at_750)
    freqs_1000.append(freq_at_1000)
    g_Ls.append(g_L)

    x += 1

print(g_Ls)
print(rheobase_freqs)
print(freqs_350)
print(freqs_500)
print(freqs_750)
print(freqs_1000)
    
#setting plots
plot1 = px.scatter(x= g_Ls, y= rheobase_freqs, labels={'x': 'Leak conductance', 'y': 'Rheobase frequency'})
plot2 = px.scatter(labels={'x': 'Leak conductance', 'y': 'Spike/s'})
addTrace(freqs_350, "350Hz", "rgba(38, 250, 1, .5)")
addTrace(freqs_500, "500Hz", "rgba(250, 220, 0, .5)")
addTrace(freqs_750, "750Hz", "rgba(2, 35, 250, .5)")
addTrace(freqs_1000, "1000Hz", "rgba(255, 16, 0, .5)")

#plotting
plot1.show()
plot2.show()


#save imgs
plot1.write_image("rheobase_freq.png")
plot2.write_image("spike_s_freqs.png")