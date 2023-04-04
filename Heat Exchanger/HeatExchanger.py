# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:58:29 2023

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

#Operating year
hr_per_day = 24
day_per_year = 365
operating_factor = 0.9 

#cost factors of equations from Seider et al.
cost_index_2006 = 500



def heatexchanger(Application, No_Heat_Exchanger, fouling_factor, E_FL, current_cost_index):
    
    E_T = np.zeros(No_Heat_Exchanger)
    E_Q = np.zeros((No_Heat_Exchanger))
    E_U = np.zeros(No_Heat_Exchanger)
    E_area = np.zeros((No_Heat_Exchanger))
    E_LMTD = np.zeros(No_Heat_Exchanger)
    E_pressure = np.zeros(No_Heat_Exchanger)
    E_FP = np.zeros(No_Heat_Exchanger)
    E_FM = np.zeros(No_Heat_Exchanger)
    E_base_costs = np.zeros(No_Heat_Exchanger)
    E_purchase_costs = np.zeros(No_Heat_Exchanger)
    E_purchase_costs_current = np.zeros(No_Heat_Exchanger)
    streamname = np.zeros(No_Heat_Exchanger)
    watercontent = np.zeros(No_Heat_Exchanger)
    E_Q_BTU = np.zeros(No_Heat_Exchanger)

    
    i=0
    for i in range(1,No_Heat_Exchanger+1):
        
        try:                #because paths a called differently for different type of heat exchangers
            E_T[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\COLD_TEMP".format(i)).Value
        except: 
            print()
        
        try: 
            E_T[i-1] = Application.Tree.FindNode("\Data\Blocks\E0{}\Output\B_TEMP".format(i)).Value
        except: 
            print()
            
        
        if E_T[i-1] < 252+273.15 :        #Because else no heat exchanger but fired heater (for T above 252C)
        
            #for area calculation:
            E_Q[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\HX_DUTY".format(i)).Value
            E_U[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Input\\U".format(i)).Value    #W/m2/C
            E_LMTD[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\HX_DTLM".format(i)).Value   #K
            E_area[i-1] = E_Q[i-1] / (E_U[i-1] * E_LMTD[i-1] * fouling_factor) * m2_to_ft2      #in ft2
            
            
            
            if E_area[i-1] < 150:       #Douple pipe HE is taken for small areas
                
                #for pressure factor calculation:
                E_pressure[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\COLDINP".format(i)).Value * N_m2_to_psig    #Aspen in N/m2
                if E_pressure[i-1] >= 600:     #for pressure factor
                    E_FP[i-1] = 0.851 + 0.1292 * (E_pressure[i-1] / 600) + 0.0198 * (E_pressure[i-1] / 600)**2
                else:
                    E_FP[i-1] = 1  
    
                #for material factor calculation:
                try:        #because there is a difference between coolers and heaters (coldin / hotin) HEATER
                    streamname = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\COLDIN".format(i)).Value      #Name of inlet stream
                    watercontent = Application.Tree.FindNode("\\Data\\Streams\\{}\\Output\\STR_MAIN\\MASSFRAC\\MIXED\\WATER".format(streamname)).Value
                except:
                    print()
        
                try:        #COOLER
                    streamname = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\HOTIN".format(i)).Value      #Name of inlet stream
                    watercontent = Application.Tree.FindNode("\\Data\\Streams\\{}\\Output\\STR_MAIN\\MASSFRAC\\MIXED\\WATER".format(streamname)).Value
                except:
                    print()
            
                if watercontent >= 0.99:
                    E_FM = 1           #carbon steel / carbon steel for water / steam
                else: 
                    E_FM = 1.75 + (E_area[i-1] / 100)**0.13        #stainless steel / carbon steel for else
            
                #base costs
                if E_area[i-1] < 2: 
                    print("Warning!! No range to apply the cost function for double pipe base from Seider.\n")
                E_base_costs[i-1] = np.exp(7.1460 + 0.16 * np.log(E_area[i-1]))
    
    
    
            else:       #Shell and Tube HE is taken for areas above 150 ft2 
            #!check this again, no example!
                
                #for pressure factor calculation:
                E_pressure[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\COLDINP".format(i)).Value * N_m2_to_psig    #Aspen in N/m2
                if E_pressure[i-1] >= 100:     #for pressure factor
                    E_FP[i-1] = 0.9803 + 0.018 * (E_pressure[i-1] / 100) + 0.0017 * (E_pressure[i-1] / 100)**2 
                else:
                    E_FP[i-1] = 1  
    
                #for material factor calculation:
                try:        #because there is a difference between coolers and heaters (coldin / hotin) HEATER
                    streamname = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\COLDIN".format(i)).Value      #Name of inlet stream
                    watercontent = Application.Tree.FindNode("\\Data\\Streams\\{}\\Output\\STR_MAIN\\MASSFRAC\\MIXED\\WATER".format(streamname)).Value
                except:
                    print()
        
                try:        #COOLER
                    streamname = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\HOTIN".format(i)).Value      #Name of inlet stream
                    watercontent = Application.Tree.FindNode("\\Data\\Streams\\{}\\Output\\STR_MAIN\\MASSFRAC\\MIXED\\WATER".format(streamname)).Value
                except:
                    print()
            
                if watercontent >= 0.99:
                    E_FM = 1           #carbon steel / carbon steel for water / steam
                else: 
                    E_FM = 1.75 + (E_area[i-1] / 100)**0.13        #stainless steel / carbon steel for else
                
                #base costs
                E_base_costs[i-1] = np.exp(11.0545 - 0.9228 * np.log(E_area[i-1]) + 0.09861 * (np.log(E_area[i-1]))**2)*E_FL     #Fixed Head Shell Tube
    
    
    
        elif E_T[i-1] > 252+273.15 and E_T[i-1] <= 300+273.15:
            
            E_Q[i-1] = Application.Tree.FindNode("\Data\Blocks\E0{}\Output\QCALC".format(i)).Value  #Aspen in W
            E_Q_BTU[i-1] = E_Q[i-1] * W_to_Btu_hr   
            
            E_pressure[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\B_PRES".format(i)).Value * N_m2_to_psig    #Aspen in N/m2
        
            if E_pressure[i-1] >= 500:     #for pressure factor
                E_FP[i-1] = 0.986 - 0.0035 * (E_pressure[i-1] / 500) + 0.0175 * (E_pressure[i-1] / 500)**2
            else:
                E_FP[i-1] = 1  
            
            E_FM = 1.7
            
            if E_Q_BTU[i-1] < 10 or E_Q_BTU[i-1] > 500 * 10**6: 
                print("Warning!! No range to apply the cost function for fired heater base from Seider.\n")
            E_base_costs[i-1] = np.exp(0.32325 + 0.766 * np.log(E_Q_BTU[i-1]))
        
        
        
        elif E_T[i-1] > 250+273.15 :
            
            E_Q[i-1] = Application.Tree.FindNode("\Data\Blocks\E0{}\Output\QCALC".format(i)).Value  #Aspen in W
            E_Q_BTU[i-1] = E_Q[i-1] * W_to_Btu_hr   
            
            E_pressure[i-1] = Application.Tree.FindNode("\\Data\\Blocks\\E0{}\\Output\\B_PRES".format(i)).Value * N_m2_to_psig    #Aspen in N/m2
        
            if E_pressure[i-1] >= 500:     #for pressure factor
                E_FP[i-1] = 0.986 - 0.0035 * (E_pressure[i-1] / 500) + 0.0175 * (E_pressure[i-1] / 500)**2
            else:
                E_FP[i-1] = 1  
            
            E_FM = 1.7 
            
            if E_Q_BTU[i-1] < 10 or E_Q_BTU[i-1] > 70 * 10**6: 
                print("Warning!! No range to apply the cost function for fired heater base from Seider.\n")
            E_base_costs[i-1] = 12.74 * E_Q_BTU[i-1]**0.65
            
            
            
        #purchase costs:
        E_purchase_costs[i-1] = E_FM * E_FP[i-1] * E_base_costs[i-1]
        E_purchase_costs_current[i-1] = current_cost_index / cost_index_2006 * E_purchase_costs[i-1]
        
        
    E_totalcosts = np.sum(E_purchase_costs_current)

    return E_totalcosts, E_purchase_costs_current, E_Q, E_area