import nest
import plotly.express as px
import plotly.io as pio

#network setting
def create_network(n=300, p=.003):
    n = 300 #neurons
    p = .003 #connection probability
    n_recorded = 50 #neuron recorded
    n_excited = 20 #neuron excited by input
    conn_dict = {"rule": "pairwise_bernoulli", "p": p}
    weight = 5.0
    syn_dict = {"model": "stdp_synapse", "weight": weight}
    #simulation setting
    scale_size = 1000.0
    time = 10.0 * scale_size
    rec_dic = {"rule": "fixed_total_number", "N": n_recorded}
    #neuron model
    params = {
        "t_ref": 1.59,
        "C_m": 14.6,
        "V_th": -60.0,
        "V_reset": -78.0,
        "E_L": -66.0,
        "tau_syn_ex": 0.64,
        "tau_syn_in": 2.0
    }
    nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)
    #input
    input_dict = {"rate": 150.0}
    input_conn = {"rule": "fixed_total_number", "N": n_excited}

    nest.ResetKernel()
    nest.CopyModel("aeif_cond_alpha", "leaky_i_f", params=params)

    #building network
    input_curr = nest.Create("poisson_generator", params = input_dict)
    neuron_pop = nest.Create("leaky_i_f", n, params = params)

    nest.Connect(input_curr, neuron_pop, input_conn) #input
    nest.Connect(neuron_pop, neuron_pop, conn_dict, syn_spec= syn_dict) #inter-network connections
    #recording
    spikeDet = nest.Create("spike_detector", params = {"withgid": True, "withtime": True})
    nest.Connect(neuron_pop, spikeDet)
    #simulating
    nest.Simulate(time)

    #recording vars
    var = nest.GetStatus(spikeDet, keys = "events")
    print(var)
    spikes = var[0]["senders"]
    spike_freq = spikes * scale_size / time
    t = var[0]["times"]
    #plotting
    pio.templates.default = "simple_white" # Sets the plotly default theme
    plot = px.scatter(x = t, y = spike_freq, labels = { 'x': 'time (ms)', 'y': 'spike frequency (Hz)' })
    plot.show()
    #plot.write_image("plots/rheobase_freq_noprop.png")
    plot.write_image("plots/rheobase_freq_prop.png")
    #plot.write_image("plots/rheobase_freq_highprop.png")

create_network()
