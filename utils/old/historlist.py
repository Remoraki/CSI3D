
class Historlist () :
    """
        pls don't store heavy objects in this list ._."
    """
    def __init__ (self) :
        self.lst = []
        self.correspondance = []
        self.raw_lst = []
        
    def append (self, elt) :
        self.lst.append(elt)
        self.correspondance.append(len(self.lst)-1)
        self.raw_lst.append(elt)

    def __getitem__ (self, idx) :
        return self.lst[idx]
    
    def insert(self, idx,elt) : 
        self.lst.insert(idx, elt)
        
        for i in range(len(self.correspondance)) :
            if self.correspondance[i] >= idx :
                self.correspondance[i] += 1
    
        self.correspondance.append(idx)
        self.raw_lst.append(elt)
        
    def remove (self, idx) :
        self.lst.pop(idx)
        
        self.correspondance[ self.correspondance.index(idx) ] = -1

        for i in range(idx,len(self.lst)+1) :
            if self.correspondance[i] != -1 :
                self.correspondance[i] -= 1
            
        
    def __setitem__ (self, idx, elt) :
        self.lst[idx] = elt
        self.raw_lst[ self.correspondance.index(idx) ] = elt
        
    def __len__ (self) :
        return len(self.lst)
    
    def __iter__ (self) :
        return iter(self.lst)
        
        
        
        
        