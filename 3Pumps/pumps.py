# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:40:43 2023

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


def pumps(Application, No_pumps, pump_material_factor, current_cost_index):
    """
    This function calculates the purchase costs of each single pump and motor, the total purchase costs of all pumps and motors combined, and the pump head and flowrate of each pump modelled in Aspen Plus, by retrieving values from Aspen Plus.
    It is necessary to name all pumps in the Aspen Plus simulation according to "P01", "P02", "P03", etc. 
    
    Parameters
    ----------
    Application : Aspen Plus python connection
    No_pumps : how many pumps
    pump_material_factor : material factor for the material of the pumps (e.g. 2 for stainless steel, see Seider et al. (2009))
    current_cost_index : cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019)

    Returns
    -------
    pump_total_costs : float, sum of the costs of all pumps and motors
    pump_motor_purchase_costs_current : array, purchase costs of all motors of the pumps in a vector
    pump_purchase_costs_current : array, purchase costs of all pumps in a vector
    pump_head : array, pump head of all pumps stored in a vector (meters)
    pump_flowrate : array,pump flowrate of all pumps in a vector (in m3/s) 


    """
    
    
    #constants
    earth_acceleration = 9.81       #m/s2
    
    #costs pump
    pump_flowrate = np.zeros(No_pumps)
    pump_head_J_kg = np.zeros(No_pumps)
    pump_head = np.zeros(No_pumps)
    pump_size_factor  = np.zeros(No_pumps)
    pump_electricity = np.zeros(No_pumps)
    pump_base_costs  = np.zeros(No_pumps)
    pump_purchase_costs = np.zeros(No_pumps)
    pump_purchase_costs_current = np.zeros(No_pumps)
    pump_fractional_efficiency = np.zeros(No_pumps)
    pump_liquid_density = np.zeros(No_pumps)
    pump_break_horsepower = np.zeros(No_pumps)
    pump_motor_efficiency = np.zeros(No_pumps)
    pump_power_consumption = np.zeros(No_pumps)
    pump_motor_base_costs = np.zeros(No_pumps)
    pump_motor_purchase_costs = np.zeros(No_pumps)
    pump_motor_purchase_costs_current = np.zeros(No_pumps)
     
    i=0
    for i in range(1,No_pumps+1):
        
        
        pump_flowrate[i-1] = Application.Tree.FindNode(f"\Data\Blocks\P0{i}\Output\VFLOW").Value        #in m3/s
        pump_head_J_kg[i-1] = Application.Tree.FindNode(f"\Data\Blocks\P0{i}\Output\HEAD_CAL").Value    #in J/kg
        pump_head[i-1] = pump_head_J_kg[i-1] / earth_acceleration * m_to_ft     #ft
        pump_size_factor[i-1] = (pump_flowrate[i-1]*m3_s_to_gpm) * pump_head[i-1]**0.5 
        pump_electricity[i-1] = Application.Tree.FindNode(f"\Data\Blocks\P0{i}\Output\ELEC_POWER").Value / HP_to_W   #from Aspen in W to HP
    
        # centrifugal pump for volumetric flowrate from 0.000631 m3/s to 0.3155 m3/s and heads to 3200 ft
        if pump_head[i-1] <= 3200:
            if pump_size_factor[i-1] < 300:
                pump_base_costs[i-1] = np.exp(9.7171 - 0.6019 * np.log(300) + 0.0519 * (np.log(300))**2) * (pump_size_factor[i-1]/300)**0.6
            else: 
                pump_base_costs[i-1] = np.exp(9.7171 - 0.6019 * np.log(pump_size_factor[i-1]) + 0.0519 * (np.log(pump_size_factor[i-1]))**2) 
        
            pump_purchase_costs[i-1] = pump_base_costs[i-1] * pump_material_factor
            pump_purchase_costs_current[i-1] = current_cost_index / cost_index_2006 * pump_purchase_costs[i-1]
            
            
            #costs motor of pumps (electric motor)
            if pump_flowrate[i-1]*m3_s_to_gpm < 50 :
                pump_fractional_efficiency[i-1] = (-0.316 + 0.24015 * (np.log(50)) - 0.01199 * (np.log(50))**2) * (pump_flowrate[i-1]*m3_s_to_gpm/50)**0.6
            else : 
                pump_fractional_efficiency[i-1] = (-0.316 + 0.24015 * (np.log(pump_flowrate[i-1]*m3_s_to_gpm)) - 0.01199 * (np.log(pump_flowrate[i-1]*m3_s_to_gpm))**2)
            

            pump_liquid_density[i-1] = Application.Tree.FindNode(f"\Data\Blocks\P0{i}\Output\BAL_MASI_TFL").Value / pump_flowrate[i-1] * kg_m3_to_lb_gal     #Aspen plus kg/s / m3/s to lb/gal
            pump_break_horsepower[i-1] = pump_head[i-1] * pump_flowrate[i-1] * m3_s_to_gpm * pump_liquid_density[i-1] / (33000 * pump_fractional_efficiency[i-1])   #HP
            
            if pump_break_horsepower[i-1] > 1500 :
                print('Error Horsepower too high for applying efficiency equation for motor')
                
            pump_motor_efficiency[i-1] = 0.8 + 0.0319 * np.log(pump_break_horsepower[i-1]) - 0.00182 * (np.log(pump_break_horsepower[i-1]))**2

            pump_power_consumption[i-1] = pump_break_horsepower[i-1] / pump_motor_efficiency[i-1]
        
            pump_motor_base_costs[i-1] = np.exp(5.8259 + 0.13141 * np.log(pump_power_consumption[i-1]) + 0.053255 * (np.log(pump_power_consumption[i-1]))**2 + 0.028628 * (np.log(pump_power_consumption[i-1]))**3 - 0.0035549 * (np.log(pump_power_consumption[i-1]))**4)
            pump_motor_purchase_costs[i-1] = pump_motor_base_costs[i-1] * pump_material_factor
            pump_motor_purchase_costs_current[i-1] = current_cost_index / cost_index_2006 * pump_motor_purchase_costs[i-1]
            
        
        
        #reciprocating plunder pumps best for most demanding applications and for wider range of flowrates
        #includes V belt drive
        #unfortunaletly materal factor is different than the one above        
        elif pump_head[i-1] > 3200:
        
            pump_fractional_efficiency[i-1] = 0.9
            pump_liquid_density[i-1] = Application.Tree.FindNode(f"\Data\Blocks\P0{i}\Output\BAL_MASI_TFL").Value / pump_flowrate[i-1] * kg_m3_to_lb_gal     #Aspen plus kg/s / m3/s to lb/gal
            pump_break_horsepower[i-1] = pump_head[i-1] * pump_flowrate[i-1] * m3_s_to_gpm * pump_liquid_density[i-1] / (33000 * pump_fractional_efficiency[i-1])
            
            pump_base_costs[i-1] = np.exp(7.8103 + 0.26986 * np.log(pump_break_horsepower[i-1]) + 0.06718 * np.log(pump_break_horsepower[i-1])**2)
            pump_purchase_costs[i-1] = pump_base_costs[i-1] * pump_material_factor
            pump_purchase_costs_current[i-1] = current_cost_index / cost_index_2006 * pump_purchase_costs[i-1]
            
            if pump_break_horsepower[i-1] > 200 or pump_break_horsepower[i-1] < 1:
                print('reciprocating plunder pump cost equation cannot be applied because pump break horsepower is out of range')

        
        
        
    pump_total_costs = np.sum(pump_motor_purchase_costs_current) + np.sum(pump_purchase_costs_current)

    return pump_total_costs, pump_motor_purchase_costs_current, pump_purchase_costs_current, pump_head/m_to_ft , pump_flowrate
