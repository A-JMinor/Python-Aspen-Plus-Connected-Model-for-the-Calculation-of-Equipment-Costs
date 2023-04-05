# Function Details

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. Furthermore, all heat exchangers in Aspen Plus must be named according to E01, E02, E03, .. etc in the Aspen Plus simulation. 

This function called "heatexchanger" in the HeatExchanger.py file decides about the type of heat exchanger according to heuristics of Seider et al. (2008) and gives as output the sum of the current costs of all heat exchangers present in the simulation (*E_totalcosts*), the current costs of the individual heat exchangers (array *E_purchase_costs_current*), the heat exchanger duties (array *E_Q*) of the individual heat exchangers as well as the required heat exchanger areas of the individual heat exchangers (array *E_area*). As input required is the application, the total number of heat exchangers (*No_Heat_Exchanger*), the defined material and tube length correction factor (arrays *E_FM* and *E_FL*) of the heat echangers, and the current cost index (*current_cost_index*). The factors can be found in the book of Seider et al. (2008). For example, for stainless steel heat exchangers, the material factor is always set to 1. 

## Covered Heat Exchanger Equipment Types 

This code automatically decides which type of heat exchanger is taken according to heuristics of Seider et al. (2008). Four types of heat exchangers are considered: 

1. double pipe for heat exchanger areas below 14 m<sup>2</sup>, 
2. shell and tube for heat exchanger areas above 14 m<sup>2</sup>, 
3. fired heaters for temperatures above 252°C but below 300°C, and 
4. specialised fired heaters (using Dowtherm A) for temperatures above 300°C. 

A kettle reboiler is not included in this package, but can be found at LINK, because it is usually only used for distillation columns. 

For the first two types of heat exchangers (shell and tube, and double pipe, both work at temperatures until 252°C) a *HeatX* model needs to be chosen in Aspen Plus. The most commonly used *Heater* model will not work, as it does not provide the logarithmic mean temperature difference required to calculate the heat exchanger area which is necessary for the equipment cost calculation. It is very easy to replace a *heater* by a *HeatX* model in Aspen Plus. The only additional information required is the utility. There is already a list of hot or cold utilities such as steam (LP, MP, or HP) or cooling water (CW) in Aspen Plus, where you just pick the applicable one as shown below:

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/HeatX.PNG" width="650">

## Used Equations

The code in python was implemented according to the following equations: 

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Heatexchangerequations.PNG" width="700">

It is important to mention that the units are automatically adapted in the code, for example the area in m<sup>2</sup> is changed to an area in ft<sup>2</sup> within the function to match the cost correlation function. However, the output is fully transferred to SI units again, hence nothing needs to be adapted manually, only the units of the Aspen Plus file need to correspond to SI units as written above.


<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Heatexchangerexample.PNG" width="1000">


# Example

An example for the cost calculation of heat exchangers in a cumene production plant is given. 

First, the Aspen Plus simulation had to be changed to match SI units as written above, rename all heat exchangers as described above, and change all heat exchangers to HeatX models.

Logarithmic mean temperature difference	From Aspen Plus
Heat transfer coefficient	<ul><li>Water-liquid: 850 W/m²·°C</li><li>Liquid-liquid: 280 W/m²·°C</li><li>Gas-gas: 30 W/m²·°C</li><li>Reboiler: 1140 W/m²·°C</li><li>Water-water: 1140 W/m²·°C</li><li>Liquid-condensing vapour: 850 W/m²·°C</li></ul>
Correction factor	F=0.9 (heuristic Seider et al., 2008)
Arest	Q
Area	A=U·ΔT<sub>LM</sub>·F / bar<br>Heat Exchanger: A in ft²<br>For A < 105 ft²: Double pipe: C<sub>b</sub>=exp(7.1460+0.16 ln(A))<br>Else: Shell and tube: C<sub>b</sub>=exp(11.0545-0.9228 ln(A)+0.09861 ln(A)²)
Base costs	Reboiler: A in ft²<br>Kettle reboiler: C<sub>b</sub>=exp(11.967-0.8709 ln(A)+0.09005 ln(A)²)<br>Fired Heater: Q in BTU/h<br>For T < 300°C: C<sub>b</sub>=exp(0.32325-0.766 ln(Q))<br>For T > 300°C: Dowtherm A Heater: C<sub>b</sub>=12.74·Q⁰·⁶⁵
Purchase costs	<ul><li>Shell and tube: C<sub>p</sub>=F<sub>M</sub>·F<sub>L</sub>·C<sub>b</sub> with F<sub>L</sub>=1.05 (heuristic Seider et al., 2008)</li><li>Double pipe, kettle reboiler and fired heater: C<sub>p</sub>=F<sub>M</sub>·C<sub>b</sub> with F<sub>M</sub> according to heuristics (Seider et al., 2008)</li></ul>


Then, running the python code ExampleCumenePlant.py, it calls the function Heatexchanger.py and assesses the Aspen Plus example simulation CumenePlant4.bkp and computes costs and areas of all heat exchangers. As results the following outputs for the total costs, individual heat exchanger costs, heat duties and areas are obtained:

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Heatexchangeroutputs.PNG" width="450">
