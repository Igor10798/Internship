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

###  14/06/2021 stats.py (https://github.com/Igor10798/Internship/blob/7057349e4946615abed763c4e6dbf7e429addf64/stats.py#L35-L43)
After the work in the lab where I learnt how to plot linear regression, I tried to drop "zero values"  
From the plot where the R^2 index was low to see if the linear relationship explained that pattern. Sincce the R^2 value was .9, I can conclude that there is a linear relationship between leak conductance and spike/s, and the input frequency is not a mediator of this relationship.

Now I am going to plot data in csv format and analize them with JASP && Rstudio.
###### 20/06/2021 recap of first findings (https://github.com/Igor10798/Internship/tree/master/stats/data/plot%20Rstudio)
I had a first analysis of the data using RStudio. You can find the plot in the folder above, where I plotted the main diagnostic plots of the regression, and in a `.txt` file I gathered all R^2 values in order to assess whether a linear of logarithmic regression was better.  
Here I am going to analyze only a dataset as an example.  
In the case of `rheobase frequency`, the coefficient of determination was significantly higher in case of linear regression, so I analyzed deeper only that casistic (https://github.com/Igor10798/Internship/tree/master/stats/data/plot%20Rstudio/rheobase).  
From the residuals graph we can see that residuals are not randomly dinstributed, so a linear model may not fit very well this dinstribution, despite a high value of R^2.  
![alt text](https://github.com/Igor10798/Internship/blob/master/stats/data/plot%20Rstudio/rheobase/residual-fitted.png)  
From the Scale-Location plot, we can check if the homoscedasticity assumption is violated, which seems to be the case of our model: the variance of population are not equal  
![alt text](https://github.com/Igor10798/Internship/blob/master/stats/data/plot%20Rstudio/rheobase/std%20residual-fitted.png)  
From the residuals-leverage plot, we can search for high Leverage points and for outliers. We may define an outlier a data whose std residual is 3 standard far from the mean, while we may define a leverage as the distance of the X value of an observation from the others. The former are data that are not in line with other observation (to check if there are some problems with the model), the latter are data that have a greater effects on determining the regression. We have to be careful and check what data are outlier and what are high leverage points, and what are both (i.e. `influence ponts`).  
From the graph below we can see that there are no outliers nor high leverage points, since all points are far away from the Cook distance.  
![alt text](https://github.com/Igor10798/Internship/blob/master/stats/data/plot%20Rstudio/rheobase/residual-leverage.png)  

From this analysis we can conclude that there are not data to not consider in order to enhanche the predictive power of the model, but the distribution doesn't meet some assumption of linear regression (i.e. homoscedasticity and linearity), so the model clearly cannot fit the data. Maybe the use of a GLM could explain better these data.

###### 21/06/2021 Trying to fix heteroscedasticity
I used `weighted least square regression` trying to fix heteroscedasticity while maintaining "simple" regression. I'll bring here an example on the ○`750Hz input`. Using weights (i.e. `lm(abs(model$residuals) ~ model$fitted.values)$fitted.values^2`) in order to make residuals more plain, I enhanced the coefficient of determination (from .8977 to .9378), and by using a non linear model (hence we previously found out that the linearity was missing) (i.e. `V1 ~ 1/V2 + log(V2)`) it becomes .962.  
Despite the enhancement of R^2, from the Scale-Location plot we can still notice a pattern composed by residuals, and performing a `var.test` will confirm the heteroscedasticity.  
[!There have been some problems! Click for the image](https://github.com/Igor10798/Internship/blob/master/stats/data/plot%20Rstudio/750Hz%20wls/scale-location.png)

### 16/06/2021 script.py (https://github.com/Igor10798/Internship/blob/master/first_network/script.py)
I am going to investigate the importance of weight magnitude and number of random connection between neurons in a single population of LIF neuron, how they influence the output of the network (spikes/s) and how their relationship.  
I am going to compile a report with my findings and try to understand the nature of these relationships.
###### 20/06/2021 recap of first findings
From my code I got a step function looking at how outcome varies in function of probability of connection  
  ![alt text](https://github.com/Igor10798/Internship/blob/master/first_network/params_variability/probability.png)  
*Labels are wrong but it was just a test plot, because when weights vary I cannot see spikes for every weight I assign to the network.*  
From this plot I may infer that there are cluster of probability that makes the network behave differently (e.g. `[0, .035]` && `(.035, 0.14]`). This remarks the importance to investigate how probability interacts with other network parameters: supposing an exponential mediation of probability in weights/output relationship, the lower part of a step may influence less the output, while the upper part may influence it more.  
I plotted output in function of weights (w) variation (from 1 to 100).  
![alt text](https://github.com/Igor10798/Internship/blob/master/first_network/params_variability/weight.png)  
As you can see from the image it only display output for `w = 2^x`. Trying to investigate why this happens, I printed the total spikes recorded by the device, and it recorded spikes only for w values indicates above and plotted in the image. Since, using the same code probability was plotted for every value of p, I feel to exclude that how the loop was set causes this problem.  
Investigating further, I tried to plot the missing values (i.e. w belonging to [33, 63] && [65, 100]). The plots only show an output for the first value of the sets of w.  
![alt text](https://github.com/Igor10798/Internship/blob/master/first_network/params_variability/weight_33to63.png)  
![alt text](https://github.com/Igor10798/Internship/blob/master/first_network/params_variability/weight_65to100.png)  
###### 21/06/2021 News
Although I did some code refactoring, I couldn't find the error. While waiting, I added a function that gives to the neuron of the newtork the `STDP synapse model`, comparing the outputs from a non-plastic and from a plastic network for different weights. (https://github.com/Igor10798/Internship/tree/master/first_network/plasticity)  
Unexpectedly, these plots don't differ at all. Maybe setting fixed weights force static connections in the network (with the given strenght). I will try to vary the connectivity instead, to check if I obtain different results.

### 24/06/2021 Code refactoring of `first_network` (https://github.com/Igor10798/Internship/tree/master/first_network)
###### Dir structure
As suggested in issue #11, I simplified my code giving it a modular structure. It follows an explanation about how the folder is structured.  
- `./collect_data.py` is the main script, where I use all the modules in order to run the simulation and store my data. (https://github.com/Igor10798/Internship/blob/master/first_network/collect_data.py)  
- `./analysis.py` contains the script where I do my offline analysis (in this case just the plots) (https://github.com/Igor10798/Internship/blob/master/first_network/analysis.py)  
- `./params_interaction` is the folder where my plots will be saved (https://github.com/Igor10798/Internship/tree/master/first_network/params_interaction)  
- `./modules` is the folder where you can find my modules (`graph.py` for the charts, `simulation.py` with my simulations script and `models.py` for my object models) (https://github.com/Igor10798/Internship/tree/master/first_network/modules)  
- `./offline_analysis` is the folder where I stored my pkl file (and maybe some Rstudio plot in the future) (https://github.com/Igor10798/Internship/tree/master/first_network/offline_analysis)

###### Online analysis (https://github.com/Igor10798/Internship/blob/master/first_network/collect_data.py)
I wrote a script that runs the simulation varying weights `w` and probability of connection `p`. For every value of `w` it runs a simulation per every value of `p`.  
For every `w` I stored the maximum `p` value where my outcome was `dead_prop`, `constant_prop` or `exploded_prop`.  
I planned, as suggested in #10, to plot every outcome in order to check if the storage of data for the main chart was correct. To do so, I created an object that collects all the outcomes (spikes/s) and their times, labelling them as `dead_prop`, `constant_prop` or `exploded_prop`. I create an istance of this object for every `p` value in every `w`.

### 02/07/2021
After the work in the lab I updated `g_L in aeif_cond_alpha model` (https://github.com/Igor10798/Internship/blob/master/g_L_investigation/g_L_in_aeif_cond_alpha_CORRECTED.docx) with statistical analysis I showed (here in https://github.com/Igor10798/Internship#14062021-statspy-httpsgithubcomigor10798internshipblob7057349e4946615abed763c4e6dbf7e429addf64statspyl35-l43).  
I completed the offline analysis in the `first_network` directory: I exported the raw data (spikes/s, weight and probability of connection) for further analysis with RStudio in order to determine the relationship. I plotted a stacked area graph where the interaction is qualitatively evident.

### 05/07/2021
I started analyzing data on RStudio (https://github.com/Igor10798/Internship/blob/master/first_network\offline_analysis\plot_rstudio\first_set_params).  
I unfortunately found that starting from the first values of my set of `weights`, for every `p` value of connectivity, the output of the network reaches very high values and stabilizes itself.  
My interpretation is that the sets of weights and connectivity I used (https://github.com/Igor10798/Internship/blob/ee54029711086ce6ced0509ce9961212c206f504/first_network/collect_data.py#L25-L27) were too big, the signal exploded and reached the maximum output obtainable (i.e. every neuron connected fires). Since this extreme condition won't give information about the relationship between `w`, `p` and the output, I will make other simulations with different sets of parameters.