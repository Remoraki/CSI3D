from .decomp import Decompression
from ..utils.colored_graph_nosort import ColoredGraph, Patch, Face
from ..utils.triplet import Triplet, triplet_sort
from ..objc.objc import Objc

import numpy as np

def pipeline(objc, parsing) : 
    D = Decompression()
    graph = objc.graph
    D.graph = graph

    try : 
        err = next(parsing)
    except StopIteration :
        raise StopIteration("EOF")
    
    
    patches = D.from_color_to_patch(verbose=True)
    print("error : ", err)
    

    print("done")
    bary = []
    removed_faces = []
    add_faces = []
    bary_idx = []
    
    print("qtt de patch : " ,len(patches))
    idx_bary_relatif = 1 #me demande pas pk ,mais c'est un 1, avec un 0 ça marche pas... ;(
    for patch in patches :
        print("patch faces : ",patch.faces)
        bi,b,rf,ra = graph.interpolate_patch(patch,idx_bary_relatif)
        bary.append(b)
        removed_faces.append(rf)
        bary_idx.append(bi)
        add_faces.append(ra)
        idx_bary_relatif +=1
        
    # resort the barycenters :   

    _, idx_sort = triplet_sort(bary, list(range(len(bary))))
    sorted_patches = [patches[i] for i in idx_sort]
        
    corrected_bary = []
        
    final_added_faces = []
    for raw_idx, idx in enumerate(idx_sort) :
        print("on ajoute le barycenter : ", idx)
        print("raw_idx : ", raw_idx)
        graph.add_vertice(bary[idx]+err[raw_idx])
        corrected_bary.append(bary[idx]+err[raw_idx])
        
        for trip in add_faces[idx] :
            trip = Triplet(trip.x,trip.y,len(graph.verticies)-1)
            color = patches[idx].color
            final_added_faces.append(trip)
            graph.set_face(trip,color)
        

    
    for sublist in removed_faces :
        for idx in sublist :
            print("remove face : ", idx)
            graph.remove_face(idx)
    
    print("faces : ")
    for f in graph.faces  :
        if f is not None :
            print(f.verticies,"color : ",f.color)
        else : 
            print("None")

    if __name__ == "__main__" :  
        e = input("enter to show\n")

        graph.show()
    
    return corrected_bary, removed_faces, final_added_faces
    
    
if __name__ == "__main__" : 
    objc = Objc()
    parsing = objc.open_objc_from_path("horses/objc/test.objc")
    next(parsing)
    
    while True : 
        pipeline(objc, parsing)