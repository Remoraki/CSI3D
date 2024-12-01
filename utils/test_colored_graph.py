from colored_graph_nosort import ColoredGraph, Face, Patch

graph = ColoredGraph()

# Create 2 faces
graph.add_vertice((0,0,0))
graph.add_vertice((1,0,0))
graph.add_vertice((1,1,0))
graph.add_vertice((0,1,0))
graph.add_vertice((0,0,1))

graph.set_face((0,1,2))
graph.set_face((1,2,3))
graph.set_face((0,1,4))

graph.remove_vertice(3)

graph.show()

