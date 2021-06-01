import nest

class StructuralPlasticityNet():

    def __init__(self):
        self.exc_n = 800
        self.inh_n = 200
        # Structural_plasticity properties
        self.update_interval = 1000
        self.dt = .1
        # rate of background Poisson input
        self.bg_rate = 10000.0 #he used high frequency, should I change it?

        # Excitatory synaptic elements of Excitatory neurons && Inhibitory synaptic elements of Excitatory neurons
        self.g_rate = .0001
        self.eps = .05
        self.growth_curve_e_e = self.growth_curve_e_i = self.growth_curve(self.g_rate, self.eps)
        # Inhibitory synaptic elements of Inhibitory neurons
        self.eps = .2
        self.growth_curve_i_i = self.growth_curve(self.g_rate, self.eps)
        # Excitatory synaptic elements of Inhibitory neurons
        self.g_rate = .0004
        self.growth_curve_i_e = self.growth_curve(self.g_rate, self.eps)

        self.model_params = {
            'tau_m': 10.0,  # membrane time constant (ms)
            'tau_syn_ex': .5, # excitatory synaptic time constant (ms)
            'tau_syn_in': .5, # inhibitory synaptic time constant (ms)
            't_ref': 2.0,  # absolute refractory period (ms)
            'E_L': -65.0,  # resting membrane potential (mV)
            'V_th': -50.0,  # spike threshold (mV)
            'C_m': 250.0,  # membrane capacitance (pF)
            'V_reset': -65.0  # reset potential (mV)
        }

        self.nodes_e = None
        self.nodes_i = None
        self.mean_ca_e = []
        self.mean_ca_i = []
        self.total_connections_e = []
        self.total_connections_i = []

        self.psc_d = 1.0
        self.psc_e = 585.0
        self.psc_i = -585.0
        self.psc_ext = 6.2

        #model connectivity
        self.alpha_min = .1
        self.alpha_max = 3.
        self.w_mean = 15.0
        self.w_dev = 1.0
        self.ratio = -5.0 #inh/exc weigth ratio
        self.w_mean_in = self.ratio * self.w_mean

        self.syn_dict_ex = {
            "model": "stdp_synapse",
            "alpha": {"distribution": "uniform", "low": self.alpha_min, "high": self.alpha_max},
            "weight": {"distribution": "normal", "mu": self.w_mean, "sigma": self.w_dev},
            "Wmax": 100.0
        }
        self.syn_dict_in =   {
            "model": "stdp_synapse",
            "alpha": {"distribution": "uniform", "low": self.alpha_min, "high": self.alpha_max},
            "weight": {"distribution": "normal", "mu": self.w_mean_in, "sigma": self.w_dev},
            "Wmax": -100.0
        }
        
        self.conn_dict_str = {"rule": "pairwise_bernoulli", "p": .6}
        self.conn_dict_weak = {"rule": "pairwise_bernoulli", "p": .4}
        self.conn_dict_in = {"rule": "pairwise_bernoulli", "p": .6}

        #initializing network
        self.prepare_simulation()
        self.create_nodes()
        self.connect_external_input()
    
    def prepare_simulation(self):
        #simulation functions
        nest.ResetKernel()
        nest.set_verbosity('M_ERROR')
        nest.SetKernelStatus({ 'resolution': self.dt })
        nest.SetStructuralPlasticityStatus({ 'structural_plasticity_update_interval': self.update_interval })

        #creating personalized models
        nest.CopyModel('static_synapse', 'synapse_ex')
        nest.SetDefaults('synapse_ex', {'weight': self.psc_e, 'delay': self.psc_d})
        nest.CopyModel('static_synapse', 'synapse_in')
        nest.SetDefaults('synapse_in', {'weight': self.psc_i, 'delay': self.psc_d})
        nest.SetStructuralPlasticityStatus({
            'structural_plasticity_synapses': {
                'synapse_ex': {
                    'model': 'synapse_ex',
                    'post_synaptic_element': 'Den_ex',
                    'pre_synaptic_element': 'Axon_ex',
                },
                'synapse_in': {
                    'model': 'synapse_in',
                    'post_synaptic_element': 'Den_in',
                    'pre_synaptic_element': 'Axon_in',
                },
            }
        })

    def growth_curve(self, rate, eps):
        return {
            'growth_curve': "gaussian",
            'growth_rate': rate,  # (elements/ms)
            'continuous': False,
            'eta': .0,  # Ca2+
            'eps': eps,  # Ca2+
        }

    def create_nodes(self):
        synaptic_elements = {
            'Den_ex': self.growth_curve_e_e,
            'Den_in': self.growth_curve_e_i,
            'Axon_ex': self.growth_curve_e_e,
        }

        synaptic_elements_i = {
            'Den_ex': self.growth_curve_i_e,
            'Den_in': self.growth_curve_i_i,
            'Axon_in': self.growth_curve_i_i,
        }

        self.nodes_e = nest.Create('iaf_psc_alpha', self.exc_n, { 'synaptic_elements': synaptic_elements })
        self.nodes_i = nest.Create('iaf_psc_alpha', self.inh_n, { 'synaptic_elements': synaptic_elements_i })
        nest.SetStatus(self.nodes_e, 'synaptic_elements', synaptic_elements)
        nest.SetStatus(self.nodes_i, 'synaptic_elements', synaptic_elements_i)

    def connect_external_input(self):
        noise = nest.Create('poisson_generator')
        nest.SetStatus(noise, {"rate": self.bg_rate})
        nest.Connect(noise, self.nodes_e, 'all_to_all', { 'weight': self.psc_ext, 'delay': 1.0 })
        nest.Connect(noise, self.nodes_i, 'all_to_all', { 'weight': self.psc_ext, 'delay': 1.0 })
        
    def connect_nodes(self, incoming= None, outcoming = None, conn_dict_ex = None, syn_dict_ex = None, conn_dict_in = None, syn_dict_in = None):
        if conn_dict_ex is None:
            conn_dict_ex = self.conn_dict_str
        if syn_dict_ex is None:
            syn_dict_ex = self.syn_dict_ex
        if conn_dict_in is None:
            conn_dict_in = self.conn_dict_in
        if syn_dict_in is None:
            syn_dict_in = self.syn_dict_in
        if incoming is not None:
            nest.Connect(incoming, self.nodes_e, conn_dict_ex, syn_spec= syn_dict_ex)
        nest.Connect(self.nodes_e, self.nodes_i, self.conn_dict_weak, syn_spec= self.syn_dict_ex)
        if outcoming is not None:
            nest.Connect(self.nodes_i, outcoming, conn_dict_in, syn_spec= syn_dict_in)

