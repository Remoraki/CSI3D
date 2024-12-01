from .colored_graph_nosort import ColoredGraph, Face, Patch
from ..obja.obja import Model, parse_file
import sys
from tqdm import tqdm

def main () : 
    if len(sys.argv) == 1:
        print("obja needs a path to an obj file")
        return

    model = parse_file(sys.argv[1])
    cg = ColoredGraph()
    
    for v in model.vertices :
        
        cg.add_vertice(v)
        
    i = 0
    # yellow and blue
    colors = [1,0,2,3]
    for f in model.faces :
        i+=1
        a,b,c = f.a, f.b, f.c
        cg.set_face((a,b,c),colors[i%len(colors)])
        
        
    cg.show()
    
def load (file_name) :
    model = parse_file(file_name)
    cg = ColoredGraph()
    
    for v in model.vertices :
        
        cg.add_vertice(v)
        
    i = 0
    colors = [1,0,2,3]
    print("loading faces")
    for f in tqdm(model.faces) :
        i+=1
        a,b,c = f.a, f.b, f.c
        cg.set_face((a,b,c))
    
    return cg

def save_obj(graph) :
    vertices = graph.verticies
    faces = graph.faces
    
    with open("output.obj","w") as f :
        for v in vertices :
            f.write(f"v {v.x} {v.y} {v.z}\n")
        
        for face in faces :
            if face is not None :
                f.write(f"f {face.verticies[0]+1} {face.verticies[1]+1} {face.verticies[2]+1}\n")
        
    print("saved")
    
        
if __name__ == "__main__" :
    main()
    