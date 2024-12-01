from ..objc.objc import Objc
from ..utils.colored_graph_nosort import ColoredGraph, Patch, Face
import numpy as np
from tqdm import tqdm

class Decompression () :
    def __init__ (self) :
        self.graph = ColoredGraph()
        self.objc = Objc()
        self.objc.graph = self.graph
    
    def open_objc (self, path) :
        self.objc.open_objc_from_path(path)
        
    
    def  voisins(self, f) :
        face = self.graph.faces[f]
        vertices = [face.verticies[i] for i in range(3)]
        voisinx = []
        
        voisin_trouve = 0
        for idx, face_explored in self.graph.enumerate_over_faces() : 
            vertice_commun = 0
            for vertice in face_explored.verticies :
                if vertice in vertices :
                    vertice_commun += 1
                    
            if vertice_commun == 2 :
                voisinx.append(idx)
                voisin_trouve +=1
                
            if voisin_trouve ==3 :
                break
            
        return voisinx
                
            
    def _patch_propagation(self, face) : 
        pile_propagation = [face]
        patch = []
        done = [face]
        
        
        while len(pile_propagation) > 0 :

            f = pile_propagation.pop()
            face = self.graph.faces[f]
            
            patch.append(f)
            
            color = face.color
            
            voisins = self.voisins(f)
            for v in voisins : 
                if v not in done and self.graph.faces[v].color == color :
                    pile_propagation.append(v)
                    done.append(v)

                    
        return patch
    
    def from_color_to_patch (self, verbose = False) :
        # 4 coloration
        done = []
        patches = []
        if verbose :
            print("patching")

        for idx, face in self.graph.enumerate_over_faces() :
            if idx in done : 
                continue
            
            
            patch = Patch()
            patch.color = face.color
            lst_prop = self._patch_propagation(idx)
            done += lst_prop
            patch.faces = lst_prop
            patches.append(patch)
            
        return patches
    
    
    
            