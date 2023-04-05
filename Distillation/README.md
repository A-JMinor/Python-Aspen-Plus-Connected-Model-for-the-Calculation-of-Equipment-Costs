# Function Details 

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. 

In the *Distillation.py* file there are functions to calculate the equipment costs of the entire RADFRAC column model or DWSTU column model used in Aspen Plus. For both models, there exist separate functions to calculate the costs of a **trayed** columns, the reflux drums as horizonal vessels, the kettle reboilers and the condensers of the columns. 

## Costs of the Trayed Columns
The functions *distillationDWSTU* or *distillationRADFRAC* give as output the costs of the trayed DWSTU or RADFRAC columns, respectively (*d_costs_puchase_current*). Additionally, they give the dimentions of the columns such as diameter and volume (*d_diameter* in m, *d_volume* in m<sup>3</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU / RADFRAC defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the name of the input stream of the DWSTU / RADFRAC (*name_inputstream_DWSTU* / *name_inputstream_RADFRAC*), the tray spacing which is usally defined according to heuristics (mostly 0.5m), the top and bottom space (mostly defined through heuristics, 1.5 meters each), the density of the material in kg/m3 (*d_rho*), e.g. for stainless steel 8000 kg/m<sup>3</sup>, the material factor (*F_M*), e.g. for stainless steel 2.1 according to Seider et al. (2008) and the cost index of the desired year for the CAPEX calculation. 

### Used Equations for the Calucation of Equipment Dimensions and Purchase Costs
The dimensions of the DWSTU and RADFRAC model are calulcated as show below. It is important to mention that for the DWSTU model in AspenPlus, the diameter needed to be calculated in the python code in an while loop, to operate at 80 percent of the flooding velocity. For the RADFRAC WEITER

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationDimension.png" width="700">
</p>

Based on the vessel weight, the costs are calculated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationCosts.png" width="700">
</p>


## Costs of the Reflux Drums
The functions *refluxdrumDWSTU* or *refluxdrumRADFRAC* give as output the current costs of the reflux drums of the DWSTU or RADFRAC column model used in Aspen Plus (*drum_costs_puchase_current*) and the volumes of the horizontal vessels (*drum_volume* in m<sup>3</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU / RADFRAC columns defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the name of the distillates of the DWSTU / RADFRAC (*name_distallestream_DWSTU* / *name_distallestream_RADFRAC*), the residence time of the drum (*drum_residence_time*), which is usally defined according to heuristics (mostly 300seconds), the level of the liquid in the reflux drum (*drum_filled*), which is mostly defined according to heuristics (often 0.5), the length to diameter ratio (heuristics: 3), the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1 and the cost index of the desired year for the CAPEX calculation.

### Used Equations for the Calucation of Equipment Dimensions and Purchase Costs
The dimensions of the reflux drum of the DWSTU and RADFRAC model are calulcated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/RefluxdrumDimension.png" width="700">
</p>

Based on the horizontal vessel weight, the costs are calculated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/RefluxdrumCosts.png" width="700">
</p>

## Costs of the Kettle Reboilers and Condensers of the Distillation Columns
The functions *kettleDWSTU* or *kettleRADFRAC* give as output the current costs of the kettle reboiler of the DWSTU or RADFRAC column model used in Aspen Plus (*kettle_purchase_costs_current*), the heat duty and the required area (*kettle_Q* in kW, *kettle_area* in m<sup>2</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU / RADFRAC column defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the temperature of the hot utility (*kettle_hotutility_temperature*) that is used (e.g. 412 Kelvin for LP steam), the heat transfer coefficient (*kettle_U*), e.g. 1140 W/m2/°C as a heuristic, the fouling factor, e.g. 0.9 as a heuristic, and the cost index of the desired year for the CAPEX calculation.

The functions *condenserDWSTU* or *condenserRADFRAC* give as output the current costs of the condensers of the DWSTU or RADFRAC column model used in Aspen Plus (*cond_purchase_costs_current*), and the heat duty (*cond_Q*). As input required is the application (aspen Plus python connection),  the name of the DWSTU / RADFRAC column defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the fouling factor, e.g. 0.9 as a heuristic, and the cost index of the year where CAPEX is to be calculated.

The equations for the cost calculation of a kettle reboiler or condenser are given at the subfolder [Heat Exchangers](https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/tree/main/Heat-Exchanger).

# Example