#building network
incoming = StructuralPlasticityNet()
incoming.connect_nodes()

outcoming = StructuralPlasticityNet()
outcoming.connect_nodes()

plastic = StructuralPlasticityNet()
plastic.connect_nodes(incoming.nodes_e, outcoming.nodes_e) #THIS DOESN'T WORK => THEY PLOT THE SAME NETWORK

#recording data && simulation
def createDevice(n):
    return nest.Create("spike_detector", n, params={"withgid": True, "withtime": True})

spikeDet_incoming_ex = createDevice(incoming.exc_n)
spikeDet_incoming_in = createDevice(incoming.inh_n)
spikeDet_outcoming_ex = createDevice(outcoming.exc_n)
spikeDet_outcoming_in = createDevice(outcoming.inh_n)
spikeDet_plastic_ex = createDevice(plastic.exc_n)
spikeDet_plastic_in = createDevice(plastic.inh_n)

nest.Connect(incoming.nodes_e, spikeDet_incoming_ex)
nest.Connect(incoming.nodes_i, spikeDet_incoming_in)
nest.Connect(outcoming.nodes_e, spikeDet_outcoming_ex)
nest.Connect(outcoming.nodes_i, spikeDet_outcoming_in)
nest.Connect(plastic.nodes_e, spikeDet_plastic_ex)
nest.Connect(plastic.nodes_i, spikeDet_plastic_in)

nest.Simulate(1000.0)

#plotting simulation
import plotly.express as px

dmm1 = nest.GetStatus(spikeDet_incoming_ex, keys= "events")[0]
spikes1 = dmm1['senders']
ts1 = dmm1["times"]
plot1 = px.scatter(x=ts1, y=spikes1, labels={'x': 't', 'y': 'spikes neuron exc input pop'})
plot1.show()

dmm2 = nest.GetStatus(spikeDet_incoming_in, keys= "events")[0]
spikes2 = dmm2['senders']
ts2 = dmm2["times"]
plot2 = px.scatter(x=ts2, y=spikes2, labels={'x': 't', 'y': 'spikes neuron inh input pop'})
plot2.show()

dmm3 = nest.GetStatus(spikeDet_outcoming_ex, keys= "events")[0]
spikes3 = dmm3['senders']
ts3 = dmm3["times"]
plot3 = px.scatter(x=ts3, y=spikes3, labels={'x': 't', 'y': 'spikes neuron exc output pop'})
plot3.show()

dmm4 = nest.GetStatus(spikeDet_outcoming_in, keys= "events")[0]
spikes4 = dmm4['senders']
ts4 = dmm4["times"]
plot4 = px.scatter(x=ts4, y=spikes4, labels={'x': 't', 'y': 'spikes neuron inh output pop'})
plot4.show()

dmm5 = nest.GetStatus(spikeDet_plastic_ex, keys= "events")[0]
spikes5 = dmm5['senders']
ts5 = dmm5["times"]
plot5 = px.scatter(x=ts5, y=spikes5, labels={'x': 't', 'y': 'spikes neuron exc middle pop'})
plot5.show()

dmm6 = nest.GetStatus(spikeDet_plastic_in, keys= "events")[0]
spikes6 = dmm6['senders']
ts6 = dmm6["times"]
plot6 = px.scatter(x=ts6, y=spikes6, labels={'x': 't', 'y': 'spikes neuron inh middle pop'})
plot6.show()