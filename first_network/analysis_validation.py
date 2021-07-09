import numpy as np
import nest
from modules.models import LineForChart
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "simple_white" # Sets the plotly default theme

import modules.simulation as sim
t = 1000.0
net = LineForChart()
single = LineForChart()
input_fr = np.logspace(3, 8, 8, base = 2.0)

for i in input_fr:
    nest.ResetKernel()
    sim.initKernel()
    input_curr, neuron_pop, spikeDet = sim.create_network(p = .0, n = 300, n_excited = 300, input_rate = i)
    nest.Simulate(t)
    spikes = sim.extract_spikes(spikeDet)
    net.y.append(spikes[:,0].size)
    net.x.append(i)

    nest.ResetKernel()
    sim.initKernel()
    input_spikes = np.round(np.linspace(0, t, int(t / 1000 * i)) + 0.1, 1)
    input_curr = nest.Create("spike_generator", params = {"spike_times": input_spikes})
    print(input_spikes)
    print("len", input_spikes.size)
    neuron = nest.Create("leaky_i_f")
    spikeDet2 = nest.Create("spike_detector", params = {"withgid": True, "withtime": True})
    nest.Connect(input_curr, neuron)
    nest.Connect(neuron, spikeDet2)
    nest.Simulate(t)
    spikes2 = sim.extract_spikes(spikeDet2)
    single.y.append(spikes2[:,0].size)
    single.x.append(i)
    var = nest.GetStatus(spikeDet2)[0]["events"]
    print("single Y", var["senders"])

fig = go.Figure()
fig.add_trace(go.Scatter(x= net.x, y= net.y, mode='lines+markers'))
fig.update_layout(xaxis_title="time (ms)", yaxis_title= "output (Hz)", title="Network")
fig.show()
fig.write_image('validation/net.png')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x= single.x, y= single.y, mode='lines+markers'))
fig2.update_layout(xaxis_title="input (Hz)", yaxis_title= "output (Hz)", title="Single Cell")
fig2.show()
fig2.write_image('validation/single.png')