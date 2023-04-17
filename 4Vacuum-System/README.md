

# Function Details and Prerequisites

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for mass flowrates to be in kg/s. 

The two functions called "*vacuumsystemSTEAMJET*" and "*vacuumsystemLIQUIDRING*" in the *vacuumoperation.py* file gives as output the purchase costs of a steam jet ejector and liquid ring pump (*v_costs_purchase_current*) and the medium pressure steam consumption of the steam jet ejector (*steam_consumption*). According to heuristics, the steam jet ejector should be taken fpr pressures below 2kPa, while the liquid ring pump is taken for pressures above 2kPa. Those functions can be used for any simulated equipment in Aspen Plus (e.g. reactor, DWSTU, ..). The stages of the steam jet ejector are determined automatically (and costs and steam consumptions accordingly). As input for those functions are the application, the pressure and volume of the equipment (*pressure*, *volume*), the flowrate to the vacuum system (*flowrate* for steam jet ejector in kg/s and for liquid ring pump in m3/s) and the cost index of the year where CAPEX is to be calculated (e.g. 600 for the year 2019, *current_cost_index*). For the liquid ring pump, the flowrate is just air because of air leakage through for example joints of the equipment. This airleakage is calculated based on an equation shown at Seider at al. (2008) and a function of pressure and volume in torr and ft3, respectively (see example file). For the steam jet ejector system, next to the air leakage flowrate, the mass flowrates of volatile components at the temperature and pressure of the vacuum system is to be added (can be modelled with a flash unit, see example file). Pay attention to units, the airleakage in the equation from Seider at al. (2008) is in lg/hr, but needs to be in kg/s or m3/s for the input to functions "*vacuumsystemSTEAMJET*" or "*vacuumsystemLIQUIDRING*", respectively. 


## Used Equations

The equations for the cost calculation of the liquid ring pump and steam jet ejectors are given below and include the calculation of the inputs such as flowrates to the vacuum systems. 

<p align="center">
Liquid ring pump:
  
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/liquidringpump.png" width="650">

Steam jet ejector system:
  
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/steamjetejector.png" width="650">
</p>


## Example

The file in the example folder  CumenePlantPump.py first connects the example Aspen Plus simulation (CumenePlant.bkp) and Python and then accesses the function *pumps* from the pumps.py file, which calculates the costs and other variables described above. 
