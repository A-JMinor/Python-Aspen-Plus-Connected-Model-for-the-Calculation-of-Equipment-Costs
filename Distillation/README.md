# Function Details 

**Important note:** This code only works correctly if the SI units are used in Aspen Plus. Particularly, for temperature and power / enthalpy flow the units are required to be in K and kW, respectively. 

In the *Distillation.py* file there are functions to calculate the equipment costs of the entire RADFRAC column model or DWSTU column model used in Aspen Plus. For both models, there exist separate functions to calculate the costs of a **trayed** columns, the reflux drums as horizonal vessels, the kettle reboilers and the condensers of the columns. 

## Costs of the Trayed Columns
The functions *distillationDWSTU* or *distillationRADFRAC* give as output the costs of the trayed DWSTU or RADFRAC columns, respectively (*d_costs_puchase_current*). Additionally, they give the dimentions of the columns such as diameter and volume (*d_diameter* in m, *d_volume* in m<sup>3</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU / RADFRAC defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the name of the input stream of the DWSTU / RADFRAC (*name_inputstream_DWSTU* / *name_inputstream_RADFRAC*), the tray spacing which is usally defined according to heuristics (mostly 0.5m), the top and bottom space (mostly defined through heuristics, 1.5 meters each), the density of the material in kg/m3 (*d_rho*), e.g. for stainless steel 8000 kg/m<sup>3</sup>, the material factor (*F_M*), e.g. for stainless steel 2.1 according to Seider et al. (2008) and the cost index of the desired year for the CAPEX calculation.[^1]

### Used Equations for the Calucation of Equipment Dimensions and Purchase Costs
The dimensions of the DWSTU and RADFRAC model are calulcated as show below. 

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationDimension.png" width="700">
</p>

It is important to mention that for the DWSTU model in AspenPlus, the diameter needed to be calculated in the python code in an while loop, to operate at 80 percent of the flooding velocity. For the RADFRAC column model, Aspen Plus is able to calculate the diameter and give it as output. For this, it is important to generate a Tray Sizing tab *1* as shown in the figure below.  

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/RADFRACSizing.PNG" width="600">
</p>

Based on the vessel weight, the costs are calculated as follows:

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationCosts.png" width="700">
</p>


## Costs of the Reflux Drums
The functions *refluxdrumDWSTU* or *refluxdrumRADFRAC* give as output the current costs of the reflux drums of the DWSTU or RADFRAC column model used in Aspen Plus (*drum_costs_puchase_current*) and the volumes of the horizontal vessels (*drum_volume* in m<sup>3</sup>). As input required is the application (aspen Plus python connection), the name of the DWSTU / RADFRAC columns defined in Aspen Plus (*nameDWSTU* / *nameRADFRAC*), the name of the distillates of the DWSTU / RADFRAC (*name_distallestream_DWSTU* / *name_distallestream_RADFRAC*), the residence time of the drum (*drum_residence_time*), which is usally defined according to heuristics (mostly 300seconds), the level of the liquid in the reflux drum (*drum_filled*), which is mostly defined according to heuristics (often 0.5), the length to diameter ratio (heuristics: 3), the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1 and the cost index of the desired year for the CAPEX calculation.[^1]

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
An example for the cost calculation of the three RADFRAC columns of the cumene production plant (Example Simulation provided by Aspen Plus: *CumenePlant.bkp*) is given below. First, the Aspen Plus simulation had to be changed to match SI units as written above, and Tray Sizing had to be created as shown above to obtain column diameters.

<p align="center">
<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/Heatexchangerexample.PNG" width="1000">
</p>

The file ExampleCumenePlant.py first connects Aspen Plus and Python, accesses the functions required for the cost calculation in the distillation.py file and calculates the costs of towers, reflux drums, condensers, and kettle reboilers in a for loop:

```ruby
i=0
for i in range(1,no_towers+1):

    nameRADFRAC = "RAD{}".format(i)
    d_costs_puchase2019[i-1], d_diamter[i-1], d_volume[i-1] = distillationRADFRAC(Application, nameRADFRAC, tray_Spacing, top, bottom, rho, F_M, cost_index_2019) #distillation column 
    
    kettle_T = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value                          #kettle reboiler
    if kettle_T <= 120+273.15:                                  #utility kettle
        kettle_hotutility_temperature.append(138.9 + 273.15)    #LP Steam
    elif kettle_T <= 170+273.15 and kettle_T > 120+273.15:
        kettle_hotutility_temperature.append(186 + 273.15)      #MP Steam
    elif kettle_T <= 255+273.15 and kettle_T > 170+273.15:
        kettle_hotutility_temperature.append(270 + 273.15)      #HP Steam
    elif kettle_T <= 300+273.15 and kettle_T > 255+273.15:
    
    kettle_purchase_costs2019[i-1], kettle_Q[i-1], kettle_area[i-1] = kettleRADFRAC(Application, nameRADFRAC, kettle_hotutility_temperature[i-1], kettle_U,fouling_factor, cost_index_2019)

    cond_purchase_costs2019[i-1], cond_Q[i-1] = condenserRADFRAC(Application,nameRADFRAC, fouling_factor, cost_index_2019)      #condenser

    name_distallestream_DWSTU = "RADTOP{}".format(i)            #reflux drum
    drum_costs_puchase2019[i-1], drum_volume[i-1] = refluxdrumRADFRAC(Application, nameRADFRAC, name_distallestream_DWSTU, drum_residence_time, drum_filled, drum_l_to_d, rho, F_M, cost_index_2019) 
```
The following results are obtained:

<img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/DistillationExample.PNG" width="600">

## References
[^1]: W.D. Seider, J.D. Seader, D.R. Lewin, Product and Process Design Principles: Synthesis, Analysis and Design, 3rd Edition, Wiley New York, 2008.
