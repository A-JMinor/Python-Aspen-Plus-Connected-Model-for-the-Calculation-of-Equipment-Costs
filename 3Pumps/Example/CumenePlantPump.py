# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 22:17:28 2023

@author: Ann-Joelle
"""

import os                          # Import operating system interface
import win32com.client as win32    # Import COM
import numpy as np


from pumps import  pumps
 

#%% Aspen Plus Connection

# 1. Specify file name
file = 'CumenePlant.bkp'  

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
cost_index_2006 = 500

#number of pumps
No_pumps = 3

#constants
pump_material_factor = 2

#%% Function Call

pump_total_costs, pump_purchase_costs2019, pump_motor_purchase_costs2019, pump_head, pump_flowrate = pumps(Application, No_pumps, pump_material_factor, cost_index_2019)

