from ..utils.colored_graph_nosort import ColoredGraph, Face
from ..utils.cg_from_obj import load
from ..utils.triplet import triplet_sort
from tqdm import tqdm
import networkx as nx
import numpy as np


class Compresser:

    def __init__(self, graph: ColoredGraph):
        self.graph = graph
        self.graphs = [graph]
        self.triangless_added = []
        self.triangless_removed = []
        self.verticess_removed = []
        self.errorss = []
    

    def border_vertex(self, set):
        pass

    def two_or_less_and_not_border_vertex(self, ind_set, step):
        graph = self.graphs[step]
        to_remove = []
        for vertex in ind_set:
            adja = graph.adjacence[vertex]
            if len(adja) < 3:
                to_remove.append(vertex)
            else:
                for v in adja:
                    if adja.count(v) != 2:
                        to_remove.append(vertex)
                        break
        for v in to_remove:
            ind_set.remove(v)
        return ind_set


    def independant_algo(self, set, step):
        g = nx.Graph()
        g.add_nodes_from(set)
        for face in self.graphs[step].faces :
            g.add_edge(face.verticies[0], face.verticies[1])
            g.add_edge(face.verticies[1], face.verticies[2])
            g.add_edge(face.verticies[2], face.verticies[0])
        d = nx.maximal_independent_set(g)
        return d

    def independant_set(self, step) :
        verticies = self.graphs[step].verticies ####
        ind_set = []
        for i, vertex in enumerate(verticies):
            if vertex != None:
                ind_set.append(i)
        # A FAIREE
        # set = self.border_vertex(set)
        ind_set = self.two_or_less_and_not_border_vertex(ind_set, step)
        ind_set = self.independant_algo(ind_set, step)
        return ind_set


    def get_patch(self, vertex, step):
        faces = self.graphs[step].faces
        patch_indices = []
        n = len(faces)
        for i in range(n):
            if faces[i] != None and vertex in faces[i].verticies:
                patch_indices.append(i)
        if len(patch_indices) == 0:
            print("MAIS WESH")
        return patch_indices
        


    def color_patches(self, vertices, step):
        N = len(vertices)
        patches = [self.get_patch(vertex, step) for vertex in vertices]
        coloriage = nx.Graph()
        coloriage.add_nodes_from(range(N))
        border = []
        for i in tqdm(range(N), "set coloring"):
            border.append(set(self.graphs[step].adjacence[vertices[i]]))

        for i in tqdm(range(N-1), "Coloring"):
            for j in range(i+1,N):
                vertex_commun = list(border[i] & border[j])
                n = len(vertex_commun)
                break_twice = False
                for v1 in range(n-1):
                    for v2 in range(v1+1,n):
                        if self.graphs[step].adjacence[vertex_commun[v1]].count(vertex_commun[v2]) == 2 :
                            coloriage.add_edge(i,j)
                            break_twice = True
                            break
                    if break_twice:
                            break
        d = nx.greedy_color(coloriage, strategy="smallest_last")
        chosen_ones = []
        for i in range(N):
            if (d[i] < 3):
                chosen_ones.append(i)
        vertices = [vertices[i] for i in chosen_ones]
        patches = [patches[i] for i in chosen_ones]
        d = [d[i] for i in chosen_ones]
        
        return vertices, patches, d
        
        
    def get_error(self, vertex, border, step):
        graph = self.graphs[step]
        xyz = [graph.verticies[vertex].to_numpy_array() for vertex in border]
        barycenter = np.mean(np.array(xyz), axis=0)
        error = graph.verticies[vertex].to_numpy_array() - barycenter
        return error, barycenter

    def construct_patch(self,center, vertices, patches, step):
        
        """Return a set of [v1,v2,v3] triangles"""
        graph = self.graphs[step+1]
        start_point = vertices[0]
        border = [start_point]
        iter_max = 100
        iter = 0
        
        edge_border = []
        for face in patches:
            t_vs = graph.faces[face].verticies
            
            vs = [t_vs[0], t_vs[1], t_vs[2]]
            vs.remove(center)
            vs.sort()
            edge = (vs[0], vs[1])
            if edge in edge_border:
                edge_border.remove(edge)
            else:
                edge_border.append(edge)
        

        while len(edge_border) > 0:
            for edge in edge_border:
                if edge[0] ==  border[-1] and edge[1] in vertices:
                    border.append(edge[1])
                    edge_border.remove(edge)
                    break
                elif edge[1] ==  border[-1] and edge[0] in vertices:
                    border.append(edge[0])
                    edge_border.remove(edge)
                    break
            
            iter += 1
            if iter > iter_max:
                #print("BOUCLE INFINIE")
                break
        # Il faut orienter les normales correctement, en définissant le sens de départ, c'est hyper chiant, on le fera plus tard (non)
        begin = 0
        end = len(border) - 1
        sens = True
        triangles = []

        while begin < end - 1:
            if sens:
                old = begin
                begin += 1
                triangles.append([border[old], border[end], border[begin]])
                sens = False
            else:
                old = end
                end -= 1
                triangles.append([border[old], border[begin], border[end]])
                sens = True
        
        return triangles, border
                    



    def create_new_mesh(self, vertices, patches, colors, step) :
        self.graphs[step+1] = self.graphs[step].copy() 
        graph = self.graphs[step+1]
        errors = []
        false_vertices = []
        N = len(vertices)

        borders = []
        for i in range(N):
            borders += self.graphs[step].adjacence[vertices[i]]
        
        

        for i in range(N):
            
            adja = graph.adjacence[vertices[i]]
            if len(adja) < 3:
                #print("what")
                if len(adja) == 0:
                    print("DANGER")
            else:
                for v in adja:
                    if adja.count(v) != 2:
                        #print("HOOOOW")
                        break
            
            border = self.graphs[step].adjacence[vertices[i]]
            error, false_vertex = self.get_error(vertices[i], border, step)

            errors.append(error)
            false_vertices.append(false_vertex)

            new_faces, ord_bord = self.construct_patch(vertices[i], border, patches[i], step)

            graph = self.graphs[step+1]


            for face in patches[i]:
                self.triangless_removed[step].append(face)

            graph.remove_vertice(vertices[i])

            for face in new_faces:
                index = graph.set_face(face, colors[i] + 1) 
                self.triangless_added[step+1].append(index)
        

        # _ , perm = triplet_sort (false_vertices)
        # self.verticess_removed[step] = vertices[perm]
        # self.errorss[step] = errors[perm]

        
