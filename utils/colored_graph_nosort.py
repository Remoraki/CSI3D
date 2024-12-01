import numpy as np
import matplotlib.pyplot as plt
from .triplet import Triplet

import plotly.graph_objects as go

class ColoredGraph () : 
    def __init__ (self) :
        self.verticies = []
        self.faces = []
        self.adjacence = []


    def add_voisins(self, vertx1, vertx2):
        self.adjacence[vertx1].append(vertx2)
        self.adjacence[vertx2].append(vertx1)

        
    def copy(self) : 
        c = ColoredGraph()
        c.verticies = [v.copy() for v in self.verticies]
        c.faces = [f.copy() for f in self.faces]
        c.adjacence = self.adjacence.copy()
        return c        

    def add_vertice (self, vertice) :
        self.verticies.append(Triplet(vertice[0],vertice[1],vertice[2]))
        self.adjacence.append([])
        
    def set_face (self, verticies,color = 0) :
        f = Face()
        f.verticies = Triplet( verticies[0],verticies[1],verticies[2])
        f.color = color
        f.id = len(self.faces)
        f.color = color
        self.faces.append(f)
        self.add_voisins(verticies[0],verticies[1])
        self.add_voisins(verticies[0],verticies[2])
        self.add_voisins(verticies[1],verticies[2])
        return f.id
    
    def enumerate_over_faces (self) :
        idx = 0
        while idx < len(self.faces) :
            if self.faces[idx] != None :
                yield idx,self.faces[idx]
            idx += 1
        
    def remove_face (self, idx) :
         vertices = self.faces[idx].verticies

         vertex1 = vertices[0]
         vertex2 = vertices[1]
         vertex3 = vertices[2]

         self.adjacence[vertex1].remove(vertex2)
         self.adjacence[vertex1].remove(vertex3)
         self.adjacence[vertex2].remove(vertex1)
         self.adjacence[vertex2].remove(vertex3)
         self.adjacence[vertex3].remove(vertex1)
         self.adjacence[vertex3].remove(vertex2)

         self.faces[idx] = None
       
    
    def  voisins_face(self, f) :
        face = self.faces[f]
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
    
    def enumerate_over_verticies (self) : 
        i = 0
        for v in self.verticies : 
            if v != None : 
                yield i
            else : 
                continue
            i +=1

    def show (self) :
        x,y,z = zip(*[(v.x,v.y,v.z) if v != None else (0,0,0) for v in self.verticies ])
        not_none_faces = [f for f in self.faces if f != None ]
        
        f1,f2,f3 = zip(*[(f.verticies[0],f.verticies[1],f.verticies[2]) for f in not_none_faces])
        color_to_rgb = {0:"#ffe79b",1:"#a7e7ff",2:"#ff69b1",3:"#9d87ff"} # 0 jaune et 1 bleu, 2 rose, 3 lavende
        
        colors = [color_to_rgb[f.color] for f in not_none_faces]
        # text = [f"face {f.id}" for f in not_none_faces]
        
        # fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, i=f1, j=f2, k=f3, facecolor=colors, opacity=1,text=text,hoverinfo="text",hovertext=text)])

        fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, i=f1, j=f2, k=f3, facecolor=colors, opacity=1)])
        # plot all the verticies : 
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers',marker=dict(size=3,color="black"),hoverinfo="text",hovertext=[f"vertice {i}" for i in iter(self.enumerate_over_verticies())]))
        
        # plot the edges : 
        for f in not_none_faces :
            for i in range(3) :
                edge = (f.verticies[i],f.verticies[(i+1)%3])
                x,y,z = zip(*[(self.verticies[e].x,self.verticies[e].y,self.verticies[e].z) for e in edge])
                fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines',line=dict(color="black",width=2)))
        
        
        
        fig.show()
        
    def get_face_neighbours (self, face) :
        neighbours = [0,0,0]
        pts = [self.verticies[i] for i in face.verticies]
        for idx, f in enumerate(self.faces) : 
            nb_communs = 0
            idx_to_assign = 0
            for pt in pts :
                if pt in f.verticies  :
                    nb_communs += 1
                    
            
            if nb_communs == 2 :
                neighbours.append(idx)
        return neighbours
        
        
    def remove_vertice (self, idx) :
        
        to_remove = []
        for i, face in enumerate(self.faces) :
            if face != None and idx in face.verticies :
                to_remove.append(i)
        
        for i in to_remove :
            self.remove_face(i)

        self.verticies[idx]= None # remove the vertice
        
    def __repr__ (self) :
        overview = f"Colored Graph with : \n"
        ofacesverview += f"{len(self.verticies)} verticies \n"
        overview += f"{len(self.edges)} edges \n"
        overview += f"{len(self.faces)} faces \n"
        overview += "-"*20 + "\n"
        
        details = ""
        for f in self.faces :
            details += f"face {f.id} : {f.verticies} \n"
        
        return overview + details
    
    def interpolate_patch (self, patch,idx_bary_relatif) :
        idx_contours = patch.get_contour_verticies(self.faces)
        contour = [self.verticies[i].to_numpy_array() for i in idx_contours]
        
        # compute the barycenter
        bary = np.mean(np.array(contour), axis=0)
        bary = Triplet(bary[0],bary[1],bary[2])
        #self.add_vertice(bary)
        idx_bary = len(self.verticies)+idx_bary_relatif-1
        
        if patch.edges == [] : 
            patch.make_edges(self)
        
        
            
        contour_edge = patch.get_contour_edge(self)
        print("edge : ")
        print(contour_edge)
        print("---")
        
        for idx in patch.faces :
            self.remove_face(idx)
        trips = []
        for idx in range(len(contour_edge)) :
            trip = Triplet(contour_edge[idx][0],contour_edge[idx][1],idx_bary)
            trips.append(trip)
            
        return idx_bary,bary, patch.faces, trips


        
class Face () :
    def __init__ (self) :
        self.verticies =  []
        self.color = 0 
        self.edges = []
        self.smallest_angles = (float("inf"),float("inf"),float("inf"))
        
    def copy(self) : 
        f = Face()
        f.verticies = self.verticies.copy()
        f.color = self.color
        f.edges = self.edges.copy()
        f.smallest_angles = self.smallest_angles
        return f
        
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
    def __init__ (self) :
        self.faces = []
        self.color = 0
        self.adj = None
        self.edges = []
        
    def get_edges (self) :
        edges = []

        for edge in self.edges :
            if edge not in edges :
                edges.append(edge)
        return edges
    
    def get_contour_edge (self,graph) : 
        # greedy algorithm extracting tge contour 
        edges = []
        for v in self.edges :
            if v in edges :
                edges.remove(v)
            elif (v[1],v[0]) in edges :
                edges.remove((v[1],v[0]))
            else :
                edges.append(v)
        return edges
    
    def get_contour_verticies (self,faces) :
        vert = []
        for f in self.faces : 
            for vf in faces[f].verticies :
                if vf not in vert :
                    vert.append(vf)

        return vert
    
    def  make_edges (self,graph) : 
        for f in self.faces :
            for i in range(3) :
                edge = (graph.faces[f].verticies[i],graph.faces[f].verticies[(i+1)%3])
                self.edges.append(edge)
    
    
        
        
    

            
