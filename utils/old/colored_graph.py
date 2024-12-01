import numpy as np
import matplotlib.pyplot as plt
from triplet import Triplet
from historlist import Historlist


class ColoredGraph () :
    """
    Colored graph for implementing the paper, using bicolor compression
    """
    def __init__ (self) :
        self.verticies = Historlist() # list of verticies : 3D points triés par x,y,z croissants
        self.edges = Historlist() # list of edges : couple of index verticies
        
        self.faces = Historlist() # list of faces : list of index verticies, MUST BE TRIANGLE
        self.adjacency = None # elle sera sparse
        self.face_adjacency = None # elle sera sparse

    
    def make_adjacency (self) :
        self.adjacency = np.zeros((len(self.verticies),len(self.verticies)))
        for edge in self.edges :
            self.adjacency[edge[0],edge[1]] = 1
            self.adjacency[edge[1],edge[0]] = 1
    
    def make_face_adjacency (self) :
        # the make adjacency must be called before
        self.face_adjacency = np.zeros((len(self.faces),len(self.faces)))
        
    def __repr__ (self) :
        """
        return a string representation of the graph
        """
        
        overview = "Colored Graph with : \n"
        overview += f"{len(self.verticies)} verticies \n"
        overview += f"{len(self.edges)} edges \n"
        overview += f"{len(self.faces)} faces \n"
        overview += "-"*20 + "\n"
        
        details = ""
        for f in self.faces : 
            details += f"face {f.id} : {f.verticies} \n"
            
        return overview + details
        
                
    def show (self) : 
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        for vertex in self.verticies :
            ax.scatter(vertex[0],vertex[1],vertex[2])
        
        for face in self.faces :
            v1 = self.verticies[face.verticies[0]]
            v2 = self.verticies[face.verticies[1]]
            v3 = self.verticies[face.verticies[2]]
            ax.plot([v1[0],v2[0]],[v1[1],v2[1]],[v1[2],v2[2]])
            ax.plot([v2[0],v3[0]],[v2[1],v3[1]],[v2[2],v3[2]])
            ax.plot([v3[0],v1[0]],[v3[1],v1[1]],[v3[2],v1[2]])
            
        plt.show()            
    
    def color2patch_bicolor (self) :   
        
        """
        on pars de la liste des faces colorées, et on dois en déduire les patches associés
        un patch est définis de la manière suivante : 
            + un ensemble de face colorées soit en 1 soit en 0 (true ou false), on dira jaune ou bleu 
            + il y a nécéssairement 2 face jaunes par patch, et autant de bleu que nécéssaire
            + les faces bleu sont telles que elles ont 2 côté adjacent à des faces du patch
            + les faces jaunes sont telles que elles ont 1 côté adjacent à une face du patch
        """
        pass
  
    def remove_vertice (self, index) :
        pass
    

    
    # trie par x,y,z croissants
    def add_vertice (self, vertex) :
        """
        in : vertex : tuple de 3 float
        """
        x,y,z = vertex
        triplet_xyz = Triplet(x,y,z)
        vertex_idx = 0        
        
        if self.verticies == [] :
            self.verticies.append(vertex)
            return
        
        while vertex_idx < len(self.verticies) and triplet_xyz < self.verticies[vertex_idx] :
            vertex_idx +=1 
        
        self.verticies.insert(vertex_idx,triplet_xyz)
        
    def set_face (self, indexes) :
        # condition pour color2patch_bicolor : les faces bleu (intérieurs) doivent former un Z
        """
        indexes : tuple de 3 points (3 indexes)
        les faces sont triées par indices croissants (honhon baguette)
        """
        if len(indexes) != 3 :
            raise IndexError("les faces sont nécéssairement des triangles")
        
        if any([index < 0 or index >= len(self.verticies) for index in indexes]) :
            raise IndexError("les indexes doivent être dans la liste des verticies")
        
        i0 = indexes[0]
        i1 = indexes[1]
        i2 = indexes[2]
        
        face_idx = len(self.faces)
        i = 0
        
        triplet_i012 = Triplet(i0,i1,i2)
        
        if self.faces == [] :
            face = Face(face_idx, indexes)
            self.faces.append(face)
            return
        
        while i < len(self.faces) and triplet_i012 < self.faces[i].verticies :
            i+=1
            
        # insertion de la face 
        face = Face(face_idx, indexes)
        self.faces.insert(i,face)        
        
     
    def is_zed (self, patch) :
        """
        à partir d'un patch, vérifie si les faces bleu forment un Z sachant que les faces jaunes sont les "haut" du z
        """    
        pass
        
        
class Face () :
    def __init__ (self,id,verticies) :
        self.verticies = Triplet(verticies[0],verticies[1],verticies[2]) #liste d'indice
        self.color = None # 0 ou 1
        self.edges = []
        self.id = id
        self.smallest_angles = (float("inf"),float("inf"),float("inf"))
        
    def compute_smallest_angles (self) :
        v1 = self.verticies[0]
        v2 = self.verticies[1]
        v3 = self.verticies[2]
        a = np.linalg.norm(v1-v2)
        b = np.linalg.norm(v2-v3)
        c = np.linalg.norm(v3-v1)
            
        angle1 = np.arccos((b**2 + c**2 - a**2)/(2*b*c))
        angle2 = np.arccos((a**2 + c**2 - b**2)/(2*a*c))
        angle3 = np.arccos((a**2 + b**2 - c**2)/(2*a*b))
        
        for angle, idx in enumerate([angle1,angle2,angle3]) :
            if self.smallest_angles == None :
                self.smallest_angles = (angle,(idx+1)%3,(idx+2)%3)
            elif idx < self.smallest_angles[1] :
                self.smallest_angles = (angle,(idx+1)%3,(idx+2)%3)
        
        
class Patch () :
    def __init__ (self,faces) :
        self.faces = []
        
    def get_edges (self) :
        edges = []
        for face in self.faces :
            for edge in face.edges :
                if edge not in edges :
                    edges.append(edge)
        return edges
    
    def get_contour (self) : 
        # greedy algorithm extracting tge contour 
        edges = []
        for f in self.faces : 
            for v in f.edges :
                if v in edges :
                    edges.remove(v)
                else :
                    edges.append(v)
        return edges