# C'EST DE LA MERDE NOTRE VIE
    # def remontee(self, LOD, path) :

    #     self.graphs[-1].write(path)
    #     vertices = self.graphs[-1].vertexs_indices
    #     faces = self.graphs[-1].faces_indices

    #     for step in range(LOD - 1, -1, -1):

    #         colors = self.colorss[step]  
    #         write(colors[faces])          
            
    
    def compress(self, LOD, path) :

        self.init(LOD)
        
        for step in range(LOD - 1) :
            list_vertex = self.independant_set(step)
            vertices, patches, colors = self.color_patches(list_vertex, step)
            self.create_new_mesh(vertices, patches, colors, step)

        self.remontee(LOD, path)

    def init(self, LOD):
        self.graphs = [ColoredGraph()] * LOD
        self.graphs[0] = self.graph 
        self.blue_triangless = [[]] * LOD
        self.triangless_added = [[]] * LOD
        self.triangless_removed = [[]] * LOD
        self.verticess_removed = [[]] * LOD
        self.errorss = [[]] * LOD

    

def compress(file):
    print("lunch")
    graph = load(file)
    print("File loaded")
    LOD = 2
    compresser = Compresser(graph)
    compresser.init(LOD)
    print("Compresser created")
    set_ind = compresser.independant_set(0)
    print("Independant set calculated : ")
    vertices, patches, colors = compresser.color_patches(set_ind, 0)
    print("Optimal coloration calculated")
    N = len(vertices)
    for i in range(N):
        for face in patches[i]:
            graph.faces[face].color = colors[i] + 1 
    print("Graph colored")
    compresser.create_new_mesh(vertices, patches, colors, 0)
    print("Graph compressed")
    return compresser.graphs[1]

if __name__ == "__main__":
    file = "./horses/obja/example/suzanne.obj"
    compressed_graph = compress(file)
    compressed_graph.show()


