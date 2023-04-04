# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:23:28 2022

@author: Ann-Joelle
"""

import os                          # Import operating system interface
import win32com.client as win32    # Import COM
import numpy as np


from HeatExchanger import  heatexchanger
 

#%% Aspen Plus Connection

# 1. Specify file name
file = 'CumenePlant4.bkp'  

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

#number of heat exchangers
No_Heat_Exchanger = 8

#constants
fouling_factor = 0.9
E_FL = np.ones(No_Heat_Exchanger) * 1.05     #Tube length correction factor for shell and tube heat exchanger according to Seider (2008)
E_FM = np.ones(No_Heat_Exchanger)  #only carbon steel chosen

#%% Function Call

E_totalcosts, E_purchase_costs2019, E_Q, E_area = heatexchanger(Application, No_Heat_Exchanger, fouling_factor, E_FM, E_FL, cost_index_2019)




