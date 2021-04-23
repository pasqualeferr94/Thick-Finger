
import SofaRuntime
SofaRuntime.importPlugin("SofaComponentAll")

# to add elements like Node or objects
import Sofa.Core
import os
path = os.path.dirname(os.path.abspath(__file__))+'/design/'

def createScene(rootNode):
	rootNode.addObject('RequiredPlugin' ,pluginName='SofaExporter')
	rootNode.addObject('VisualStyle',displayFlags="hideVisual")
	rootNode.addObject('RequiredPlugin', pluginName="CGALPlugin")
	rootNode.addObject('RequiredPlugin', name="SofaOpenglVisual")
	rootNode.addObject('MeshObjLoader', name="loader", filename="design/BSPA_New_Design_Outer.obj")

	rootNode.addObject('MechanicalObject', name="dofs", position="@loader.position")
	#rootNode.addObject('TriangleSetTopologyContainer', name="topo", triangles="@loader.triangles")
	#rootNode.addObject('TriangleSetTopologyModifier' ,  name="Modifier")
	#rootNode.addObject('TriangleSetTopologyAlgorithms', name="TopoAlgo", template="Vec3d")
	#rootNode.addObject('TriangleSetGeometryAlgorithms', template="Vec3d" ,name="GeomAlgo", drawTriangles="1")

	rootNode.addObject('MeshGenerationFromPolyhedron', name="gen", inputPoints="@loader.position", inputTriangles="@loader.triangles",facetSize="0.75",facetApproximation="1",cellRatio="2", cellSize="2")
	rootNode.addObject('Mesh', name ='topo', position='@gen.outputPoints', tetrahedra='@gen.outputTetras')
	rootNode.addObject('VTKExporter', filename='finger',src = '@topo', edges='0', exportAtBegin='1')
	rootNode.addObject('OglModel', color=[0.3, 0.2, 0.2, 0.6])
	return rootNode