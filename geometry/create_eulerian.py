# -*- coding: utf-8 -*-
from abaqus import *
from abaqusConstants import *
from part import *
from step import *
from material import *
from section import *
from assembly import *
from interaction import *
from mesh import *
from visualization import *
from connectorBehavior import *


class EulerianModel():
    """
    Class to define and build an Eulerian model in Abaqus, including geometry, partitions, sets, sections, and mesh.
    """
    def __init__(self, data):
        """
        Initialize the EulerianModel class and execute the workflow.

        :param data: Dictionary containing input data for model creation. If no data is provided, default data is loaded.
        """

        # import json
        # data = r"S:\Junior\abaqus-with-python\otimization-scripts\backup\results\inp-and-simulation\info\sim_v166_h75_gam-6.json"
        # with open(data, "r") as info:
        #     data = json.load(info)

        self.dataInput(data)
        self.createPart()
        self.createPartition()
        self.createSetsandSections()
        self.createMesh()


    def dataInput(self, data):
        """
        Extract input data and define model variables.

        :param data: Dictionary containing model parameters.
        """


        # Calling Model
        self.ModelName = str(data['generalInformation']['modelName'])
        self.m = mdb.models[self.ModelName]
        # Defining Variables
        self.KssDomain = "KssDomain"
        self.ElementType = "EC3D8RT"
        self.ElementLibrary = "EXPLICIT"
        self.EulerDomain = "EulerDomain"
        self.SectionName = "EulerSection"
        self.WorkpieceDomain = "WorkpieceDomain"
        self.WorkpieceBottom = "WorkpieceBottom"
        self.PartName = str(data['eulerianData']['createPartInformation']['Name'])
        self.MaxWidth = data['eulerianData']['createPartInformation']['MaxWidth']
        self.MinWidth = data['eulerianData']['createPartInformation']['MinWidth']
        self.MaxHeight = data['eulerianData']['createPartInformation']['MaxHeight']
        self.MinHeight = data['eulerianData']['createParticionInformation']['y_points'][3] 
        self.Trickness = data['eulerianData']['createPartInformation']['Trickness']
        self.Material = str(data['eulerianData']['createPartInformation']['Material'])
        self.x_partition_points = data['eulerianData']['createParticionInformation']['x_points']
        self.y_partition_points = data['eulerianData']['createParticionInformation']['y_points']
        self.y_partition_points_tool = data['eulerianData']['createParticionInformation']['y_points'][2] 
        self.GlobalSize = data['eulerianData']['createMeshInformation']['globalSize']
        self.DeviationFactor = data['eulerianData']['createMeshInformation']['deviationFactor']
        self.MinSizeFactor = data['eulerianData']['createMeshInformation']['minSizeFactor']
        self.CuttingDepth = -data['assemblyAndSimulationData']['toolPosition']['cuttingDepth']


    def createPart(self):
        """
        Create the part geometry for the Eulerian model.
        """
        # Creating Sketch
        s = mdb.models[self.ModelName].ConstrainedSketch(name='__profile__', sheetSize=200.0)
        s.Line(point1=(0.0, 0.0), point2=(33.75, 0.0))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[2])
        s.Line(point1=(33.75, 2.5), point2=(33.75, 10.0))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[3])
        s.Line(point1=(30.0, 11.25), point2=(20.0, 11.25))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[4])
        s.Line(point1=(17.5, 13.75), point2=(17.5, 23.75))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[5])
        s.Line(point1=(13.75, 23.75), point2=(0.0, 23.75))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[6])
        s.Line(point1=(0.0, 21.25), point2=(0.0, 5.0))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[7])
        s.CoincidentConstraint(entity1=s.vertices[11], entity2=s.vertices[0])
        s.CoincidentConstraint(entity1=s.vertices[9], entity2=s.vertices[10])
        s.CoincidentConstraint(entity1=s.vertices[2], entity2=s.vertices[1])
        s.CoincidentConstraint(entity1=s.vertices[4], entity2=s.vertices[3])
        s.CoincidentConstraint(entity1=s.vertices[7], entity2=s.vertices[8])
        s.CoincidentConstraint(entity1=s.vertices[6], entity2=s.vertices[5])
        s.HorizontalDimension(textPoint=(16.3909759521484, -5.15337371826172), value=self.MaxWidth, vertex1=s.vertices[0], vertex2=s.vertices[1])
        s.VerticalDimension(textPoint=(-3.11485934257507, 5.61979579925537), value=self.MaxHeight, vertex1=s.vertices[9], vertex2=s.vertices[0])
        s.HorizontalDimension(textPoint=(3.8, 3.125), value=self.MinWidth, vertex1=s.vertices[9], vertex2=s.vertices[7])
        s.VerticalDimension(textPoint=(5.7988452911377, 0.750127792358398), value=self.MinHeight, vertex1=s.vertices[3], vertex2=s.vertices[1])
        # # Creating Body
        self.p = mdb.models[self.ModelName].Part(dimensionality=THREE_D, name=self.PartName, type=EULERIAN)
        self.p.BaseSolidExtrude(depth=self.Trickness, sketch=s)
        

    def createPartition(self):
        """
        Create the part geometry for the Eulerian model.
        """
        # Creating Sketch Tool Particion
        s = mdb.models[self.ModelName].ConstrainedSketch(gridSpacing=0.22, name='__profile__', sheetSize=8.83, transform=self.p.MakeSketchTransform(sketchPlane=self.p.faces[6], sketchPlaneSide=SIDE1, sketchUpEdge=self.p.edges[4], sketchOrientation=RIGHT, origin=(1.41412, 1.016452, 0.02)))
        self.p.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=s)
        # Draw the first vertical line and add constraints
        s.Line(point1=(0.935, -0.605), point2=(0.935, -0.824999999976717))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[8])
        s.CoincidentConstraint(entity1=s.vertices[6], entity2=s.vertices[2])
        s.CoincidentConstraint(entity1=s.vertices[7], entity2=s.geometry[6])
        # Draw the second vertical line and add constraints
        s.Line(point1=(-0.44, 0.165), point2=(-0.44, -0.495000000055879))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[9])
        s.CoincidentConstraint(entity1=s.vertices[8], entity2=s.geometry[2])
        s.CoincidentConstraint(entity1=s.vertices[9], entity2=s.geometry[6])
        # Draw the third vertical line and add constraints
        s.Line(point1=(-0.165, 0.44), point2=(-0.165, 0.0))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[10])
        s.CoincidentConstraint(entity1=s.vertices[10], entity2=s.geometry[2])
        s.CoincidentConstraint(entity1=s.vertices[11], entity2=s.geometry[6])
        # Draw the fourth vertical line and add constraints
        s.Line(point1=(0.275, 0.275), point2=(0.275, 0.0549999999674037))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[11])
        s.CoincidentConstraint(entity1=s.vertices[12], entity2=s.geometry[2])
        s.CoincidentConstraint(entity1=s.vertices[13], entity2=s.geometry[6])
        # Draw the first horizontal line and add constraints
        s.Line(point1=(-0.66, -0.33), point2=(-0.11, -0.33))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[12])
        s.CoincidentConstraint(entity1=s.vertices[6], entity2=s.vertices[15])
        s.CoincidentConstraint(entity1=s.vertices[14], entity2=s.geometry[7])
        # Draw the second horizontal line and add constraints
        s.Line(point1=(-0.99, -0.66), point2=(0.11, -0.66))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[13])
        s.CoincidentConstraint(entity1=s.vertices[16], entity2=s.geometry[7])
        s.CoincidentConstraint(entity1=s.geometry[13], entity2=s.vertices[17])
        s.CoincidentConstraint(entity1=s.geometry[5], entity2=s.vertices[17])
        # Draw the third horizontal line and add constraints
        s.Line(point1=(-0.55, -0.825), point2=(-0.222122233593836, -0.825))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[14])
        s.CoincidentConstraint(entity1=s.geometry[7], entity2=s.vertices[18])
        s.CoincidentConstraint(entity1=s.vertices[19], entity2=s.geometry[5])
        # Draw the fourth horizontal line and add constraints
        s.Line(point1=(-0.495, -0.605), point2=(-0.274999999953434, -0.605))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[15])
        s.CoincidentConstraint(entity1=s.geometry[7], entity2=s.vertices[20])
        s.CoincidentConstraint(entity1=s.vertices[21], entity2=s.geometry[5])
        # Draw the fifth horizontal line and add constraints
        s.Line(point1=(-0.77, 0.11), point2=(0.165000000037253, 0.11))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[16])
        s.CoincidentConstraint(entity1=s.vertices[22], entity2=s.geometry[7])
        s.CoincidentConstraint(entity1=s.geometry[3], entity2=s.vertices[23])
        # Draw the sixth horizontal line and add constraints
        s.Line(point1=(-1.045, -0.11), point2=(0.0, -0.11))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[17])
        s.CoincidentConstraint(entity1=s.vertices[24], entity2=s.geometry[7])
        s.CoincidentConstraint(entity1=s.vertices[25], entity2=s.geometry[3])
        # Defining the horizontal partition positions
        s.DistanceDimension(entity1=s.geometry[14], entity2=s.geometry[6], textPoint=(-1.68507532417297, -0.90773503527832), value=self.y_partition_points[0])
        s.DistanceDimension(entity1=s.geometry[13], entity2=s.geometry[6], textPoint=(-1.90749935447693, -0.912672207214355), value=self.y_partition_points[1])
        s.DistanceDimension(entity1=s.geometry[15], entity2=s.geometry[6], textPoint=(-2.13980893432617, -0.922546789505005), value=self.y_partition_points_tool)
        s.DistanceDimension(entity1=s.geometry[17], entity2=s.geometry[6], textPoint=(-2.41166071235657, -1.01141731486511), value=self.y_partition_points[4])
        s.DistanceDimension(entity1=s.geometry[16], entity2=s.geometry[6], textPoint=(-2.64878467857361, -0.829298302986145), value=self.y_partition_points[5])
        # Defining the vertical partition positions
        s.DistanceDimension(entity1=s.geometry[7], entity2=s.geometry[9], textPoint=(-0.843816559906006, 1.32369954838562), value=self.x_partition_points[0])
        s.DistanceDimension(entity1=s.geometry[7], entity2=s.geometry[10], textPoint=(-0.478982728118897, 1.47714264645386), value=self.x_partition_points[1])
        s.DistanceDimension(entity1=s.geometry[11], entity2=s.geometry[7], textPoint=(-1.00703195869446, 1.64976604237366), value=self.x_partition_points[2])
        # Creating Partition Cells
        self.p.PartitionFaceBySketch(faces=self.p.faces.getSequenceFromMask(('[#40 ]', ), ), sketch=s, sketchUpEdge=self.p.edges[4])
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[3], self.p.edges[4], self.p.edges[13], self.p.edges[16], self.p.edges[31], self.p.edges[34], self.p.edges[50]), line=self.p.edges[85], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#2 ]', ), ), edges=(self.p.edges[30], self.p.edges[37], self.p.edges[44], self.p.edges[49], self.p.edges[60], self.p.edges[63], self.p.edges[74]), line=self.p.edges[90], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#4 ]', ), ), edges=(self.p.edges[51], self.p.edges[60], self.p.edges[66], self.p.edges[70], self.p.edges[79], self.p.edges[80], self.p.edges[88]), line=self.p.edges[95], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[60], self.p.edges[72], self.p.edges[83], self.p.edges[92]), line=self.p.edges[16], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#8 ]', ), ), edges=(self.p.edges[61], ), line=self.p.edges[103], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#10 ]', ), ), edges=(self.p.edges[76], ), line=self.p.edges[5], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#20 ]', ), ), edges=(self.p.edges[88], ), line=self.p.edges[15], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#40 ]', ), ), edges=(self.p.edges[93], ), line=self.p.edges[22], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[93], ), line=self.p.edges[13], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#2 ]', ), ), edges=(self.p.edges[94], ), line=self.p.edges[12], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#100 ]', ), ), edges=(self.p.edges[103], ), line=self.p.edges[11], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#200 ]', ), ), edges=(self.p.edges[111], ), line=self.p.edges[18], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#400 ]', ), ), edges=(self.p.edges[121], ), line=self.p.edges[24], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#800 ]', ), ), edges=(self.p.edges[125], ), line=self.p.edges[31], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[123], ), line=self.p.edges[42], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[123], ), line=self.p.edges[48], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#10000 ]', ), ), edges=(self.p.edges[130], ), line=self.p.edges[54], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#20000 ]', ), ), edges=(self.p.edges[138], ), line=self.p.edges[66], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#40000 ]', ), ), edges=(self.p.edges[148], ), line=self.p.edges[70], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#80000 ]', ), ), edges=(self.p.edges[151], ), line=self.p.edges[74], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#100000 ]', ), ), edges=(self.p.edges[149], ), line=self.p.edges[78], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#200000 ]', ), ), edges=(self.p.edges[149], ), line=self.p.edges[82], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#80000 ]', ), ), edges=(self.p.edges[156], ), line=self.p.edges[86], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#100000 ]', ), ), edges=(self.p.edges[164], ), line=self.p.edges[94], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#200000 ]', ), ), edges=(self.p.edges[172], ), line=self.p.edges[99], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#400000 ]', ), ), edges=(self.p.edges[173], ), line=self.p.edges[104], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#800000 ]', ), ), edges=(self.p.edges[174], ), line=self.p.edges[112], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1000000 ]', ), ), edges=(self.p.edges[175], ), line=self.p.edges[116], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1000000 ]', ), ), edges=(self.p.edges[179], ), line=self.p.edges[154], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#2000000 ]', ), ), edges=(self.p.edges[183], ), line=self.p.edges[161], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#4000000 ]', ), ), edges=(self.p.edges[187], ), line=self.p.edges[166], sense=REVERSE)


    def createSetsandSections(self):
        """
        Define sets and sections for the Eulerian model.
        """
        # Creating WorkpieceBottom Set 
        self.p.Set(faces=self.p.faces.getSequenceFromMask(('[#0:2 #11000000 #5 #100 ]', ), ), name=self.WorkpieceBottom)
        # Creating EulerDomain Set 
        self.p.Set(cells=self.p.cells.getSequenceFromMask(('[#ffffffff ]', ), ), name=self.EulerDomain)
        # Creating WorkpieceDomain Set 
        self.p.Set(cells=self.p.cells.getSequenceFromMask(('[#e0fc0e00 ]', ), ), name=self.WorkpieceDomain)
        # Creating Chip Set
        self.p.Set(cells=self.p.cells.getSequenceFromMask(('[#30c0 ]', ), ), name='ChipSet')
        # # Creating Sections
        self.m.EulerianSection(data={'inconel718-1': self.Material}, name=self.SectionName)
        self.p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=self.p.sets[self.EulerDomain], sectionName=self.SectionName, thicknessAssignment=FROM_SECTION)


    def createMesh(self):
        """
        Generate the mesh for the Eulerian model.
        """
        # Set the element types for the part
        self.p.setElementType(elemTypes=(ElemType(elemCode=EC3D8RT, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT), ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT), ElemType(elemCode=UNKNOWN_TET, elemLibrary=EXPLICIT)), regions=(self.p.cells.getSequenceFromMask(('[#ffffffff ]', ), ), ))
        # Seed the part with a global element size
        self.p.seedPart(deviationFactor=self.DeviationFactor, minSizeFactor=self.MinSizeFactor, size=self.GlobalSize)
        # Seed horizontal edges 1
        self.p.seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=self.p.edges.getSequenceFromMask(('[#0:4 #4808082 #10000002 #4 ]', ), ), end2Edges=self.p.edges.getSequenceFromMask(('[#0:4 #40241008 #20000050 ]', ), ), maxSize=0.03, minSize=0.015)
        # Seed horizontal edges 2
        self.p.seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=self.p.edges.getSequenceFromMask(('[#0:2 #80000000 #1081404 #0 #2080000 ]', ), ), end2Edges=self.p.edges.getSequenceFromMask(('[#0:3 #308400c2 #0 #200000 ]', ), ), maxSize=0.01, minSize=0.005)
        # Seed horizontal edges 3 and 4
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#42800000 #61414a53 #14a194d1 #0:2 #8838000 ]', ), ), minSizeFactor=0.1, size=0.005)
        # Seed horizontal edges 5
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#428505 #0:4 #1400 #1 ]', ), ), minSizeFactor=0.1, size=0.01)
        # Seed vertical edges 1
        self.p.seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=self.p.edges.getSequenceFromMask(('[#0 #2000000 #0:3 #40000000 ]', ), ), end2Edges=self.p.edges.getSequenceFromMask(('[#0 #18000000 #0 #14000 #0 #1402000 #10 ]', ), ), maxSize=0.03, minSize=0.015)
        # Seed vertical edges 2, 3, 4 and 5
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#346800 #342180 #631c6000 #302318 #9a584000 #403a5 #2 ]', ), ), minSizeFactor=0.1, size=0.005)
        # Seed vertical edges 6
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#200000d0 #8 #208 #6000000 #12040 ]', ), ), minSizeFactor=0.1, size=0.01)
        # Seed vertical edges 7
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#14000000 #4 #104 #40000000 #521 #84000000 ]', ), ), minSizeFactor=0.1, size=0.02)
        # Generate the mesh for the part
        self.p.generateMesh()

# EulerianModel()