# Prerequisites and Covered Types of Heat Exchangers

The most commonly used "heater" model of Aspen Plus cannot be taken, instead a "HeatX" model must be chosen. The reason for this is, that the heater model does not provide the logarithmic mean temperature difference required to calculate the heat exchanger area. However, this area is required for the cost calculation. It is very easy to replace a heater by a HeatX model in Aspen Plus. The only additional information you need is the utility. There is already a list of hot or cold utilities such as steam or cooling water in Aspen Plus, where you just pick the applicable one. 


# Equations used in the Python Code

