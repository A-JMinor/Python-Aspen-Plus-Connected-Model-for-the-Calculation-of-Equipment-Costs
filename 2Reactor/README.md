
# Function Details

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. 

This function called "*reactorCSTR*" in the *Reactor*.py file gives as output the current costs of a CSTR reactor modelled with Aspen Plus (*r_costs_puchase_current*), and the volume of the reactor in m3 (*r_volume*). As input required is the application, the liquid level of the reactor (e.g. 0.65 for 65% fill, *r_liquid_fill*), the height to diameter ratio (e.g. 3 for many horizontal vessels, *r_h_d_ratio*), material factor (e.g. 2.1 for stainless steel (Seider et al. (2009), *F_M*), the density of the material of the reactor (e.g. for stainless steel 8000 kg/m3, *rho*), the given name of the reactor in the Aspen Plus simulation (*namereactor*) and the cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019, *current_cost_index*).

## Used Equations

Based on the reactor dimensions, the vertical vessel weight and the costs are calculated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Reactor.png" width="600">
</p>


## Example

The file CSTRexample.py first connects the example Aspen Plus simulation (CSTR2.bkp) and Python script and then accesses the function reactorCSTR from the reactor.py file, which calculates costs and volume of the vertical vessel. 
