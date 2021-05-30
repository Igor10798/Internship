# Internship

### 30/05/2021
I read PyNest official tutorials (https://nest-simulator.readthedocs.io/en/nest-2.20.1/tutorials/index.html) and, using those info, I want to build a simple network where 2 excitatory populations receive the same input and spike on 1 inhibitory, trying to see how the competition takes place. <br>
Below you can find a scheme of the network.

![alt text](https://github.com/Igor10798/Internship/blob/master/images/01.png)


###### 1. Basic level
I build the network with deterministic connections and synapses, I expect the same behavior from the excitatory populations
###### 2. Aleatory connectivity
I build the network with aleatory connections but without synaptic plasticity, one network may be stronger than the other
###### 3. STDP synapses
I build the network with aleatory connections and synaptic plasticity, I expect different behavior depending on what population fires firstly on the inhibitory one.
