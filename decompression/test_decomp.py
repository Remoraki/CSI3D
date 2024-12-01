from .decomp import Decompression
from ..utils.colored_graph_nosort import ColoredGraph, Patch, Face
from ..utils.triplet import Triplet
from ..utils.cg_from_obj import load
from tqdm import tqdm

file_name = "horses/obja/example/suzanne.obj"
graph = load(file_name)
D = Decompression()
D.graph = graph

patches = D.from_color_to_patch(verbose=True)

print("done")
for patch in tqdm(patches) :
    print(patch.faces)
    graph.interpolate_patch(patch)

e = input("enter to continue\n")

graph.show()