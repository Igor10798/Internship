# Internship

### 30/05/2021 - first_network.py
I read PyNest official tutorials (https://nest-simulator.readthedocs.io/en/nest-2.20.1/tutorials/index.html) and, using those info, I want to build a simple network where 2 excitatory populations receive the same input and spike on 1 inhibitory, trying to see how the competition takes place. <br>
Below you can find a scheme of the network.

![alt text](https://github.com/Igor10798/Internship/blob/master/images/01.png)


###### 1. Basic level
I build the network with deterministic connections and synapses, I expect the same behavior from the excitatory populations
###### 2. Aleatory connectivity
I build the network with aleatory connections but without synaptic plasticity, one network may be stronger than the other
###### 3. STDP synapses
I build the network with aleatory connections and synaptic plasticity, I expect different behavior depending on what population fires firstly on the inhibitory one.
###### Description of procedure
I used info from the tutorial linked above and I look at some examples online for setting some parameter (e.g. https://www.nest-simulator.org/py_sample/brunel_delta_nest/ && https://www.nest-simulator.org/py_sample/structural_plasticity/).<br>
I did not observe the expected behavior (I guess it is because the logic works if they are single neuron and not populations of neurons (?) || because of the exteral inputs), so I played with some parameters to see how the network answered to modifications (I changed inputs, both in the model of the neuron and with external device, randomization of V_m, delays and tau_syn) I changed also some parameters for connections (probability of bernoulli distribution) and for synapses (weight and alpha). <br>
I looked at the documentation for the meaning of the parameters and for the list of all of them, and I got them even from the code through nest.GetStatus && nest.GetDefault.

I differentiated the inputs during the simulation because in this way I could see the different effect they had on the inhibitori population (with weaker inputs the inhibitory effect is stronger). I don't know what kind of parameter is realistic, I sacrificed realism in setting them in order to obtain certain behaviors.


### 31/05/2021 - structural_plasticity.py
I looked at a structural plasticity network (https://www.nest-simulator.org/py_sample/structural_plasticity/) and I want to use that class with some modifications in order to build a small network where structural plasticity is enabled. <br>
I looked in the docs the functions I did not know and I used the chance to look at the functions related to the simulation in the docs (https://nest-simulator.readthedocs.io/en/nest-2.20.1/ref_material/pynest_apis.html?highlight=resetkernel#module-nest.lib.hl_api_simulation), implementing them in the first_project.py file in order to run multiple simulations.

I added a function to the class that should let you to add connection and insert that plastic network in a bigger one. <br>
I read about RNG (https://nest-simulator.readthedocs.io/en/v2.18.0/guides/random_numbers.html?highlight=randomize) and how to properly randomize value, and I tried it with V_m.
###### Comments
I could not find in the docs the property "synaptic_elements" for the "iaf_psc_alpha" object, so I could not understand how it works... Maybe I can add new properties to neurons (?)

### 31/05/2021 - single_point.py
I studied the response of an integrate and fire neuron to an input varying in frequency. <br>
I then repeated the procedure to see how a leaky integrate and fire neuron would response, and I tried to vary the stimulus for amplitude and frequency.

###### Comments
I do not understand why my neuron reacted in a so different way if a vary the frequency of the input and the `E_L` property is setted as `-65.0` rather than `-65.3` (Vm is reported in the file name of the plots)  
**Updates**  
In order to investigate this problem I added a while loop and I run the simulations for `E_L` values varying from `-66.0` to `-64.0`. I found that the pattern I saw belongs to a bigger pattern of behavior of leaky integrate and fire neuron: I suppose that with too high `E_L` their behavior becomes more and more similar to an integrate and fire neuron (a sort of proto-linear relationship between spyke/second and frequency of the input), while if `E_L` is too low the neuron doesn't spyke.  
It seems that the hyperbolic graph is at a middle point between 2 linear graphs, where this curve is flatted (horizontaly if neuron doesn't spyke, inclined if for high `E_L` values).

I propose that the best `E_L` value in this model is `-65.4 mV`. Here the rheobase frequency is of about 400Hz.

###  14/06/2021 stats.py
After the work in the lab where I learnt how to plot linear regression, I tried to drop "zero values" (https://github.com/Igor10798/Internship/blob/7057349e4946615abed763c4e6dbf7e429addf64/stats.py#L35-L43) from the plot where the R^2 index was low to see if the linear relationship explained that pattern. Sincce the R^2 value was .9, I can conclude that there is a linear relationship between leak conductance and spike/s, and the input frequency is not a mediator fo this relationship.