
# Function Details

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for flowrates, or the pump head are required to be in m3/s and J/kg, respectively. 

This function called "*pumps*" in the *pumps.py* file gives as output the purchase costs of each single pump and motor (*pump_total_costs*, *pump_motor_purchase_costs_current*), the total purchase costs of all pumps and motors combined (*pump_purchase_costs_current*), and the pump head (*pump_head*) and flowrate (*pump_head*). As input required is the application, the number of pumps (*No_pumps*), pump_material_factor (e.g. 2 for stainless steel, see Seider et al. (2009), *pump_material_factor*), and the cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019, *current_cost_index*).

## Used Equations

Based on the flow rates, pump head, and liquid densities retrieved from Aspen Plus, the type of pump is decided and the pump costs calculated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/pumps.png" width="600">
</p>


## Example

The file CSTRexample.py first connects the example Aspen Plus simulation (CSTR2.bkp) and Python script and then accesses the function reactorCSTR from the reactor.py file, which calculates costs and volume of the vertical vessel. 
