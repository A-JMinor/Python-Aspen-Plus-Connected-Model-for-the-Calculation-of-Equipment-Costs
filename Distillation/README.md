# Function Details

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. 

In the *Distillation.py* file there are functions to calculate the equipment costs of the entire RADFRAC column model or DWSTU column model used in Aspen Plus. For both models, there exist separate functions to calculate the costs of a trayed column, the reflux drum as horizonal vessel, the kettle reboiler and the condenser of the column. 

The functions distillationDWSTU or distillationRADFRAC give as output the costs of the **trayed** DWSTU or RADFRAC columns, respectively (*d_costs_puchase_current*). Additionally, they give the dimentions of the columns such as diameter and volume (*d_diameter* in m, *d_volume* in m<sup>3</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU/RADFRAC defined in Aspen Plus (*nameDWSTU/nameRADFRAC*), the name of the input stream of the DWSTU/RADFRAC (*name_inputstream_DWSTU*,*name_inputstream_RADFRAC*), the tray spacing which is usally defined according to heuristics (mostly 0.5m), the top and bottom space (mostly defined through heuristics, 1.5 meters each), the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m<sup>3</sup>, the material factor (F_M), e.g. for stainless steel 2.1 according to Seider et al. (2008) and the cost index of the desired year for the CAPEX calculation. 


## Covered Distillation Models

## Used Equations 

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationDimension.png" width="700">

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationCosts.png" width="700">


# Example
