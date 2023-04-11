# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:15:04 2023

@author: Ann-Joelle
"""
import numpy as np
\

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



def reactorCSTR(Application, r_liquid_fill, r_h_d_ratio, F_M, rho, namereactor, current_cost_index):

    
    """
    This function calculates the costs and volume of a modelled CSTR reactor in Aspen Plus, by retrieving values from Aspen Plus.
        
    Parameters
    ----------
    Application : Aspen Plus Python Connection
    r_liquid_fill : Liquid level of the reactor (e.g. 0.65 for 65% fill)
    r_h_d_ratio : Height to diameter ratio (e.g. 3 for many horizontal vessels)
    F_M : Material factor (e.g. 2.1 for stainless steel (Seider et al. (2009))
    rho : Density of the material of the reactor (e.g. for stainless steel 8000 kg/m3 )
    namereactor : given name of the reactor in the Aspen Plus simulation
    current_cost_index : cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019)

    Returns
    -------
    r_volume : reactor volume in m3 (not liquid volume)
    r_costs_puchase_current : purchase costs of the reactor

    """
    
    #include whether material should be stainless steel or what
    #geometry
    r_volume = Application.Tree.FindNode("\\Data\\Blocks\\" + namereactor + "\\Output\\LIQ_VOL").Value / r_liquid_fill
    r_diameter = ((r_volume*4)/(r_h_d_ratio*np.pi))**(1/3)
    r_tangent_tangent_length = r_diameter * r_h_d_ratio
    r_lowest_pressure = Application.Tree.FindNode("\Data\Blocks\\" + namereactor + "\\Output\B_PRES").Value * 0.001 #multipliziert da Aspen in N/sqm gibt
    
    
    if r_lowest_pressure <= 34.5: #kpa
        r_design_pressure = 10.0 #psig
        #print("the design pressure of the reactor is", r_design_pressure, "psig \n")
    elif r_lowest_pressure > 34.5 and r_lowest_pressure <= 6895:
        r_design_pressure = np.exp(0.60608 + 0.91615 * np.log(r_lowest_pressure*kPa_to_psig) + 0.0015655*(np.log(r_lowest_pressure*kPa_to_psig))**2)
        #print("the design pressure of the reactor is", r_design_pressure, "psig \n")
    elif r_lowest_pressure >= 6895:
        r_design_pressure = 1.1 * r_lowest_pressure*kPa_to_psig
    
    r_temp = Application.Tree.FindNode("\Data\Blocks\\" + namereactor + "\\Output\B_TEMP").Value      #K
    r_design_temp = (r_temp - 273.15) * 9/5 + 32.0 + 50.0           #Fahrenheit
    
    if r_design_temp >= -20 and r_design_temp <= 750:
        r_allowable_stress = 15000
    elif r_design_temp <= 800: 
        r_allowable_stress = 14750
    elif r_design_temp <= 850: 
        r_allowable_stress = 14200
    elif r_design_temp <= 900: 
        r_allowable_stress = 13100
    else:
        print("Warning!! reactor design temperature is too high for wall thickness calculation from seider ")
    
    if r_design_temp >= -20.0 and r_design_temp < 200.0 :
        r_E_modulus = 30.2 *10**6
    elif r_design_temp >= 200.0 and r_design_temp < 400.0 :
        r_E_modulus = 29.5 *10**6
    elif r_design_temp >= 400.0 and r_design_temp < 650.0 :
        r_E_modulus = 28.3 *10**6
    else:
        r_E_modulus = 26.0 *10**6
        
        
    if r_lowest_pressure * 0.001 >= 101:         #101 kpa for atmospheric pressure 
        r_t_total = (r_design_pressure * (r_diameter*m_to_inch))/(2*r_allowable_stress-1.2*r_design_pressure)
        
    else:   #vacuum operation
        r_tE1 = 0.25
        error = 1
        
        while abs(error) > 0.001:
            r_tE = 1.3 * ((r_diameter*m_to_inch)+r_tE1) * ((r_design_pressure * (r_tangent_tangent_length*m_to_inch))/(r_E_modulus*((r_diameter*m_to_inch)+r_tE1)))**0.4
            error = (r_tE1 - r_tE)/r_tE1
            r_tE1 = r_tE
            
        check = r_tE/(r_diameter*m_to_inch)
        if check >= 0.05 :
            print("Warning!! the wall thickness of the distillation column did not pass the methods. \n")
        
        r_tEC = (r_tangent_tangent_length*m_to_inch) * (0.18*(r_diameter*m_to_inch)-2.2)*10**(-5) - 0.19
        
        if r_tEC > 0 :
            r_t_total = r_tEC + r_tE + 0.125       # 0.125 for corrosive allowance add up 
        else : 
            r_t_total = r_tE + 0.125               # 0.125 corrosive allowance add up 
    
    
    if r_t_total < 0.25:        #minimum wall thickness
        r_t_total = 0.25
    
    r_weight = np.pi*r_t_total * (rho*kg_to_lb/m3_to_in3) * ((r_diameter*m_to_inch) + r_t_total) * ((r_tangent_tangent_length*m_to_inch) + 0.8 * (r_diameter*m_to_inch))
    
    
    #Costs
    if r_weight < 4200 or r_weight > 1000000:
        print("Warning!! No range to apply the cost function for empty reaction vessel from Seider.\n")
    r_costs_vessel = np.exp(7.0132 + 0.18255 * np.log(r_weight) + 0.02297 * (np.log(r_weight))**2)
    
    if (r_diameter * m_to_ft )< 3 or (r_tangent_tangent_length * m_to_ft) < 27:
        print("Warning!! No range to apply the cost function for added costs from Seider.\n") 
    r_added_costs = 361.8 * ((r_diameter*m_to_ft))**0.73960 * ((r_tangent_tangent_length*m_to_ft))**0.70684
    
    r_costs_purchase = F_M * r_costs_vessel + r_added_costs 
    r_costs_puchase_current = current_cost_index / cost_index_2006 * r_costs_purchase
    
    return r_volume, r_costs_puchase_current

