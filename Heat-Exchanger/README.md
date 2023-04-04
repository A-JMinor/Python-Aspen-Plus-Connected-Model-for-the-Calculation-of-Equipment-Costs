# Equipment Costs and Type for Heat Exchangers 

This code automatically decides which type of heat exchanger is taken according to heuristics of Seider et al. (2008). Four types of heat exchangers are considered: 

1. double pipe for heat exchanger areas below 14 m<sup>2</sup>, 
2. shell and tube for heat exchanger areas above 14 m<sup>2</sup>, 
3. fired heaters for temperatures above 252°C but below 300°C, and 
4. specialised fired heaters (using Dowtherm A) for temperatures above 300°C. 

A kettle reboiler is not included in this package, but can be found at LINK, because it is usually only used for distillation columns. 

This function gives as output the sum of the current costs of all heat exchangers present in the simulation (*E_totalcosts*), and  the current costs of the individual heat exchangers (*E_purchase_costs_current*),  the heat exchanger duties (*E_Q*) of the individual heat exchangers as well as the required heat exchanger areas of the individual heat exchangers (*E_area*) in form of a vector. As input required is the application, the total number of heat exchangers (*No_Heat_Exchanger*), the defined material and tube length correction factor (*E_FM* and *E_FL*) of the heat echangers, and the current cost index (*current_cost_index*). The factors can be found in the book of Seider et al. (2008). For example, for stainless steel heat exchangers, the material factor is always set to 1. 

## Prerequisites

**Important note:** This code only works correctly if the units in Aspen Plus for temperature and power / enthalpy flow are set to K and kW, respectively. Furthermore, all heat exchangers in Aspen Plus must be named according to E01, E02, E03, .. etc.  

For the first two types of heat exchangers (shell and tube, and double pipe, both work at temperatures until 252°C) a *HeatX* model needs to be chosen in Aspen Plus. The most commonly used *Heater* model will not work, as it does not provide the logarithmic mean temperature difference required to calculate the heat exchanger area which is necessary for the equipment cost calculation. It is very easy to replace a *heater* by a *HeatX* model in Aspen Plus. The only additional information required is the utility. There is already a list of hot or cold utilities such as steam (LP, MP, or HP) or cooling water (CW) in Aspen Plus, where you just pick the applicable one as shown below:

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/HeatX.PNG" width="650">

## Equations used in the Python Code

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Heatexchangerequations.PNG" width="650">


## Example

