# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:08:38 2023

@author: Ann-Joelle
"""

import numpy as np


#Unit calculations
m_to_inch = 39.3701
m_to_ft = 3.28084
m2_to_ft2 = 10.7639
m3_to_ft3 = 35.3147
kPa_to_psig = 0.145038
kPa_to_Torr = 7.50062
kg_to_lb = 2.20462
W_to_Btu_hr = 3.41
gal_to_m3 = 0.00378541
BTU_to_J = 1055.06
HP_to_W = 745.7
m3_s_to_gpm = 15850.3
kg_m3_to_lb_gal = 0.0083454
t_to_kg = 1000
HP_per_1000_Gal = 10
N_m2_to_psig = 0.000145038
m3_to_in3 = 61023.7

#Operating year
hr_per_day = 24
day_per_year = 365
operating_factor = 0.9 

#cost factors of equations from Seider et al. 2006 
cost_index_2006 = 500

#This function gives as output the current costs of the column (d_costs_puchase_current) and the dimentions of the vessel such as diameter and volume (d_diameter, d_volume)
#As input required is the application (aspen Plus python connection), the name of the DWSTU defined in Aspen Plus (nameDWSTU)
#the name of the input stream of the DWSTU (name_inputstream_DWSTU), the tray spacing which is usally defined according to heuristics (mostly 0.5m)
#the top and bottom space (mostly defined through heuristics, 1.5 meters each), the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1
#and the cost index of the year where CAPEX is to be calculated
def distillationDWSTU(Application, nameDWSTU, name_inputstream_DWSTU, name_distallestream_DWSTU, tray_Spacing, top_space, bottom_space, d_rho, F_M, current_cost_index):   
    
    #cost factors 
    cost_index_2006 = 500
    
    #Geometry #NAME distillation column as DIST
    no_of_trays = round(Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\ACT_STAGES").Value,0)   #DWSTU gives decimal number for stages, hence needs rounding
    d_height = no_of_trays * tray_Spacing + top_space + bottom_space        #m3
    #print("\n the height of the distillation column is", d_height, "m \n")
    d_tangent_tangent_length = no_of_trays * tray_Spacing       #m3
    
    
    #calculation for the diameter  (see Turton 2018 strategy) 
    #we need vapor and liquid data of the distillate, hence we need one distillation unit with a total condenser and one with a partial condenser that gives only vapor distillate 
    #Depending on which type of distillation you need, the other one created will have the opposite type of condenser and is only fictive to get values for the diameter calculation 
    #creating a second distillation unit that takes the exact same feed can be done by a calculator block
    
    #calculation exampe in case you have a total condenser: 
    #reflux ratio from the actual distillation that you want to use
    d_RR = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\ACT_REFLUX").Value
    d_feed = Application.Tree.FindNode("\Data\Streams\\" + name_inputstream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value
    d_distillate = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value    #kg/s
    #since you have a total condenser, the liquid flow and vapor flow in the column are given as follows:
    d_liquidflow = d_RR * d_distillate
    d_vaporflow = d_liquidflow + d_distillate       #kg/s from material balance around condenser
    #diameter is determined at the highest flowrate, since feed is in vapor form, it comes together with vapor flow in column and diameter of upper part of column is determined, flowrates need to be adapted
    d_liquidflow_adapt = d_liquidflow
    d_vaporflow_adapt = d_vaporflow + d_feed
    #in AspenPlus use duplicator to find vapor density of the top of the column 
    d_liquid_rho = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value / Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\VOLFLMX\MIXED").Value         #kg/m3
    Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\OPT_RDV").Value = 'VAPOR'
    Application.Engine.Run2()
    d_vapor_rho = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value / Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\VOLFLMX\MIXED").Value      #kg/m3
    Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\OPT_RDV").Value = 'LIQUID'
    Application.Engine.Run2()
    d_flow_param = (d_liquidflow_adapt / d_vaporflow_adapt) * (d_vapor_rho/d_liquid_rho)**0.5     #correlation according to book Turton 2018
    d_capacity_param = 10**(-1.0262 - 0.63513 * np.log10(d_flow_param) - 0.20097 * (np.log10(d_flow_param))**2)         #ft/ s emprical correlation according to turton book with tray spacing = 0.5 m (certain parameters given for empirical correlation equation)
    d_flooding_velocity = d_capacity_param * 1.3 * ((d_liquid_rho - d_vapor_rho) / d_vapor_rho)**0.5        #ft / s
    d_flooding_factor = 0.8 
    d_vapor_velocity = d_flooding_velocity * d_flooding_factor / m_to_ft    #m/s
    d_active_area = d_vaporflow / (d_vapor_rho  * d_vapor_velocity)     #m2
    d_diameter = (4 * d_active_area / np.pi )**0.5
    
    #because it came out that column was square (6 m diameter, 6 m height, weird thing)
    if d_height / round(d_diameter,0) < 3 :
        d_height = 3 * round(d_diameter,0)
        no_of_trays = (d_height - top_space - bottom_space) / tray_Spacing 
        d_tangent_tangent_length = no_of_trays * tray_Spacing
 
    
        
        if d_height > 60:
            print("Warning distillation tower too high")
    
    
    d_volume = (np.pi/4) * d_diameter**2 * d_height             #m3
    
    
    d_lowest_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\PTOP").Value      #kPa
    
    if d_lowest_pressure <= 34.5: #kpa
        d_design_pressure = 10.0 #psig
    elif d_lowest_pressure > 34.5 and d_lowest_pressure <= 6895:
        d_design_pressure = np.exp(0.60608 + 0.91615 * np.log(d_lowest_pressure) + 0.0015655*np.log(d_lowest_pressure)**2)
    else:
        print("Warning!! operating pressure too high for cost calculation of distillation column! Look for another cost equation")
    
    d_highest_temp = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\BOTTOM_TEMP").Value      #K
    d_design_temp = (d_highest_temp - 273.15) * 9/5 + 32.0 + 50.0           #Fahrenheit
    
    if d_design_temp >= -20.0 and d_design_temp < 200.0 :
        d_E_modulus = 30.2 *10**6
    elif d_design_temp >= 200.0 and d_design_temp < 400.0 :
        d_E_modulus = 29.5 *10**6
    elif d_design_temp >= 400.0 and d_design_temp < 650.0 :
        d_E_modulus = 28.3 *10**6
    #elif d_design_temp >= -650.0 and d_design_temp < 700.0 :
    else:
        d_E_modulus = 26.0 *10**6
    #else:
      # print("Warning!! Design temperature is too high for carbon steel, use another material")
    
    if d_design_temp >= -20 and d_design_temp <= 750:
        d_allowable_stress = 15000
    elif d_design_temp <= 800: 
        d_allowable_stress = 14750
    elif d_design_temp <= 850: 
        d_allowable_stress = 14200
    elif d_design_temp <= 900: 
        d_allowable_stress = 13100
    else:
        print("Warning!! distillation design temperature is too high for wall thickness calculation from seider ")
    
    
    d_tE1 = 0.25
    error = 1
    
    if d_lowest_pressure >= 101:     #kpa atmospheric pressures
        
        #equation for calculating wall thickness at top where there is wind etc.
        while abs(error) > 0.001:
            d_tE = 0.22 * (((d_diameter*m_to_inch)+d_tE1)+18) * (d_tangent_tangent_length*m_to_inch)**2 / (d_allowable_stress * ((d_diameter*m_to_inch)+d_tE1)**2 ) 
            error = (d_tE1 - d_tE)/d_tE1
            d_tE1 = d_tE
    
        #equation for calculating at bottom where there is no wind 
        d_tp = (d_design_pressure * (d_diameter*m_to_inch))/(2*d_allowable_stress-1.2*d_design_pressure)
    
        #wall thickness is the average between the two
        d_t_total = (d_tp + d_tE) / 2
        
        
    elif d_lowest_pressure <= 101:  #vacuum operations
        
        while abs(error) > 0.001:
            d_tE = 1.3 * ((d_diameter*m_to_inch)+d_tE1) * ((d_design_pressure * (d_tangent_tangent_length*m_to_inch))/(d_E_modulus*((d_diameter*m_to_inch)+d_tE1)))**0.4
            error = (d_tE1 - d_tE)/d_tE1
            d_tE1 = d_tE
        
        check = d_tE/(d_diameter*m_to_inch)
        if check >= 0.05 :
            print(" ")
        
        d_tEC = (d_tangent_tangent_length*m_to_inch) * (0.18*(d_diameter*m_to_inch)-2.2)*10**(-5) - 0.19
        
        if d_tEC > 0 :
            d_t_total = d_tEC + d_tE + 0.125       # 0.125 for corrosive allowance add up 
        else : 
            d_t_total = d_tE + 0.125               # 0.125 corrosive allowance add up 
            

    if d_t_total < 0.25:   #minimum wall thickness to be bought
        d_t_total = 0.25
    
    
    d_weight = np.pi*d_t_total * (d_rho*kg_to_lb/m3_to_in3) ((d_diameter*m_to_inch) + d_t_total) * ((d_tangent_tangent_length*m_to_inch) + 0.8 * (d_diameter*m_to_inch))
    
    
    #Costs
    if d_weight < 9000 or d_weight > 2500000:
        print("")
    d_costs_vessel = np.exp(7.2756 + 0.18255 * np.log(d_weight) + 0.02297 * (np.log(d_weight))**2)
    
    if (d_diameter * m_to_ft )< 3 or (d_tangent_tangent_length * m_to_ft) < 27:
        print("") 
    d_added_costs = 300.9 * ((d_diameter*m_to_ft))**0.63316 * ((d_tangent_tangent_length*m_to_ft))**0.80161
    
    if (d_diameter * m_to_ft)< 2 or (d_diameter * m_to_ft ) > 16:
        print("")
    d_costs_sievetrays = 468 * np.exp(0.1739*(d_diameter*m_to_ft))
    
    
    if no_of_trays < 20: 
        F_NT = 2.25 / (1.0414**no_of_trays)
    else: 
        F_NT = 1.0
    
    F_TM = 1.401 + 0.0724 * (d_diameter*m_to_ft)
    
    d_costs_installed_sievetrays = F_NT * F_TM * no_of_trays * d_costs_sievetrays
    
    
    d_costs_purchase = F_M * d_costs_vessel + d_added_costs + d_costs_installed_sievetrays
    d_costs_puchase_current = current_cost_index / cost_index_2006 * d_costs_purchase
    
    return d_costs_puchase_current, d_diameter, d_volume





#This function gives as output the current costs of the RADFRAC column used in Aspen Plus (d_costs_puchase_current) and the dimentions of the vessel such as diameter and volume (d_diameter, d_volume)
#As input required is the application (aspen Plus python connection), the name of the DWSTU defined in Aspen Plus (nameDWSTU)
#the name of the input stream of the DWSTU (name_inputstream_DWSTU), the tray spacing which is usally defined according to heuristics (mostly 0.5m)
#the top and bottom space (mostly defined through heuristics, 1.5 meters each), the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1
#and the cost index of the year where CAPEX is to be calculated
def distillationRADFRAC(Application, nameRADFRAC, tray_Spacing, top_space, bottom_space, d_rho, F_M, current_cost_index):   
    
    #attention in that code, distillation height / number of trays is permanently setted to a value that fits diameter. If there are any forloops in code
    #the height / number of trays should be resetted within the foor loop
    #cost factors 
    cost_index_2006 = 500
    
    #Geometry #NAME distillation column as DIST
    no_of_trays = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Input\\NSTAGE").Value
    d_height = no_of_trays * tray_Spacing + top_space + bottom_space        #m3
    d_tangent_tangent_length = no_of_trays * tray_Spacing       #m3
    d_diameter = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Subobjects\\Tray Sizing\\1\\Output\\DIAM4\\1").Value
    
    
    if d_height / d_diameter < 3: 
        d_height = 3 * round(d_diameter,0)
        no_of_trays = (d_height - top_space - bottom_space) / tray_Spacing 
        d_tangent_tangent_length = no_of_trays * tray_Spacing
    
    
    if d_height > 60:
        print("Warning distillation tower too high")
        
    
    d_volume = (np.pi/4) * d_diameter**2 * d_height             #m3
    

    d_lowest_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Input\PRES1").Value      #kPa
    
    if d_lowest_pressure <= 34.5: #kpa
        d_design_pressure = 10.0 #psig
    elif d_lowest_pressure > 34.5 and d_lowest_pressure <= 6895:
        d_design_pressure = np.exp(0.60608 + 0.91615 * np.log(d_lowest_pressure) + 0.0015655*np.log(d_lowest_pressure)**2)
    else:
        print("Warning!! operating pressure too high for cost calculation of distillation column! Look for another cost equation")
    
    d_highest_temp = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value      #K
    d_design_temp = (d_highest_temp - 273.15) * 9/5 + 32.0 + 50.0           #Fahrenheit
    
    if d_design_temp >= -20.0 and d_design_temp < 200.0 :
        d_E_modulus = 30.2 *10**6
    elif d_design_temp >= 200.0 and d_design_temp < 400.0 :
        d_E_modulus = 29.5 *10**6
    elif d_design_temp >= 400.0 and d_design_temp < 650.0 :
        d_E_modulus = 28.3 *10**6
    #elif d_design_temp >= -650.0 and d_design_temp < 700.0 :
    else:
        d_E_modulus = 26.0 *10**6
    #else:
      # print("Warning!! Design temperature is too high for carbon steel, use another material")
    
    if d_design_temp >= -20 and d_design_temp <= 750:
        d_allowable_stress = 15000
    elif d_design_temp <= 800: 
        d_allowable_stress = 14750
    elif d_design_temp <= 850: 
        d_allowable_stress = 14200
    elif d_design_temp <= 900: 
        d_allowable_stress = 13100
    else:
        print("Warning!! distillation design temperature is too high for wall thickness calculation from seider ")
    
    
    d_tE1 = 0.25
    error = 1
    
    if d_lowest_pressure >= 101:     #kpa atmospheric pressures
        
        #equation for calculating wall thickness at top where there is wind etc.
        while abs(error) > 0.001:
            d_tE = 0.22 * (((d_diameter*m_to_inch)+d_tE1)+18) * (d_tangent_tangent_length*m_to_inch)**2 / (d_allowable_stress * ((d_diameter*m_to_inch)+d_tE1)**2 ) 
            error = (d_tE1 - d_tE)/d_tE1
            d_tE1 = d_tE
    
        #equation for calculating at bottom where there is no wind 
        d_tp = (d_design_pressure * (d_diameter*m_to_inch))/(2*d_allowable_stress-1.2*d_design_pressure)
    
        #wall thickness is the average between the two
        d_t_total = (d_tp + d_tE) / 2
        
        
    elif d_lowest_pressure <= 101:  #vacuum operations
        
        while abs(error) > 0.001:
            d_tE = 1.3 * ((d_diameter*m_to_inch)+d_tE1) * ((d_design_pressure * (d_tangent_tangent_length*m_to_inch))/(d_E_modulus*((d_diameter*m_to_inch)+d_tE1)))**0.4
            error = (d_tE1 - d_tE)/d_tE1
            d_tE1 = d_tE
        
        check = d_tE/(d_diameter*m_to_inch)
        if check >= 0.05 :
            print("")
        
        d_tEC = (d_tangent_tangent_length*m_to_inch) * (0.18*(d_diameter*m_to_inch)-2.2)*10**(-5) - 0.19
        
        if d_tEC > 0 :
            d_t_total = d_tEC + d_tE + 0.125       # 0.125 for corrosive allowance add up 
        else : 
            d_t_total = d_tE + 0.125               # 0.125 corrosive allowance add up 
            
    

    if d_t_total < 0.25:   #minimum wall thickness to be bought
        d_t_total = 0.25
    
    
    d_weight = np.pi*d_t_total * (d_rho*kg_to_lb/m3_to_in3)*((d_diameter*m_to_inch) + d_t_total) * ((d_tangent_tangent_length*m_to_inch) + 0.8 * (d_diameter*m_to_inch))
    
    
    #Costs
    if d_weight < 9000 or d_weight > 2500000:
        print("")
    d_costs_vessel = np.exp(7.2756 + 0.18255 * np.log(d_weight) + 0.02297 * (np.log(d_weight))**2)
    
    if (d_diameter * m_to_ft )< 3 or (d_tangent_tangent_length * m_to_ft) < 27:
        print("") 
    d_added_costs = 300.9 * ((d_diameter*m_to_ft))**0.63316 * ((d_tangent_tangent_length*m_to_ft))**0.80161
    
    if (d_diameter * m_to_ft)< 2 or (d_diameter * m_to_ft ) > 16:
        print("")
    d_costs_sievetrays = 468 * np.exp(0.1739*(d_diameter*m_to_ft))
    
    
    if no_of_trays < 20: 
        F_NT = 2.25 / (1.0414**no_of_trays)
    else: 
        F_NT = 1.0
    
    F_TM = 1.401 + 0.0724 * (d_diameter*m_to_ft)
    
    d_costs_installed_sievetrays = F_NT * F_TM * no_of_trays * d_costs_sievetrays
    
    
    d_costs_purchase = F_M * d_costs_vessel + d_added_costs + d_costs_installed_sievetrays
    d_costs_puchase_current = current_cost_index / cost_index_2006 * d_costs_purchase
    
    return d_costs_puchase_current, d_diameter, d_volume



#This function gives as output the current costs of the reflux drum of the DWSTU column model used in Aspen Plus (drum_costs_puchase_current) and the volume of the horizontal vessel (drum_volume)
#As input required is the application (aspen Plus python connection), the name of the DWSTU defined in Aspen Plus (nameDWSTU)
#the name of the distillate of the DWSTU (name_distallestream_DWSTU), the residence time of the drum drum_residence_time which is usally defined according to heuristics (mostly 300seconds)
#the level of the liquid in the reflux drum (drum_filled) which is mostly defined according to heuristics (often 0.5), the Length to diameter ratio (heuristics: 3)  
#the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1
#and the cost index of the year where CAPEX is to be calculated
def refluxdrumDWSTU(Application, nameDWSTU, name_distallestream_DWSTU, drum_residence_time, drum_filled, drum_l_to_d, r_rho, F_M, current_cost_index):
    

    #geometrics
    d_distillate = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value
    d_RR = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\ACT_REFLUX").Value
    d_liquid_rho = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\MASSFLMX\MIXED").Value / Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_DWSTU + "\Output\STR_MAIN\VOLFLMX\MIXED").Value         #kg/m3
    d_lowest_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\PTOP").Value      #kPa
    drum_liquid_flowrate  = d_distillate * (1 + d_RR)        #kg/s
    drum_liquid_density = d_liquid_rho        #kg/m3
    drum_flowrate = drum_liquid_flowrate / drum_liquid_density        #m3/s
    drum_hold_up = drum_residence_time * drum_flowrate
    drum_volume = drum_hold_up / drum_filled
    drum_diameter = (drum_volume*(4/np.pi))**(1/3)
    drum_length = drum_l_to_d * drum_diameter
    
    
    drum_lowest_pressure = d_lowest_pressure
    
    if drum_lowest_pressure <= 34.5: #kpa
        drum_design_pressure = 10.0 #psig
    elif drum_lowest_pressure > 34.5 and drum_lowest_pressure <= 6895:
        drum_design_pressure = np.exp(0.60608 + 0.91615 * np.log(drum_lowest_pressure) + 0.0015655*np.log(drum_lowest_pressure)**2)
    else:
        print("Warning!! operating pressure too high for cost calculation of reflux drum! Look for another cost equation")
        
    drum_temp = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\BOTTOM_TEMP").Value      #K
    drum_design_temp = (drum_temp - 273.15) * 9/5 + 32.0 + 50.0           #Fahrenheit
    
    if drum_design_temp >= -20.0 and drum_design_temp < 200.0 :
        drum_E_modulus = 30.2 *10**6
    elif drum_design_temp >= -200.0 and drum_design_temp < 400.0 :
        drum_E_modulus = 29.5 *10**6
    elif drum_design_temp >= -400.0 and drum_design_temp < 650.0 :
        drum_E_modulus = 28.3 *10**6
    elif drum_design_temp >= -650.0 and drum_design_temp < 700.0 :
        drum_E_modulus = 26.0 *10**6
    else:
        print("Warning!! Design temperature is too high for carbon steel, use another material")
    
    if drum_design_temp >= -20 and drum_design_temp <= 750:
        drum_allowable_stress = 15000
    elif drum_design_temp <= 800: 
        drum_allowable_stress = 14750
    elif drum_design_temp <= 850: 
        drum_allowable_stress = 14200
    elif drum_design_temp <= 900: 
        drum_allowable_stress = 13100
    else:
        print("Warning!! reactor design temperature is too high for wall thickness calculation from seider ")
    
    
    if drum_lowest_pressure * 0.001 >= 101:         #101 kpa for atmospheric pressure 
        drum_t_total = (drum_design_pressure * (drum_diameter*m_to_inch))/(2*drum_allowable_stress-1.2*drum_design_pressure)
        
    else:   #vacuum operation
        drum_tE1 = 0.25
        error = 1
        
        while abs(error) > 0.001:
            drum_tE = 1.3 * ((drum_diameter*m_to_inch)+drum_tE1) * ((drum_design_pressure * (drum_length*m_to_inch))/(drum_E_modulus*((drum_diameter*m_to_inch)+drum_tE1)))**0.4
            error = (drum_tE1 - drum_tE)/drum_tE1
            drum_tE1 = drum_tE
            
        check = drum_tE/(drum_diameter*m_to_inch)
        if check >= 0.05 :
            print("")
        
        drum_tEC = (drum_length*m_to_inch) * (0.18*(drum_diameter*m_to_inch)-2.2)*10**(-5) - 0.19
        
        if drum_tEC > 0 :
            drum_t_total = drum_tEC + drum_tE + 0.125       # 0.125 for corrosive allowance add up 
        else : 
            drum_t_total = drum_tE + 0.125               # 0.125 corrosive allowance add up 
    
    
    if drum_t_total < 0.25:        #minimum wall thickness
        drum_t_total = 0.25
    
   
    
    drum_weight = np.pi*drum_t_total * (r_rho*kg_to_lb/m3_to_in3) * ((drum_diameter*m_to_inch) + drum_t_total) * ((drum_length*m_to_inch) + 0.8 * (drum_diameter*m_to_inch))
    
    if drum_weight < 1000: 
        drum_cost_vessel = np.exp(8.9552 - 0.233 * np.log(1000) + 0.04333 * (np.log(1000))**2 ) * (drum_weight/1000)**0.6
    else: 
        drum_cost_vessel = np.exp(8.9552 - 0.233 * np.log(drum_weight) + 0.04333 * (np.log(drum_weight))**2 )
    
    if (drum_diameter * m_to_ft )< 3:
        print("") 
    drum_added_costs = 2005 * ((drum_diameter*m_to_ft))**0.20294 
    
    
    drum_costs_purchase = F_M * drum_cost_vessel + drum_added_costs
    drum_costs_puchase_current = current_cost_index / cost_index_2006 * drum_costs_purchase
    
    return drum_costs_puchase_current, drum_volume



#This function gives as output the current costs of the reflux drum of the RADFRAC column model used in Aspen Plus (drum_costs_puchase_current) and the volume of the horizontal vessel (drum_volume)
#As input required is the application (aspen Plus python connection), the name of the RADFRAC column defined in Aspen Plus (nameRADFRAC)
#the name of the distillate of the RADFRAC (name_distallestream_RADFRAC), the residence time of the drum drum_residence_time which is usally defined according to heuristics (mostly 300seconds)
#the level of the liquid in the reflux drum (drum_filled) which is mostly defined according to heuristics (often 0.5), the Length to diameter ratio (heuristics: 3)  
#the density of the material in kg/m3 (d_rho), e.g. for stainless steel 8000 kg/m3, the material factor (F_M), e.g. for stainless steel 2.1
#and the cost index of the year where CAPEX is to be calculated
def refluxdrumRADFRAC(Application, nameRADFRAC, name_distallestream_RADFRAC, drum_residence_time, drum_filled, drum_l_to_d, r_rho, F_M, current_cost_index):
    

    #geometrics
    d_distillate = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_RADFRAC + "\Output\STR_MAIN\MASSFLMX\MIXED").Value
    d_RR = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\MOLE_RR").Value
    d_liquid_rho = Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_RADFRAC + "\Output\STR_MAIN\MASSFLMX\MIXED").Value / Application.Tree.FindNode("\Data\Streams\\" + name_distallestream_RADFRAC + "\Output\STR_MAIN\VOLFLMX\MIXED").Value         #kg/m3
    d_lowest_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Input\PRES1").Value      #kPa
    drum_liquid_flowrate  = d_distillate * (1 + d_RR)        #kg/s
    drum_liquid_density = d_liquid_rho        #kg/m3
    drum_flowrate = drum_liquid_flowrate / drum_liquid_density        #m3/s
    drum_hold_up = drum_residence_time * drum_flowrate
    drum_volume = drum_hold_up / drum_filled
    drum_diameter = (drum_volume*(4/np.pi))**(1/3)
    drum_length = drum_l_to_d * drum_diameter
    
    
    drum_lowest_pressure = d_lowest_pressure
    
    if drum_lowest_pressure <= 34.5: #kpa
        drum_design_pressure = 10.0 #psig
    elif drum_lowest_pressure > 34.5 and drum_lowest_pressure <= 6895:
        drum_design_pressure = np.exp(0.60608 + 0.91615 * np.log(drum_lowest_pressure) + 0.0015655*np.log(drum_lowest_pressure)**2)
    else:
        print("Warning!! operating pressure too high for cost calculation of reflux drum! Look for another cost equation")
        
    drum_temp = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value      #K
    drum_design_temp = (drum_temp - 273.15) * 9/5 + 32.0 + 50.0           #Fahrenheit
    
    if drum_design_temp >= -20.0 and drum_design_temp < 200.0 :
        drum_E_modulus = 30.2 *10**6
    elif drum_design_temp >= -200.0 and drum_design_temp < 400.0 :
        drum_E_modulus = 29.5 *10**6
    elif drum_design_temp >= -400.0 and drum_design_temp < 650.0 :
        drum_E_modulus = 28.3 *10**6
    elif drum_design_temp >= -650.0 and drum_design_temp < 700.0 :
        drum_E_modulus = 26.0 *10**6
    else:
        print("Warning!! Design temperature is too high for carbon steel, use another material")
    
    drum_tE_ness1 = 0.034
    error = 1
    while abs(error) > 0.001:
        drum_tE_ness = 1.3 * ((drum_diameter*m_to_inch) + drum_tE_ness1) * ((drum_design_pressure * (drum_length*m_to_inch))/(drum_E_modulus*((drum_diameter*m_to_inch)+drum_tE_ness1)))**0.4
        error = (drum_tE_ness1 - drum_tE_ness)/drum_tE_ness1
        drum_tE_ness1 = drum_tE_ness
    
        
    check = drum_tE_ness/drum_diameter 
    if check >= 0.05 :
        print("")
    
    drum_tEC = (drum_length*m_to_inch) * (0.18*(drum_diameter*m_to_inch)-2.2)*10**(-5) - 0.19
    
    if drum_tEC > 0 :
        drum_t_total = drum_tEC + drum_tE_ness 
    else : 
        drum_t_total = drum_tE_ness 
    
    
    drum_t_total_corr = drum_t_total + 0.125     #corrosive allowance add up 
    
    if drum_t_total_corr < 0.1875 and drum_lowest_pressure > 100:     #minimum wall thickness to be bought
        drum_t_total_corr = 0.1875             #inches
    elif drum_t_total_corr < 0.25 and drum_lowest_pressure < 100:   #minimum wall thickness to be bought when vacuum
        drum_t_total_corr = 0.25
    
    
    drum_weight = np.pi*drum_t_total_corr * (r_rho*kg_to_lb/m3_to_in3) * ((drum_diameter*m_to_inch) + drum_t_total_corr) * ((drum_length*m_to_inch) + 0.8 * (drum_diameter*m_to_inch))
    
    if drum_weight < 1000: 
        drum_cost_vessel = np.exp(8.9552 - 0.233 * np.log(1000) + 0.04333 * (np.log(1000))**2 ) * (drum_weight/1000)**0.6
    else: 
        drum_cost_vessel = np.exp(8.9552 - 0.233 * np.log(drum_weight) + 0.04333 * (np.log(drum_weight))**2 )
    
    if (drum_diameter * m_to_ft )< 3:
        print("") 
    drum_added_costs = 2005 * ((drum_diameter*m_to_ft))**0.20294 
    
    
    drum_costs_purchase = F_M * drum_cost_vessel + drum_added_costs
    drum_costs_puchase_current = current_cost_index / cost_index_2006 * drum_costs_purchase
    
    return drum_costs_puchase_current, drum_volume



#This function gives as output the current costs of the kettle reboiler of the RADFRAC column model used in Aspen Plus (kettle_purchase_costs_current), the heat duty and the required area (kettle_Q, kettle_area)
#As input required is the application (aspen Plus python connection), the name of the RADFRAC column defined in Aspen Plus (nameRADFRAC)
#the temperature of the hot utility (kettle_hotutility_temperature) that is used (e.g. 412 Kelvin for LP steam) 
#the heat transfer coefficient (kettle_U), e.g. 1140 W/m2/C as a heuristic, the fouling factor, e.g. 0.9 as a heuristic, 
#and the cost index of the year where CAPEX is to be calculated
def kettleRADFRAC(Application, nameRADFRAC, kettle_hotutility_temperature, kettle_U, fouling_factor, current_cost_index):
    
    #for area calculation:
    kettle_Q = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\REB_DUTY").Value
    kettle_cold = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value
    kettle_LMTD = kettle_hotutility_temperature - kettle_cold
    kettle_area = kettle_Q / (kettle_U * kettle_LMTD * fouling_factor) * m2_to_ft2
    
    #for pressure factor calculation:
    kettle_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Input\PRES1").Value * kPa_to_psig    #Aspen in kpa
    if kettle_pressure >= 100:     #for pressure factor
        kettle_FP = 0.9803 + 0.018 * (kettle_pressure / 100) + 0.0017 * (kettle_pressure / 100)**2
    else:
        kettle_FP = 1  
    
    #for material factor calculation:
    kettle_FM = 1.75 + (kettle_area / 100)**0.13        #stainless steel / carbon steel
    
    #base costs:
    if kettle_area <= 150:
        kettle_base_costs = np.exp(11.967 - 0.8709 * np.log(150) + 0.09005 * (np.log(150))**2) * (kettle_area / 150)**0.59
        print("Warning, the area of the kettle reboiler is too small to apply cost calculation equation from Seider")
    else: 
        kettle_base_costs = np.exp(11.967 - 0.8709 * np.log(kettle_area) + 0.09005 * (np.log(kettle_area))**2) 
    
    #purchase costs:
    kettle_purchase_costs = kettle_FM * kettle_FP * kettle_base_costs
    kettle_purchase_costs_current = current_cost_index / cost_index_2006 * kettle_purchase_costs
    
    return kettle_purchase_costs_current, kettle_Q, kettle_area




#This function gives as output the current costs of the kettle reboiler of the DWSTU column model used in Aspen Plus (kettle_purchase_costs_current), the heat duty and the required area (kettle_Q, kettle_area)
#As input required is the application (aspen Plus python connection), the name of the DWSTU column defined in Aspen Plus (nameRADFRAC)
#the temperature of the hot utility (kettle_hotutility_temperature) that is used (e.g. 412 Kelvin for LP steam) 
#the heat transfer coefficient (kettle_U), e.g. 1140 W/m2/C as a heuristic, the fouling factor, e.g. 0.9 as a heuristic, 
#and the cost index of the year where CAPEX is to be calculated
def kettleDWSTU(Application, nameDWSTU, kettle_hotutility_temperature, kettle_U, fouling_factor, current_cost_index):
    
    #for area calculation:
    kettle_Q = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\REB_DUTY").Value
    kettle_U = 1140         #W/m2/°C 
    kettle_cold = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\BOTTOM_TEMP").Value
    kettle_LMTD = kettle_hotutility_temperature - kettle_cold
    kettle_area = kettle_Q / (kettle_U * kettle_LMTD * fouling_factor) * m2_to_ft2

    #for pressure factor calculation:
    kettle_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\PBOT").Value * kPa_to_psig    #Aspen in kpa
    if kettle_pressure >= 100:     #for pressure factor
        kettle_FP = 0.9803 + 0.018 * (kettle_pressure / 100) + 0.0017 * (kettle_pressure / 100)**2
    else:
        kettle_FP = 1  

    #for material factor calculation:
    kettle_FM = 1.75 + (kettle_area / 100)**0.13        #stainless steel / carbon steel

    #base costs:
    if kettle_area <= 150:
        kettle_base_costs = np.exp(11.967 - 0.8709 * np.log(150) + 0.09005 * (np.log(150))**2) * (kettle_area / 150)**0.59
        print("Warning, the area of the kettle reboiler is too small to apply cost calculation equation from Seider")
    else: 
        kettle_base_costs = np.exp(11.967 - 0.8709 * np.log(kettle_area) + 0.09005 * (np.log(kettle_area))**2) 

    #purchase costs:
    kettle_purchase_costs = kettle_FM * kettle_FP * kettle_base_costs
    kettle_purchase_costs_current = current_cost_index / cost_index_2006 * kettle_purchase_costs

    return kettle_purchase_costs_current, kettle_Q, kettle_area



#This function gives as output the current costs of the kettle reboiler of the RADFRAC column model used in Aspen Plus (cond_purchase_costs_current), and the heat duty (cond_Q)
#As input required is the application (aspen Plus python connection), the name of the RADFRAC column defined in Aspen Plus (nameRADFRAC)
#the fouling factor, e.g. 0.9 as a heuristic, and the cost index of the year where CAPEX is to be calculated
def condenserRADFRAC(Application, nameRADFRAC, fouling_factor, current_cost_index):
    #for area calculation:
    cond_Q = np.abs(Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\\COND_DUTY").Value)
    cond_U = 1140         #W/m2/°C 
    cond_cold_in = 30 + 273.15      #K cooling water defined inlet temperature
    cond_cold_out = 45 + 273.15
    cond_hot = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value
    cond_LMTD = (cond_cold_out-cond_cold_in)/np.log((cond_hot-cond_cold_in)/(cond_hot-cond_cold_out))
    cond_area = cond_Q / (cond_U * cond_LMTD * fouling_factor) * m2_to_ft2
    
    #for pressure factor calculation:
    cond_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Input\PRES1").Value * kPa_to_psig    #Aspen in kpa
    if cond_pressure >= 100:     #for pressure factor
        cond_FP = 0.9803 + 0.018 * (cond_pressure / 100) + 0.0017 * (cond_pressure / 100)**2
    else:
        cond_FP = 1  
    
    #for material factor calculation:
    cond_FM = 1
    
    #base costs
    if cond_area < 150:       #Douple pipe HE is taken for small areas
        if cond_area < 2: 
            print("")
        cond_base_costs = np.exp(7.1460 + 0.16 * np.log(cond_area))
    else:
        cond_FL = 1.05     #tube-length correction factor, tube length of 16 ft chosen
        cond_base_costs = np.exp(11.0545 - 0.9228 * np.log(cond_area) + 0.09861 * (np.log(cond_area))**2)*cond_FL 
    
    #purchase costs:
    cond_purchase_costs = cond_FM * cond_FP * cond_base_costs
    cond_purchase_costs_current = current_cost_index / cost_index_2006 * cond_purchase_costs

    return cond_purchase_costs_current, cond_Q





#This function gives as output the current costs of the kettle reboiler of the DWSTU column model used in Aspen Plus (cond_purchase_costs_current), and the heat duty (cond_Q)
#As input required is the application (aspen Plus python connection), the name of the DWSTU column defined in Aspen Plus (nameRADFRAC)
#the fouling factor, e.g. 0.9 as a heuristic, and the cost index of the year where CAPEX is to be calculated
def condenserDWSTU(Application, nameDWSTU, fouling_factor, current_cost_index):
    #for area calculation:
    cond_Q = np.abs(Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\COND_DUTY").Value)
    cond_U = 1140         #W/m2/°C 
    cond_cold_in = 30 + 273.15      #K cooling water defined inlet temperature
    cond_cold_out = 45 + 273.15
    cond_hot = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Output\DISTIL_TEMP").Value
    cond_LMTD = (cond_cold_out-cond_cold_in)/np.log((cond_hot-cond_cold_in)/(cond_hot-cond_cold_out))
    cond_area = cond_Q / (cond_U * cond_LMTD * fouling_factor) * m2_to_ft2
    
    #for pressure factor calculation:
    cond_pressure = Application.Tree.FindNode("\Data\Blocks\\" + nameDWSTU + "\Input\PTOP").Value * kPa_to_psig    #Aspen in kpa
    if cond_pressure >= 100:     #for pressure factor
        cond_FP = 0.9803 + 0.018 * (cond_pressure / 100) + 0.0017 * (cond_pressure / 100)**2
    else:
        cond_FP = 1  
    
    #for material factor calculation:
    cond_FM = 1
    
    #base costs
    if cond_area < 150:       #Douple pipe HE is taken for small areas
        if cond_area < 2: 
            print("")
        cond_base_costs = np.exp(7.1460 + 0.16 * np.log(cond_area))
    else:
        cond_FL = 1.05     #tube-length correction factor, tube length of 16 ft chosen
        cond_base_costs = np.exp(11.0545 - 0.9228 * np.log(cond_area) + 0.09861 * (np.log(cond_area))**2)*cond_FL 
    
    #purchase costs:
    cond_purchase_costs = cond_FM * cond_FP * cond_base_costs
    cond_purchase_costs_current = current_cost_index / cost_index_2006 * cond_purchase_costs

    return cond_purchase_costs_current, cond_Q

