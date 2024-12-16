# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2021 replay file
# Internal Version: 2020_03_06-15.50.37 167380
# Run by adam-ua769pu3t3n7k4o on Mon Dec 16 08:22:49 2024
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.55729, 1.55556), width=229.233, 
    height=154.311)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile(
    's:/Junior/abaqus-with-python/otimization-scripts/otimization-algorithm-with-pso-and-dsa/geometry/geometry_manager.py', 
    __main__.__dict__)
#: The model "restartMode" has been created.
#: The model "Model-1" has been created.
#: Warning: Index 4 in the sequence is out of range
#: Warning: Index 5 in the sequence is out of range
#: Warning: Index 6 in the sequence is out of range
#: The interaction property "chip-plate-contact" has been created.
#: The interaction property "self-contact" has been created.
#: The interaction property "tool-chip-contact" has been created.
#: The interaction "contact" has been created.
#: The model "Model-1" has been created.
#: Warning: Index 4 in the sequence is out of range
#: Warning: Index 5 in the sequence is out of range
#: Warning: Index 6 in the sequence is out of range
#: The interaction property "chip-plate-contact" has been created.
#: The interaction property "self-contact" has been created.
#: The interaction property "tool-chip-contact" has been created.
#: The interaction "contact" has been created.
#: The model database has been saved to "S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results\inp-and-simulation\defaut\CAE\simulation_cae.cae".
print 'RT script done'
#: RT script done
