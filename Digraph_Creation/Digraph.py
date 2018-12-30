import math


class Digraph:
    def __init__(self, n):
        """
        Constructor
        :param n: Number of vertices
        """
        self.order = n
        self.size = 0
        # You may put any required initialization code here
        self.vertice_dict = {}
        self.total_vertice_list = []
        
        self.in_vert = {}
        self.out_vert = {}
        pass

    def insert_arc(self, s, d, w):
        
        if s not in self.total_vertice_list:
            self.total_vertice_list.append(s)
        if d not in self.total_vertice_list:
            self.total_vertice_list.append(d)
            
        if len(self.total_vertice_list) > self.order:
            raise IndexError
            
        #Create two separate dictionaries for keeping
        #track of in and out degrees for each vertice
        if d in self.in_vert:
            self.in_vert[d] += 1
        else:
            self.in_vert[d] = 1
            self.out_vert[d] = 0
            
        if s in self.out_vert:
            self.out_vert[s] += 1
        else:
            self.out_vert[s] = 1
            self.in_vert[s] = 0
            
            
        self.vertice_dict[s,d] = w
        
        
        self.size = len(self.vertice_dict)
        pass

    def out_degree(self, v):
        if v not in (self.in_vert or self.out_vert):
            raise IndexError
        if v in self.out_vert:
            return self.out_vert[v]

    def are_connected(self, s, d):
        if s not in self.total_vertice_list or d not in self.total_vertice_list:
            raise IndexError
        if (s,d) in self.vertice_dict:
            return True
        else:
            return False

    def is_path_valid(self, path):
        
        for vertex in path:
            if vertex not in self.in_vert or vertex not in self.out_vert:
                raise IndexError
        
        if self.out_vert[path[0]] == 0:
            return False
        if self.in_vert[path[len(path)-1]] == 0:
            return False
        
        for vertex in path[1:len(path)-1]:
            if self.in_vert[vertex] == 0 and self.out_vert[vertex] == 0:
                return False
        
        return True

    def arc_weight(self, s, d):
        if s not in self.out_vert or d not in self.in_vert:
            raise IndexError
        
        if (s,d) not in self.vertice_dict:
            return math.inf
        else:
            return self.vertice_dict[(s,d)]
        #return math.inf

    def path_weight(self, path):
        
        if len(path) == 1:
            return 0
        
        total_weight = 0
        i = 0
        while( i < len(path)):
     
            if (path[i] not in self.out_vert) or (path[i+1] not in self.in_vert):
                raise IndexError
            
            if (path[i],path[i+1]) not in self.vertice_dict:
                return math.inf
            else:
                total_weight += self.vertice_dict[(path[i],path[i+1])]
    
            if (i+1) == (len(path)-1):
                break
            i += 1
        
        return total_weight

    def does_path_exist(self, s, d):
        
        keys_sorted = list(self.vertice_dict.keys())
        keys_sorted.sort()
        
        if s not in self.out_vert or d not in self.in_vert:
            raise IndexError
        
        if s == d:
            return True
        
        if (s,d) in keys_sorted:
            return True
            
        to_visit = []
        to_visit.append(s)
        
        i = 0
        while(i < len(keys_sorted)):
            
            #If the out degree of the vertex in the list of vertex pairs
            #is less than the input starting vertex, advance the loop
            #one iteration
            if keys_sorted[i][0] < to_visit[0]:
                i += 1
                continue
            
            if keys_sorted[i][0] != to_visit[0]:
                to_visit.pop(0)
                
            if len(to_visit) == 0:
                return False
                
            if keys_sorted[i][0] == to_visit[0]:
                if keys_sorted[i][1] == d:
                    return True
                
                #Please come back to this. It is VERY important
                if keys_sorted[i][1] < keys_sorted[i][0]:
                    i = 0
                    continue
                
                to_visit.append(keys_sorted[i][1])
            
            i += 1
        return False

    def find_min_weight_path(self, s, d):
        
        keys_sorted = list(self.vertice_dict.keys())
        keys_sorted.sort()
        
        if s not in self.out_vert or d not in self.in_vert:
            raise IndexError
        
        if (s,d) in keys_sorted:
            return [s,d]
        
        if s == d:
            return [s]
        
        to_visit = []
        to_visit.append(s)
        
        special_weight = {}
        
        weight_list = {}
        
        min_path = []
        min_path.append(s)
        
        min_weight = 0.0
        
        i = 0
        while(i < len(keys_sorted)):
            
            if keys_sorted[i][0] < to_visit[0]:
                i += 1
                continue
            
            if to_visit[0] != keys_sorted[i][0]:
                if weight_list and not special_weight:
                    min_weight = min(weight_list.keys())
                    min_path.append(weight_list[min_weight])
                    weight_list.clear()
                to_visit.pop(0)
                
                
            if len(to_visit) == 0:
                if special_weight:
                    min_weight = min(special_weight.keys())
                    min_path.append(special_weight[min_weight])
                    special_weight.clear()
                    return min_path
                else:
                    return ValueError
            
            
            if to_visit[0] == keys_sorted[i][0]:
                if keys_sorted[i][1] == d:
                    special_weight[self.vertice_dict[keys_sorted[i]]] = keys_sorted[i][1]
                else:
                    to_visit.append(keys_sorted[i][1])
                    weight_list[self.vertice_dict[keys_sorted[i]]] = keys_sorted[i][1]
                
            i += 1
            
        
        if special_weight:
            min_weight = min(special_weight.keys())
            min_path.append(special_weight[min_weight])
            special_weight.clear()
        return min_path

