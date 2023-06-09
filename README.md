# Python Aspen Plus Connected Model for the Calculation of Equipment Costs
Python model for the calculation of equipment costs (e.g. for the CSTR reactor, heat exchangers, RADFRAC distillation columns, etc.) that were simulated in Aspen Plus. The python code retrieves data from Aspen Plus, applies cost correlations of Seider et al. (2008)[^1] using this data, feeds input variables to Aspen Plus (if necessary), runs the simulation (if necessary) and gives the dimensions as well as equipment costs as output.

## Prerequisites
In this repo, the prerequisites are just mentioned or shortly explained here. There is a [detailed example](https://github.com/edgarsmdn/Aspen_Plus_Python#aspen-plus-python-connection-example) providing an entire python and aspen plus file at @edgarsmdn. There, a sensitivity analysis is performed where the python code is feeding / retrieving data to / from Aspen Plus.

### Connection between Aspen Plus and Python
The connection between Aspen Plus and Python is first required, which is done by pywin32 to provide access, control and automation of Aspen Plus from python. Hence, each package starts with this connection, and an example code for assessing an aspen plus backup file with the name "*simulation*" can be found below. 

```ruby
# 0) Import packages
import os                          # Import operating system interface
import win32com.client as win32    # Import COM

# 1) Get path to Aspen Plus backup file called simulation
file_name = 'simulation.bkp'
aspen_path = os.path.abspath(file)

# 2) Initiate Aspen Plus application and file
Application = win32.Dispatch('Apwn.Document') # Registered name of Aspen Plus
Application.InitFromArchive2(aspen_path)

# 3) Application becomes visible with 
Application.visible = 1
```

### Obtain an input/output Variable from Aspen Plus
To be able to use Aspen Plus as a blackbox model, and control its variables from Python (e.g. change the input variables of or get the results of an Aspen Plus simulation process), the "*path*" of the required Aspen Plus variables are needed. Those path IDs can be found at the *Customize tab* at *Variable Explorer* in Aspen Plus and need to be copy pasted to python. A screenshot explaining how to obtain a certain variable such as the value of the mole fraction of heptane is shown in the [Aspen Plus Python Connection Example](https://github.com/edgarsmdn/Aspen_Plus_Python#aspen-plus-python-connection-example). An example python command to save this molefraction of stream "*C7*" as variable x is shown below. 

```ruby
x = Application.Tree.FindNode("\Data\Streams\C7\Output\MOLEFRAC\MIXED\HEPTANE").Value
```

## Equipment Cost Correlations 
To obtain the CAPEX of a chemical process,  e.g. through Lang factor method, equipment costs are often required. Those equipment costs can be computed by cost correlation functions, that were established in the past by correlating the costs to a certain size factor. For example, to compute the costs of a heat exchanger, the area is required as size factor, and a cost function to compute the *purchase costs ($)* in terms of the area *A* can be found in the literature[^1] dependent on the different types of heat exchangers:

> <img align="center" src="https://github.com/A-JMinor/Python-Aspen-Plus-Connected-Model-for-the-Calculation-of-Equipment-Costs/blob/main/Pictures/purchasecosts.PNG" width="800">
> 
> copied from Seider et al. (2008)[^1]

Hence, this cost correlation is implemented in the python code, which retrieves the value for the heat exchanger area from the Aspen Plus simulation. This python package can be found at the subfolder [Heat Exchanger](0Heat-Exchanger/).

## Included Packages
The costs of the following equipment were computed using the connected python Aspen Plus model: 

[Heat Exchangers](0Heat-Exchanger/)

[Distillation Columns, Reflux Drums, Reboilers, Condensers](1Distillation/)

[Reactors](2Reactor/)

[Pumps](3Pumps/)

[Vacuum Systems](4Vacuum-System/)

[Evaporators](5Evaporator/)

## References
[^1]: W.D. Seider, J.D. Seader, D.R. Lewin, Product and Process Design Principles: Synthesis, Analysis and Design, 3rd Edition, Wiley New York, 2008.
