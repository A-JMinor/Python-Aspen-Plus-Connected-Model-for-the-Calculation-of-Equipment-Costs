# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:57:00 2023

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


#p in kpa, volume in m3, componentloss in kg/s
#for pressures between 2 and 760 torr and gas flowrates up to 1000000 ft3/min
def vacuumsystemSTEAMJET(Application, pressure, volume, flowrate, F_M, current_cost_index):
    """
    This function calculates the costs of a steam jet ejector (vacuum system modelled in Aspen Plus) and gives the steam consumption and flowrate to the vacuum system.
    A steam jet ejector is taken for pressures below 2 kPa according to heuristics in Seider et al (2008). The stages are determined automatically in this function. 

    Parameters
    ----------
    Application : Aspen Plus Python connection
    pressure : float, pressure of the vacuum system in kPa
    volume : float, volume of the vacuum system in m3
    flowrate : float, describes the flowrate in kg/s to the vacuum system (so air flowrate through leakage through joints + volatile compounds at the temperature of steam jet ejector)
    F_M : material factor (see Seider at al. (2008), e.g. 1 for carbon steel)
    current_cost_index : cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019)


    Returns
    -------
    v_costs_purchase_current : float, purchase costs of the steam jet ejector
    steam_consumption : float, consumption of MP steam in kg/s

    """
    

    v_gas_flowrate = flowrate * kg_to_lb * 3600      #lb/hr
    
    v_size_factor = v_gas_flowrate / (pressure * kPa_to_Torr)  #in lb/hr/torr
    
    
    if pressure > 100 / kPa_to_Torr and pressure < 760 / kPa_to_Torr:  
        steam_consumption =  10 * v_gas_flowrate / kg_to_lb / 3600       #kg/s
        v_type_factor = 1       #one stage
        
    elif pressure < 100 / kPa_to_Torr and pressure > 15 / kPa_to_Torr: 
        steam_consumption =  10 * v_gas_flowrate / kg_to_lb / 3600       #kg/s
        v_type_factor = 1.8 * 1.6   #for 1 surface condenser between stages and two stages
        
    elif pressure < 15 / kPa_to_Torr and pressure > 2 / kPa_to_Torr: 
        steam_consumption =  100 * v_gas_flowrate / kg_to_lb / 3600       #kg/s
        v_type_factor = 2.1 * 2.3   #for 2 surface condensers between stages and three stages
        
        
    #purchase costs from seider only from 50 ft3/min: 
    if v_size_factor < 0.1: 
        v_costs_purchase = 1690 * 0.1**0.41 * (v_size_factor/0.1)**0.6 * F_M * v_type_factor
    elif v_size_factor > 0.1 and v_size_factor <= 100:
        v_costs_purchase = 1690 * v_size_factor**0.41 * F_M * v_type_factor
    elif v_size_factor > 100:
        v_costs_purchase = 1690 * 100**0.41 * (v_size_factor/100)**0.6 * F_M * v_type_factor
    
    v_costs_purchase_current = current_cost_index / cost_index_2006 * v_costs_purchase
    
    
    return v_costs_purchase_current, steam_consumption



def vacuumsystemLIQUIDRING(Application, pressure, flowrate, current_cost_index):
    """
    This function calculates the costs of a liquid ring pump (vacuum system modelled in Aspen Plus). A liquid ring pump is taken for pressures down to 2 kPa according to heuristics in Seider et al (2008)


    Parameters
    ----------
    Application : Aspen Plus Python connection
    pressure : float, pressure of the vacuum system in kPa
    flowrate : float, describes the flowrate in m3/s to the vacuum system (so air flowrate through leakage through joints)
    current_cost_index : cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019)

    Returns
    -------
    v_costs_purchase_current : float, purchase costs of the steam jet ejector

    """
    
    v_size_factor = flowrate * m3_to_ft3 * 60           #ft3/min
    
    #purchase costs from seider only from 50 ft3/min: 
    if v_size_factor < 50: 
        v_costs_purchase = 8250 * 50**0.35 * (v_size_factor/50)**0.6
    else: 
        v_costs_purchase = 8250 * v_size_factor**0.35
    
    v_costs_purchase_current = current_cost_index / cost_index_2006 * v_costs_purchase

    return v_costs_purchase_current

