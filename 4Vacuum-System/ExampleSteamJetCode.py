# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:59:12 2023

@author: Ann-Joelle
"""


import os                          # Import operating system interface
import win32com.client as win32    # Import COM
import numpy as np


from vacuumoperation import vacuumsystemSTEAMJET

kPa_to_Torr = 7.50062
kg_to_lb = 2.20462
m3_to_ft3 = 35.3147

#%% Aspen Plus Connection

# 1. Specify file name
file = 'exampleSteamJet.bkp'  

# 2. Get path to Aspen Plus file
aspen_Path = os.path.abspath(file)
print(aspen_Path)
 

# 3 Initiate Aspen Plus application
print('\n Connecting to the Aspen Plus... Please wait ')
Application = win32.Dispatch('Apwn.Document') # Registered name of Aspen Plus
print('Connected!')

# 4. Initiate Aspen Plus file
Application.InitFromArchive2(aspen_Path)    

# 5. Make the files visible
Application.visible = 1   

#%% Constants and Inputs

#cost factors 
cost_index_2019 = 607.5


#constants 
F_M = 1
r_liquid_fill = 0.65


#pressure and volume of the vacuum system
v_pressure = Application.Tree.FindNode("\Data\Blocks\REACTOR\Input\PRES").Value    #kpa
v_volume = Application.Tree.FindNode("\\Data\\Blocks\\REACTOR\\Output\\LIQ_VOL").Value / r_liquid_fill #kPa

#airleakage through joints is calculated according to formula in Seider et al.(2008)
v_air_leakage = (5 + (0.0298 + 0.03088 * np.log(v_pressure * kPa_to_Torr) - 0.0005733 * (np.log(v_pressure * kPa_to_Torr))**2) * ((v_volume)*m3_to_ft3)**0.66) / kg_to_lb / 3600         #formula from seider for air leakage rate in lb / hr converted to kg/s
Application.Tree.FindNode("\Data\Streams\AIR\Input\TOTFLOW\MIXED").Value = v_air_leakage     #give to aspen the air flow in lb/hr
Application.Engine.Run2()

#loss of volatile compounds at temperature of steam jet ejector and air flow
#this variable can be obtained by putting a flash and obtaining the equilibrium at that temperature and composition, the gas stream corresponds to 
#the volatile compound stream that will be lost to the vacuum system and the input airflow
flowrate_to_steamjet = Application.Tree.FindNode("\Data\Streams\FLASHGAS\Output\STR_MAIN\MASSFLMX\MIXED").Value     #kg/s

#%% Function call

v_costs_purchase2019, steam_consumption = vacuumsystemSTEAMJET(Application, v_pressure, v_volume, flowrate_to_steamjet, F_M, cost_index_2019)

v_total_costs = np.sum(v_costs_purchase2019)
