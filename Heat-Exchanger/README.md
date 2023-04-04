# Prerequisites and Covered Types of Heat Exchangers

**Important note:** This code only works correctly if the units in Aspen Plus for temperature and power / enthalpy flow are set to K and kW, respectively.

This code is written for 4 types of heat exchangers: 1) double pipe for heat exchanger areas below 14 m<sup>2</sup>, 2) shell and tube for heat exchanger areas above 14 m<sup>2</sup>, 3) fired heaters for temperatures above 252°C but below 300°C, and 4) specialised fired heaters (using Dowtherm A) for temperatures above 300°C.

For the first two types of heat exchangers, that work at temperatures until 252°C, a *HeatX* model needs to be chosen in Aspen Plus. The most commonly used *Heater* model will not work, as it does not provide the logarithmic mean temperature difference required to calculate the heat exchanger area which is necessary for the equipment cost calculation. It is very easy to replace a *heater* by a *HeatX* model in Aspen Plus. The only additional information required is the utility. There is already a list of hot or cold utilities such as steam (LP, MP, or HP) or cooling water (CW) in Aspen Plus, where you just pick the applicable one as shown below:

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/HeatX.PNG" width="500">



# Equations used in the Python Code


# Example

