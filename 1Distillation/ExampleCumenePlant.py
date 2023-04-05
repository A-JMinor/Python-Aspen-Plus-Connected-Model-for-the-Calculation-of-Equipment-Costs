# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:23:28 2022

@author: Ann-Joelle
"""

import os                          # Import operating system interface
import win32com.client as win32    # Import COM
import numpy as np


from Distillation import  distillationRADFRAC, refluxdrumRADFRAC, kettleRADFRAC, condenserRADFRAC
 

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

#constants
fouling_factor = 0.9

#number of equipment pieces
no_towers = 3


#Fixed variables clolum
tray_Spacing = 0.5 #m
flooding = 0.8 #Fractional approach to flooding 
top = 1.2 #m
bottom = 1.8 #m
rho = 0.284 #lb/in3
F_M = 2.1            #material factor stainless steel 316
d_costs_puchase2019 = np.zeros(no_towers)
d_diamter = np.zeros(no_towers)
d_volume = np.zeros(no_towers)


#Fixed variables kettle
fouling_factor = 0.9
kettle_U = 1140         #W/m2/°C 
kettle_hotutility_temperature = []
kettle_purchase_costs2019 = np.zeros(no_towers)
kettle_Q = np.zeros(no_towers)
kettle_area = np.zeros(no_towers)


#Fixed variables condenser
cond_purchase_costs2019 = np.zeros(no_towers)
cond_Q = np.zeros(no_towers)


#Fixed variables reflux drum
drum_residence_time = 300        #s
drum_filled = 0.5       #half filled
drum_l_to_d = 3
drum_costs_puchase2019 = np.zeros(no_towers)
drum_volume = np.zeros(no_towers)


#%% Function Call

i=0
for i in range(1,no_towers+1):
    

    nameRADFRAC = "RAD{}".format(i)
    
    #distillation column    
    d_costs_puchase2019[i-1], d_diamter[i-1], d_volume[i-1] = distillationRADFRAC(Application, nameRADFRAC, tray_Spacing, top, bottom, rho, F_M, cost_index_2019)

    
    #kettle reboiler
    kettle_T = Application.Tree.FindNode("\Data\Blocks\\" + nameRADFRAC + "\Output\BOTTOM_TEMP").Value 
    #utility kettle 
    if kettle_T <= 120+273.15:
        kettle_hotutility_temperature.append(138.9 + 273.15)    #LP Steam
    
    elif kettle_T <= 170+273.15 and kettle_T > 120+273.15:
        kettle_hotutility_temperature.append(186 + 273.15)     #MP Steam
    
    elif kettle_T <= 255+273.15 and kettle_T > 170+273.15:
        kettle_hotutility_temperature.append(270 + 273.15)     #HP Steam
    
    elif kettle_T <= 300+273.15 and kettle_T > 255+273.15:
        kettle_hotutility_temperature.append(337.8  + 273.15)     #FuelOilNo2 Steam
    
    elif kettle_T <= 380+273.15 and kettle_T > 300+273.15:
        kettle_hotutility_temperature.append(400 + 273.15)     #DowthermA Steam
    
    else:
        print("kettle temperature out of range")

    kettle_purchase_costs2019[i-1], kettle_Q[i-1], kettle_area[i-1] = kettleRADFRAC(Application, nameRADFRAC, kettle_hotutility_temperature[i-1], kettle_U,fouling_factor, cost_index_2019)
    
    
    #condenser
    cond_purchase_costs2019[i-1], cond_Q[i-1] = condenserRADFRAC(Application,nameRADFRAC, fouling_factor, cost_index_2019)

    
    #reflux drum
    name_distallestream_DWSTU = "RADTOP{}".format(i)
    
    drum_costs_puchase2019[i-1], drum_volume[i-1] = refluxdrumRADFRAC(Application, nameRADFRAC, name_distallestream_DWSTU, drum_residence_time, drum_filled, drum_l_to_d, rho, F_M, cost_index_2019)
    

