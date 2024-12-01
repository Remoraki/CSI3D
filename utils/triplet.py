
import numpy as np

class Triplet () :
    def __init__ (self, x,y,z) :
        self.x = x
        self.y = y 
        self.z = z

    def __lt__ (self, triplet2) :
        """ 
        renvoie True si le triplet 1 est plus petit que le triplet 2 par priorité à la variable
        1 puis 2 puis 3.
        """
        
        t1,t2,t3 = self.x, self.y, self.z
        p1, p2,p3 = triplet2
        
        if t1 > p1 :
            return True
        elif t1 == p1 :
            if t2 > p2 :
                return True
            elif t2 == p2 :
                if t3 > p3 :
                    return True
                elif t3 == p3 :
                    return False
                else :
                    return False
            else :
                return False
            
    def __gt__ (self, triplet2) : 
        t1,t2,t3 = triplet2
        p1, p2, p3 = self.x ,self.y, self.z
        
        if t1 > p1 :
            return True
        elif t1 == p1 :
            if t2 > p2 :
                return True
            elif t2 == p2 :
                if t3 > p3 :
                    return True
                elif t3 == p3 :
                    return False
                else :
                    return False
            else :
                return False
            
    def __eq__ (self, triplet2) :
        
        if triplet2 == None : 
            return False
        
        if type(triplet2) is Triplet:
            return all( triplet2[i] == self[i] for i in range(3) )
        else :
            return False
    
    def __getitem__ (self, idx) :
        return [self.x, self.y, self.z][idx]
    
    def __le__ (self, triplet2) : 
        t1,t2,t3 = self.x, self.y, self.z
        p1, p2,p3 = triplet2
        
        if t1 > p1 :
            return True
        elif t1 == p1 :
            if t2 > p2 :
                return True
            elif t2 == p2 :
                if t3 > p3 :
                    return True
                elif t3 == p3 :
                    return False
                else :
                    return True
            else :
                return False

    def __ge__ (self, triplet2) :
        t1,t2,t3 = triplet2
        p1, p2, p3 = self.x ,self.y, self.z
        
        if t1 > p1 :
            return True
        elif t1 == p1 :
            if t2 > p2 :
                return True
            elif t2 == p2 :
                if t3 > p3 :
                    return True
                elif t3 == p3 :
                    return False
                else :
                    return True
            else :
                return False 
            
    def __repr__ (self) :
        return f"Triplet : {self.x} {self.y} {self.z}"
            
    def to_numpy_array(self) : 
        return np.array([self.x, self.y, self.z])
    
    def copy(self) : 
        return Triplet(self.x,self.y,self.z)
    
    def __add__ (self, other) : 
        return Triplet( self.x+other.x,self.y+other.y,self.z+other.z )
    
    def __sub__ (self, other) : 
        return Triplet( self.x-other.x,self.y-other.y,self.z-other.z )
    
    
    
        
def triplet_sort (triplets, indices) : 
    
    if len(triplets) == 1 :
        return triplets, indices
    if len(triplets) == 0 :
        return [],[]
    
    pivot = triplets[0]
    left_idx = []
    right_idx = []
    
    left = []
    right = []

    for idx, triplet in enumerate(triplets) :
        if triplet < pivot :
            left.append(triplet)
            left_idx.append(indices[idx])
            
        elif triplet > pivot :
            right.append(triplet)
            right_idx.append(indices[idx])
            
    next_left,next_idx_left = triplet_sort(left, left_idx)
    next_right,next_idx_right = triplet_sort(right, right_idx)
    
    return next_left + [pivot] + next_right, next_idx_left + [indices[0]] + next_idx_right