import Sofa
import os
path = os.path.dirname(os.path.abspath(__file__))+'/design/'

def createScene(rootNode):
	rootNode.createObject('RequiredPlugin', pluginName='SoftRobots SofaOpenglVisual SofaSparseSolver SofaPreconditioner SofaMiscCollision')
	rootNode.createObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels hideCollisionModels hideBoundingCollisionModels showForceFields hideInteractionForceFields hideWireframe')
	rootNode.createObject('RequiredPlugin', name='SoftRobots')
	rootNode.createObject('RequiredPlugin', name='SofaPython')
	rootNode.createObject('RequiredPlugin', name='SofaSparseSolver')
	rootNode.findData('gravity').value=[ 0, 0, -9810]
	rootNode.findData('dt').value = 0.001
	rootNode.createObject('FreeMotionAnimationLoop')
	rootNode.createObject('GenericConstraintSolver', tolerance=1e-12, maxIterations=10000)
	rootNode.createObject('DefaultPipeline')
	rootNode.createObject('BruteForceDetection')
	rootNode.createObject('DefaultContactManager', response='FrictionContact', responseParams='mu=0.6')
	rootNode.createObject('LocalMinDistance', name='Proximity', alarmDistance=5, contactDistance=1, angleCone=0.0)
	rootNode.createObject('BackgroundSetting', color=[0, 0.168627, 0.211765])
	rootNode.createObject('OglSceneFrame', style='Arrows', alignment='TopRight')
	rootNode.createObject('PythonScriptController', filename='pythonControllers/fingerController.py', classname='controller')

	finger = rootNode.createChild('finger')
	finger.createObject('EulerImplicitSolver', name='odesolver', rayleighStiffness=0.1, rayleighMass=0.1)
	finger.createObject('SparseLDLSolver', name='directSolver')
	finger.createObject('MeshVTKLoader', name='loader', filename='design/finger0.vtu')
	finger.createObject('MechanicalObject', name='tetras', template='Vec3d', src = '@loader')
	finger.createObject('TetrahedronSetTopologyContainer', name="topo", src ='@loader')
	finger.createObject('TetrahedronSetTopologyModifier' ,  name="Modifier")
	finger.createObject('TetrahedronSetTopologyAlgorithms', name="TopoAlgo", template="Vec3d")
	finger.createObject('TetrahedronSetGeometryAlgorithms', template="Vec3d" ,name="GeomAlgo", drawTriangles="1")
	



	finger.createObject('MeshMatrixMass', massDensity='1020e-9', src = '@topo')

	youngModulus = 120
	poisson = 0.44
	mu = 2*1515.4118
	k0 = youngModulus/(3*(1-2*poisson))

	finger.createObject('TetrahedronHyperelasticityFEMForceField', template='Vec3d', name='FEM', src ='@topo', ParameterSet=str(mu)+' '+str(k0),materialName="NeoHookean")
	finger.createObject('BoxROI', name='boxROI', box=[-10, 0, 0, 10,15, 5], drawBoxes=True)
	finger.createObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness=1e12, angularStiffness=1e12)
	finger.createObject('LinearSolverConstraintCorrection', solverName='directSolver')

	cavity = finger.createChild('cavity')
	cavity.createObject('MeshObjLoader', name='cavityLoader', filename='design/BSPA_New_Design_Inner.obj')
	cavity.createObject('MeshTopology', src='@cavityLoader', name='cavityMesh')
	cavity.createObject('MechanicalObject', name='cavity')
	cavity.createObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3d', value= 0, triangles='@cavityMesh.triangles', valueType='pressure')
	cavity.createObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)


	collisionFinger = finger.createChild('collisionFinger')
	collisionFinger.createObject('MeshObjLoader', name='loader', filename='design/BSPA_New_Design_Outer.obj')
	collisionFinger.createObject('MeshTopology', src='@loader', name='topo')
	collisionFinger.createObject('MechanicalObject', name='collisMech')
	collisionFinger.createObject('TriangleCollisionModel', selfCollision=False)
	collisionFinger.createObject('LineCollisionModel', selfCollision=False)
	collisionFinger.createObject('PointCollisionModel', selfCollision=False)
	collisionFinger.createObject('BarycentricMapping')

	modelVisu = finger.createChild('visu')
	modelVisu.createObject('MeshObjLoader', name='loader', filename='design/BSPA_New_Design_Outer.obj')
	modelVisu.createObject('OglModel', src='@loader', color='yellow')
	modelVisu.createObject('BarycentricMapping')




	return rootNode