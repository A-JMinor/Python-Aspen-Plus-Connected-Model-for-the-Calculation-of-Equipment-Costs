# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:27:23 2023

@author: Ann-Joelle
"""

import numpy as np
import math

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

#Operating year
hr_per_day = 24
day_per_year = 365
operating_factor = 0.9 

#cost factors of equations from Seider et al. 2006 
cost_index_2006 = 500

#input evap_hotutility_temperature is vector of size of Number of evaporators
def verticalEVAPORATORS(Application, No_Evaporators, souders_brown_param, L_D_ratio, evap_U, evap_hotutility_temperature, fouling_factor, current_cost_index):
    
    evap_volume = np.zeros(No_Evaporators)
    evap_Q = np.zeros(No_Evaporators)
    evap_area = np.zeros(No_Evaporators)
    evap_purchase_costs_current = np.zeros(No_Evaporators)
    
    i=0
    for i in range(1,No_Evaporators+1):
    
        #horizontal vessel diameter calculation based on Souders Brown parameter and maximum gas velocity 
        #call evaporators "EVAP1", EVAP2.. and the streams on top and bottom, EVAP1TOP, EVAP1BOTTOM respecitvely
        evap_vapor_flowrate = Application.Tree.FindNode("\\Data\\Streams\\EVAP{}TOP\\Output\\STR_MAIN\\VOLFLMX\\MIXED".format(i)).Value       #m3/s
        evap_rho_vapor = Application.Tree.FindNode("\Data\Streams\EVAP{}TOP\Output\STR_MAIN\MASSFLMX\MIXED".format(i)).Value / Application.Tree.FindNode("\Data\Streams\EVAP{}TOP\Output\STR_MAIN\VOLFLMX\MIXED".format(i)).Value     #kg/m3
        evap_rho_liquid = Application.Tree.FindNode("\Data\Streams\EVAP{}BOT\Output\STR_MAIN\MASSFLMX\MIXED".format(i)).Value / Application.Tree.FindNode("\Data\Streams\EVAP{}BOT\Output\STR_MAIN\VOLFLMX\MIXED".format(i)).Value    #kg/m3
        evap_max_gasvelocity = souders_brown_param * math.sqrt((evap_rho_liquid - evap_rho_vapor)/evap_rho_vapor)
        evap_diameter = math.sqrt(evap_vapor_flowrate * 4 / math.pi / evap_max_gasvelocity)
        evap_length = L_D_ratio * evap_diameter
        evap_volume[i-1] = math.pi / 4 * evap_diameter**2 * evap_length
        
        #for area calculation:
        evap_Q[i-1] = Application.Tree.FindNode("\Data\Blocks\EVAP{}\Output\QCALC".format(i)).Value
        evap_cold = Application.Tree.FindNode("\Data\Blocks\EVAP{}\Input\TEMP".format(i)).Value
        evap_LMTD = evap_hotutility_temperature[i-1] - evap_cold
        evap_area[i-1] = evap_Q[i-1] / (evap_U * evap_LMTD * fouling_factor) * m2_to_ft2
        
        evap_purchase_costs = 5700 * evap_area[i-1]**0.55
        evap_purchase_costs_current[i-1] = current_cost_index / cost_index_2006 * evap_purchase_costs
        evap_total_costs = np.sum(evap_purchase_costs_current)
    
    return evap_volume, evap_Q, evap_area, evap_purchase_costs_current, evap_total_costs

