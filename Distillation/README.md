# Function Details

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. Furthermore, all heat exchangers in Aspen Plus must be named according to E01, E02, E03, .. etc in the Aspen Plus simulation. 

This function called "heatexchanger" in the HeatExchanger.py file decides about the type of heat exchanger according to heuristics of Seider et al. (2008) and gives as output the sum of the current costs of all heat exchangers present in the simulation (*E_totalcosts*), the current costs of the individual heat exchangers (array *E_purchase_costs_current*), the heat exchanger duties (array *E_Q*) of the individual heat exchangers as well as the required heat exchanger areas of the individual heat exchangers (array *E_area*). As input required is the application, the total number of heat exchangers (*No_Heat_Exchanger*), the defined material and tube length correction factor (arrays *E_FM* and *E_FL*) of the heat echangers, and the current cost index (*current_cost_index*). The factors can be found in the book of Seider et al. (2008). For example, for stainless steel heat exchangers, the material factor is always set to 1. 

## Covered Distillation Models

## Used Equations 

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationDimension.png" width="450">

# Example
