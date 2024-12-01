from ..utils.colored_graph_nosort import ColoredGraph
from ..utils.cg_from_obj import main as cg_from_obj
from ..utils.triplet import Triplet

class Objc () :
    """
        cette classe permet de lire écrire et initerprêter les fichiers .objc
        c'est comme des obj MAIS 
            + comprend des listes de couleurs
            + comprend des listes d'erreures 
    """
    
    def __init__ (self) :
        self.graph = ColoredGraph()
        self.errors = []
        self.obja = ""
        self.line_buffer = ""
        self.file = None
        
        self.verticies = []
        self.faces = []
    
    def create_file (self, filename) : 
        self.filename = filename
        self.file = open(filename, "w")
        
    def write_colors (self, colors) :
        self.line_buffer = "c "+"".join([str(c) for c in colors])+"\n"
        self.file.write(self.line_buffer)
        
    def write_face (self, face) : 
        self.line_buffer = f"f {face.verticies[0]} {face.verticies[1]} {face.verticies[2]}\n"
        self.file.write(self.line_buffer)
        
    def write_vertex (self, vertex) :
        self.line_buffer = f"v {vertex.x} {vertex.y} {vertex.z}\n"
        self.file.write(self.line_buffer)
    
    def write_error (self, error) : 
        self.line_buffer = f"e {error.x} {error.y} {error.z}\n"
        self.file.write(self.line_buffer) 
    
    def graph_to_obja (self) :
        for v in self.graph.verticies :
            self.obja += f"v {v.x} {v.y} {v.z}\n"
        for f in self.graph.faces :
            self.obja += f"f {f.verticies[0]} {f.verticies[1]} {f.verticies[2]}\n"
            
    def close_file (self) :
        self.file.write("EOF")
        self.file.close()
        
    def parse_line (self,line) :
        """
            parse une ligne d'un fichier .objc
                + v suivit d'un triplet de float : une vertex
                + f suivit d'un triplet d'indice : une face
                + c suivit d'une liste de nombre (1 ou 0) : les couleurs  PAS SÉPARÉS PAR DES ESPACES !!!!
                + e suivit d'un triplet de float : une erreure
        """
        
        line = line.strip()
        
        line_split = line.split(" ")
        arg = line_split[0]
        if arg == "v" :
            vertex = Triplet( float(line_split[1]), float(line_split[2]), float(line_split[3]) )
            self.graph.add_vertice(vertex)
            self.obja += line
            self.verticies.append(vertex)
        elif arg == "f" :
            face = Triplet( int(line_split[1]), int(line_split[2]), int(line_split[3]) )
            self.graph.set_face(face)
            self.obja += line
            self.faces.append(face)
            
        # les couleurs
        elif arg == "c" : 
            idx = 0
            idx_face = 0
            while idx < len(line_split[1]) :
                c = line_split[1][idx]
                #self.graph.faces[idx_face].color = int(c)
                while self.graph.faces[idx_face] is None : 
                    idx_face += 1
                self.graph.faces[idx_face].color = int(c)
                idx_face +=1
                idx += 1 # on ne bouge que si on a bien un face
                              
        # les erreures  
        elif arg == "e" :
            error = Triplet( float(line_split[1]), float(line_split[2]), float(line_split[3] ))
            self.errors.append(error)
        elif arg == "EOF" :
            return "EOF"
            
        return arg
    
    def add_face (self, face) :
        self.obja += f"f {face.verticies[0]} {face.verticies[1]} {face.verticies[2]}\n"
    
    def add_vertex (self, vertex) :
        self.obja += f"v {vertex.x} {vertex.y} {vertex.z}\n"
            
            
    def open_objc_from_path (self, path) :
        error_mod = False
        initialization = True
        # c'est immonde mais tkt ça marche
        with open(path, "r") as f :
            for line in f :
                if initialization and line[0] == "v" and line[0] == "f" :
                    arg = self.parse_line(line)
                    continue
                elif initialization and line[0] == "c" : 
                    initialization = False
                    print("hihih chocolat")
                    yield None

                if line[0] != "e" and error_mod : 
                    yield self.errors
                    error_mod = False
                    self.errors = []                    
                    
                arg = self.parse_line(line)
                
                if arg == "e" : 
                    error_mod = True
                if arg == "EOF" : 
                    yield self.errors
                    break

                
    def open_obj (self, path) : 
        self.graph = cg_from_obj(path)
                
    def save_objc (self, path) :
        with open(path, "w") as f :
            for v in self.graph.verticies :
                f.write(f"v {v.x} {v.y} {v.z}\n")
                
            for f in self.graph.faces :
                f.write(f"f {f.verticies[0]} {f.verticies[1]} {f.verticies[2]}\n")
                
            for e in self.errors :
                f.write(f"e {e.x} {e.y} {e.z}\n")
            
            to_write = ""
            for c in self.graph.faces :
                if c == 0 :
                    to_write += "0"
                else :
                    to_write += "1"
                    
            f.write(f"c {to_write}\n")
            
            
            
            
            
        
        