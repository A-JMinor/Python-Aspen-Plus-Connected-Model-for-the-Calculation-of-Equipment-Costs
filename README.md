# Python Aspen Plus Connected Model for the Calculation of Equipment Costs
Python model for the calculation of equipment costs (e.g. for the CSTR reactor, heat exchangers, RADFRAC distillation columns, etc.) that were simulated in Aspen Plus. The python code retrieves data from Aspen Plus, applies cost correlations of Seider et al. (2009) using this data, feeds input variables to Aspen Plus (if necessary), runs the simulation (if necessary) and gives the dimensions as well as equipment costs as output.

For this, the connection of Aspen Plus and Python is first required, which is done by pywin32 to provide access, control and automation of Aspen Plus from python.
