# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 22:27:26 2023

@author: Ann-Joelle
"""

import os                          # Import operating system interface
import win32com.client as win32    # Import COM
import numpy as np


from Reactor import  reactorCSTR
 

#%% Aspen Plus Connection

# 1. Specify file name
file = 'CSTR2.bkp'  

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

r_h_d_ratio = 3
F_M_R = 2.1     #Stainless steel 316
r_rho = 8000  #density titanium in kg/m3
r_liquid_fill = 0.65
reactor_name = "CSTR"

#%% Function call

r_volume, r_costs_puchase2019 = reactorCSTR(Application, r_liquid_fill, r_h_d_ratio, F_M_R, r_rho, reactor_name, cost_index_2019)
    

