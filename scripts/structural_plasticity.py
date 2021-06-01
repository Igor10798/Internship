import nest

class StructuralPlasticityNet():

    def __init__(self):
        self.time = 200000.0   # simulation time
        self.dt = .1 #resolution time update
        self.exc_n = 800
        self.inh_n = 200
        # Structural_plasticity properties
        self.update_interval = 1000
        self.record_interval = 1000
        # rate of background Poisson input
        self.bg_rate = 10000.0

        self.model_n = 'iaf_psc_exp'

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


example = StructuralPlasticityNet()
example.prepare_simulation()
example.create_nodes()
example.connect_external_input()