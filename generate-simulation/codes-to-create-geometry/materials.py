# -*- coding: utf-8 -*-
import os
import json
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
import inspect 

class Materials():
    def __init__(self, data):
        self.ModelName = str(data['generalInformation']['modelName'])
        self.materialsPart()

    def materialsPart(self):
        table_specific_heat = ((4406000.0, 20.0), (459700.0, 100.0), (486700.0, 300.0), (520900.0, 500.0), (559900.0, 600.0), (610900.0, 700.0), (662000.0, 800.0), (651000.0, 900.0), (673000.0, 1000.0), (710100.0, 1200.0), (710100.0, 1500.0))
        table_elastic = (202565, 0.29, 21.11), (201168, 0.29, 37.78), (198374, 0.29, 93.33), (195580, 0.28, 148.89), (192786, 0.28, 204.44), (189294, 0.28, 260), (186500, 0.27, 315.56), (183007, 0.27, 371.11), (180213, 0.27, 426.67), (176721, 0.27, 482.22), (173228, 0.27, 537.78), (169037, 0.28, 593.33), (165545, 0.28, 648.89), (160655, 0.29, 704.44), (155766, 0.31, 760), (148781, 0.32, 815.56), (141097, 0.33, 871.11), (131318, 0.33, 926.67), (121539, 0.34, 982.22), (111062, 0.37, 1037.78), (99885.5, 0.4, 1093.33)
        table_conductive = (11.39, 21.11), (12.55, 93.33), (14.42, 204.44), (16.15, 315.56), (17.88, 426.67), (19.62, 537.78), (21.35, 648.89), (23.22, 760), (24.95, 871.11), (26.83, 982.22), (28.7, 1093.33)
        table_damage_evolution = (0, 0), (0.042900728, 0.0003298), (0.083303112, 0.0006596), (0.121352644, 0.0009894), (0.157186345, 0.0013192), (0.190933252, 0.001649), (0.222714893, 0.0019788), (0.252645716, 0.0023086), (0.280833503, 0.0026384), (0.30737976, 0.0029682), (0.332380085, 0.003298), (0.355924503, 0.0036278), (0.378097802, 0.0039576), (0.398979828, 0.0042874), (0.41864578, 0.0046172), (0.437166475, 0.004947), (0.45460861, 0.0052768), (0.471034993, 0.0056066), (0.486504779, 0.0059364), (0.501073674, 0.0062662), (0.514794143, 0.006596), (0.527715594, 0.0069258), (0.539884558, 0.0072556), (0.551344857, 0.0075854), (0.56213776, 0.0079152), (0.572302133, 0.008245), (0.58187458, 0.0085748), (0.59088957, 0.0089046), (0.599379568, 0.0092344), (0.607375148, 0.0095642), (0.614905101, 0.009894), (0.621996543, 0.0102238), (0.628675012, 0.0105536), (0.634964558, 0.0108834), (0.640887829, 0.0112132), (0.646466155, 0.011543), (0.651719625, 0.0118728), (0.656667156, 0.0122026), (0.661326566, 0.0125324), (0.665714633, 0.0128622), (0.669847159, 0.013192), (0.673739025, 0.0135218), (0.677404247, 0.0138516), (0.680856023, 0.0141814), (0.684106782, 0.0145112), (0.687168233, 0.014841), (0.690051398, 0.0151708), (0.692766661, 0.0155006), (0.6953238, 0.0158304), (0.697732022, 0.0161602), (0.7, 0.01649)
        
        m = mdb.models[self.ModelName]
        m.Material(name='Inconel718')

        m.materials['Inconel718'].SpecificHeat(dependencies=0, law=CONSTANTVOLUME, table=table_specific_heat, temperatureDependency=ON)
        m.materials['Inconel718'].setValues(materialIdentifier='')
        m.materials['Inconel718'].setValues(description='Damage model and specific heat from DA718 [PENG20]\nProperties from literature - Mass Scaling 1000')
        m.materials['Inconel718'].Elastic(dependencies=0, moduli=LONG_TERM, noCompression=OFF, noTension=OFF, table=table_elastic, temperatureDependency=ON, type=ISOTROPIC)
        m.materials['Inconel718'].Density(dependencies=0, distributionType=UNIFORM, fieldName='', table=((8.22e-06, ), ), temperatureDependency=OFF)
        m.materials['Inconel718'].InelasticHeatFraction(fraction=0.9)
        m.materials['Inconel718'].Conductivity(dependencies=0, table=table_conductive, temperatureDependency=ON, type=ISOTROPIC)
        m.materials['Inconel718'].JohnsonCookDamageInitiation(alpha=0.0, definition=MSFLD, dependencies=0, direction=NMORI, feq=10.0, fnn=10.0, fnt=10.0, frequency=1, ks=0.0, numberImperfections=4, omega=1.0, position=CENTROID, table=((0.04, 0.75, -1.45, 0.04, 0.89, 1260, 25, 0.0001), ), temperatureDependency=OFF, tolerance=0.05)
        m.materials['Inconel718'].johnsonCookDamageInitiation.DamageEvolution(degradation=MAXIMUM, dependencies=0, mixedModeBehavior=MODE_INDEPENDENT, modeMixRatio=ENERGY, power=None, softening=TABULAR, table=table_damage_evolution, temperatureDependency=OFF, type=DISPLACEMENT)
        m.materials['Inconel718'].Plastic(dataType=HALF_CYCLE, dependencies=0, hardening=JOHNSON_COOK, numBackstresses=1, rate=OFF, strainRangeDependency=OFF, table=((1200.0, 800.0, 0.4, 1.55, 1260.0, 25.0), ), temperatureDependency=OFF)
        m.materials['Inconel718'].plastic.RateDependent(dependencies=0, table=((0.0135, 0.001), ), temperatureDependency=OFF, type=JOHNSON_COOK)
        # m.materials['Inconel718'].Plastic(dataType=HALF_CYCLE, dependencies=0, hardening=USER, numBackstresses=1, rate=OFF, strainRangeDependency=OFF, table=((1.0, ), ), temperatureDependency=OFF)
        # m.materials['Inconel718'].Depvar(n=5)
        
        m.Material(name='EMT210 - Extramet')
        m.materials['EMT210 - Extramet'].Elastic(dependencies=0, moduli=LONG_TERM, noCompression=OFF, noTension=OFF, table=((580000.0, 0.22), ), temperatureDependency=OFF, type=ISOTROPIC)
        m.materials['EMT210 - Extramet'].Density(dependencies=0, distributionType=UNIFORM, fieldName='', table=((1.445e-05, ), ), temperatureDependency=OFF)
        m.materials['EMT210 - Extramet'].setValues(description='[SPRI02] Mass Scaling 1000\n89.0 % Wolframcarbid\n')
        m.materials['EMT210 - Extramet'].SpecificHeat(dependencies=0, law=CONSTANTVOLUME, table=((222000.0, 87.0), (243000.0, 177.0), (259000.0, 277.0), (268000.0, 377.0), (293000.0, 477.0), (301000.0, 577.0), (314000.0, 687.0)), temperatureDependency=ON)
        m.materials['EMT210 - Extramet'].setValues(materialIdentifier='')
        m.materials['EMT210 - Extramet'].Conductivity(dependencies=0, table=((85.0, 20.0), (70.4, 500.0), (68.6, 550.0), (68.4, 600.0), (66.8, 650.0), (64.7, 700.0)), temperatureDependency=ON, type=ISOTROPIC)

# model = Materials()