# -*- coding: utf-8 -*-
import os
from abaqus import *
from abaqusConstants import *
import numpy as np
from part import *
from step import *
from material import *
from section import *
from assembly import *
from interaction import *
from mesh import *
from visualization import *
from connectorBehavior import *


class AssemblyModel():
    """
    Class to handle the assembly and simulation process in Abaqus.
    """
    def __init__(self, data, path_INP, path_CAE, filename):
        self.dataInput(data)
        self.assemblyPositions()
        self.stepsAndHistory()
        self.setInteractions()
        self.setContactAndConstraints()
        self.setBoundaryConditionsAndPredefinedFields()
        self.submitSimulation(path_INP, path_CAE, filename)


    def dataInput(self, data):
        """
        Extract input data and set model-level parameters.
        """
        # Calling Model
        self.ModelName = str(data['generalInformation']['modelName'])
        self.m = mdb.models[self.ModelName]
        # Defining Variables
        self.StepName = "CuttingStep"
        self.xToolPosition = data['eulerianData']['createParticionInformation']['x_points'][2] + data['assemblyAndSimulationData']['toolPosition']['clearanceAfterWorkpiece']
        self.yToolPosition = data['eulerianData']['createParticionInformation']['y_points'][3] + data['assemblyAndSimulationData']['toolPosition']['clearanceOverWorkpiece']
        self.xChipPlatePosition = 0
        self.yChipPlatePosition = self.yToolPosition + data['assemblyAndSimulationData']['chipPlatePosition']['clearanceOverWorkpiece']
        self.CuttingDepth = -data['assemblyAndSimulationData']['toolPosition']['cuttingDepth']
        self.TimePeriod = data['assemblyAndSimulationData']['stepsAndHistoryInformation']['timePeriod']
        self.CuttingVelocity = data['assemblyAndSimulationData']['stepsAndHistoryInformation']['cuttingVelocity']


    def assemblyPositions(self):
        """
        Set positions for the assembly components in the simulation.
        """
        # Setting the default coordinate system to Cartesian
        self.m.rootAssembly.DatumCsysByDefault(CARTESIAN)
        # Creating instances of parts in the assembly
        self.m.rootAssembly.Instance(dependent=ON, name='ChipPlate-1', part=self.m.parts['ChipPlate'])
        self.m.rootAssembly.Instance(dependent=ON, name='Eulerian-1', part=self.m.parts['Eulerian'])
        self.m.rootAssembly.Instance(dependent=ON, name='Tool-1', part=self.m.parts['Tool'])
        # Positioning the Chip Plate
        self.m.rootAssembly.translate(instanceList=('ChipPlate-1', ), vector=(self.xChipPlatePosition, self.yChipPlatePosition, 0.0))
        # Positioning the Tool
        self.m.rootAssembly.translate(instanceList=('Tool-1', ), vector=(self.xToolPosition, self.yToolPosition, 0.0))
        # Applying the Feed to the Tool
        self.m.rootAssembly.translate(instanceList=('Tool-1', ), vector=(0.0, self.CuttingDepth, 0.0))
        # Creating an assembly set that includes multiple parts
        self.m.rootAssembly.Set(cells=self.m.rootAssembly.instances['ChipPlate-1'].cells.getSequenceFromMask(mask=('[#1 ]', ), )+\
            self.m.rootAssembly.instances['Eulerian-1'].cells.getSequenceFromMask(mask=('[#ffffffff ]', ), )+\
            self.m.rootAssembly.instances['Tool-1'].cells.getSequenceFromMask(mask=('[#f ]', ), ), name='AssembleSet')
    

    def stepsAndHistory(self):
        """
        Define simulation steps and history outputs.
        """
        # Creating a new step for the simulation
        self.m.TempDisplacementDynamicsStep(improvedDtMethod=ON, name=self.StepName, previous='Initial', timePeriod=self.TimePeriod)
        # Defining field outputs for the new step
        self.m.FieldOutputRequest(createStepName='CuttingStep', name='FieldOutput', variables=('CSTRESS', 'DMICRT', 'ER', 'EVF', 'NT', 'PE', 'PEEQ', 'PEEQMAX', 'RF', 'S', 'SDEG'))
        self.m.fieldOutputRequests['FieldOutput'].setValues(numIntervals=50)
        # Creating history outputs 
        self.m.HistoryOutputRequest(createStepName='CuttingStep', name='CuttingForce', numIntervals=1000, rebar=EXCLUDE, region= self.m.rootAssembly.allInstances['Tool-1'].sets['ToolRP'], sectionPoints=DEFAULT, variables=('RF1', 'RF2'))
        del mdb.models[self.ModelName].fieldOutputRequests['F-Output-1']
        del mdb.models[self.ModelName].historyOutputRequests['H-Output-1']


    def setInteractions(self):
        """
        Define contact interactions between parts.
        """
        # Contact chip-plate-contact
        self.m.ContactProperty('chip-plate-contact')
        self.m.interactionProperties['chip-plate-contact'].TangentialBehavior(dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, table=((0.01, ), ), temperatureDependency=OFF)
        self.m.interactionProperties['chip-plate-contact'].NormalBehavior(allowSeparation=ON, constraintEnforcementMethod=DEFAULT, pressureOverclosure=HARD)
        # Contact self-contact
        self.m.ContactProperty('self-contact')
        self.m.interactionProperties['self-contact'].TangentialBehavior(dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, table=((0.015, ), ), temperatureDependency=OFF)
        self.m.interactionProperties['self-contact'].NormalBehavior(allowSeparation=ON, constraintEnforcementMethod=DEFAULT, pressureOverclosure=HARD)
        # Contact tool-chip-contact
        self.m.ContactProperty('tool-chip-contact')
        table_values = ((0.5544, 0.0), (0.5544, 25.0), (0.5544, 50.0), (0.5544, 75.0), (0.5544, 100.0), (0.5544, 125.0), (0.5544, 150.0), (0.5544, 175.0), (0.5544, 200.0), (0.5544, 225.0), (0.5544, 250.0), (0.5544, 275.0), (0.5544, 300.0), (0.5544, 325.0), (0.5544, 350.0), (0.5544, 375.0), (0.5544, 400.0), (0.5544, 425.0), (0.5544, 450.0), (0.5544, 475.0), (0.5544, 500.0), (0.5544, 525.0), (0.5544, 550.0), (0.5544, 575.0), (0.5544, 600.0), (0.5544, 625.0), (0.5544, 650.0), (0.5544, 675.0), (0.5544, 680.0), (0.5535, 680.1), (0.5084, 700.0), (0.4706, 725.0), (0.4383, 750.0), (0.4088, 775.0), (0.3814, 800.0), (0.3554, 825.0), (0.3306, 850.0), (0.3067, 875.0), (0.2836, 900.0), (0.2612, 925.0), (0.2394, 950.0), (0.2181, 975.0), (0.1972, 1000.0), (0.1768, 1025.0), (0.1567, 1050.0), (0.137, 1075.0), (0.1177, 1100.0), (0.0986, 1125.0), (0.0798, 1150.0), (0.0613, 1175.0), (0.043, 1200.0), (0.0249, 1225.0), (0.0071, 1250.0), (0.0, 1260.0), (0.0, 1350.0), (0.0, 1375.0), (0.0, 1400.0), (0.0, 1425.0), (0.0, 1450.0), (0.0, 1475.0), (0.0, 1500.0), (0.0, 1525.0), (0.0, 1550.0), (0.0, 1575.0), (0.0, 1600.0), (0.0, 1625.0), (0.0, 1650.0), (0.0, 1675.0), (0.0, 1700.0), (0.0, 1725.0), (0.0, 1750.0), (0.0, 1775.0), (0.0, 1800.0), (0.0, 1825.0), (0.0, 1850.0), (0.0, 1875.0), (0.0, 1900.0), (0.0, 1925.0), (0.0, 1950.0), (0.0, 1975.0), (0.0, 2000.0), (0.0, 2025.0), (0.0, 2050.0), (0.0, 2075.0), (0.0, 2100.0), (0.0, 2125.0), (0.0, 2150.0), (0.0, 2175.0), (0.0, 2200.0), (0.0, 2225.0), (0.0, 2250.0), (0.0, 2275.0), (0.0, 2300.0), (0.0, 2325.0), (0.0, 2350.0), (0.0, 2375.0), (0.0, 2400.0), (0.0, 2425.0), (0.0, 2450.0), (0.0, 2475.0), (0.0, 2500.0))
        self.m.interactionProperties['tool-chip-contact'].TangentialBehavior(dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, table=table_values, temperatureDependency=ON)
        self.m.interactionProperties['tool-chip-contact'].NormalBehavior(allowSeparation=ON, constraintEnforcementMethod=DEFAULT, pressureOverclosure=HARD)
        self.m.interactionProperties['tool-chip-contact'].ThermalConductance(clearanceDependency=OFF, definition=TABULAR, dependenciesP=0, massFlowRateDependencyP=OFF, pressureDepTable=((10000.0, 0.0), (10000.0, 1000.0)), pressureDependency=ON, temperatureDependencyP=OFF)
        self.m.interactionProperties['tool-chip-contact'].HeatGeneration(conversionFraction=0.9, slaveFraction=0.5)
        # Defining the contact interaction in the simulation step
        self.m.ContactExp(createStepName='CuttingStep', name='contact')


    def setContactAndConstraints(self):
        """
        Define constraints interactions between parts.
        """
        # Assigning contact properties and setting up constraints between parts
        self.m.interactions['contact'].includedPairs.setValuesInStep(stepName='CuttingStep', useAllstar=ON)
        self.m.interactions['contact'].contactPropertyAssignments.appendInStep(assignments=((GLOBAL, SELF, 'tool-chip-contact'), (self.m.rootAssembly.instances['ChipPlate-1'].surfaces['ChipPlateSurface'], 'Eulerian-1.inconel718-1', 'chip-plate-contact')), stepName='CuttingStep')      
        self.m.RigidBody(bodyRegion=self.m.rootAssembly.instances['Tool-1'].sets['ToolDomain'], name='ToolConstraint', refPointRegion=self.m.rootAssembly.instances['Tool-1'].sets['ToolRP'])
        self.m.RigidBody(bodyRegion=self.m.rootAssembly.instances['ChipPlate-1'].sets['PlateDomain'], name='ChipPlateConstraint', refPointRegion=self.m.rootAssembly.instances['ChipPlate-1'].sets['PlateRP'])


    def setBoundaryConditionsAndPredefinedFields(self):
        """
        Define boundary conditions interactions between parts.
        """
        # Absolut zero
        self.m.setValues(absoluteZero=1.79769e+308)
        # Setting boundary conditions for the simulation
        self.m.VelocityBC(amplitude=UNSET, createStepName='CuttingStep', distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-WorkpieceBottom', region=self.m.rootAssembly.instances['Eulerian-1'].sets['WorkpieceBottom'], v1=self.CuttingVelocity, v2=0.0, v3=0.0, vr1=0.0, vr2=0.0, vr3=0.0)
        self.m.VelocityBC(amplitude=UNSET, createStepName='CuttingStep', distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-zLock', region=self.m.rootAssembly.instances['Eulerian-1'].sets['EulerDomain'], v1=UNSET, v2=UNSET, v3=0.0, vr1=UNSET, vr2=UNSET, vr3=UNSET)
        self.m.EncastreBC(createStepName='CuttingStep', localCsys=None, name='ToolFix', region=self.m.rootAssembly.instances['Tool-1'].sets['ToolRP'])
        self.m.EncastreBC(createStepName='CuttingStep', localCsys=None, name='ChipPlateFix', region=self.m.rootAssembly.instances['ChipPlate-1'].sets['PlateRP'])
        # Defining the initial velocity and temperature for the simulation
        self.m.Velocity(distributionType=MAGNITUDE, field='', name='cuttingMove', omega=0.0, region=self.m.rootAssembly.instances['Eulerian-1'].sets['WorkpieceDomain'], velocity1=self.CuttingVelocity)
        self.m.Temperature(createStepName='Initial', crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=UNIFORM, magnitudes=(20.0, ), name='InitialTemperature', region=self.m.rootAssembly.sets['AssembleSet'])
        self.m.MaterialAssignment(assignmentList=((self.m.rootAssembly.instances['Eulerian-1'].sets['EulerDomain'], (0, )), (self.m.rootAssembly.instances['Eulerian-1'].sets['WorkpieceDomain'], (1, ))), instanceList=(self.m.rootAssembly.instances['Eulerian-1'], ), name='MaterialAssignment', useFields=False)


    def submitSimulation(self, path_INP, path_CAE, filename):
        """
        Submit the simulation job.
        """
        # Creating and submitting the simulation job
        job = mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
        description='', echoPrint=OFF, explicitPrecision=SINGLE, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model=self.ModelName, modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name=filename, nodalOutputPrecision=SINGLE, 
        numCpus=6, numDomains=6, queue=None, 
        resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=
        0, waitMinutes=0)

        # Writing the INP file        
        os.chdir(path_INP)
        job.writeInput(consistencyChecking=OFF)

