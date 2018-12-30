
class HashMap:
    def __init__(self, load_factor=.7):
        # You may change the default maximum load factor
        self.max_load_factor = load_factor
        # Other initialization code can go here
        
        
        #Construct an initial hash table with finite table size of 20
        self.hash_map = [None]*20
        
        #Hash positions
        self.hash_pos = []
        
        #Used for determining how many elements are in the hash table
        #along with the table's current capacity
        self.size = 0
        self.capacity = 20

    #The size of the hash table
    def __len__(self):
        return self.size

    #Load function displays the current load factor, which
    #is the total elements in the hash table/hash table capacity
    def load(self):
        load_factor = self.size/self.capacity
        return load_factor

    #Contains function used for operator 'in'
    def __contains__(self, key):
        #Create a hashed_key for inputting into a hash function
        hashed_key = hash(key)
        #Use a simple hash function to input the data into the hash table (map)
        hash_position = hashed_key % self.capacity
        #If the hash table has elements...
        if self.size > 0:
            #Check if the hash map (table)'s current position is
            #None or empty, if it isn't use linear probing to solve the issue
            if self.hash_map[hash_position] != None:
                #find that specific position in the hash map, and if the key
                #at that position isn't equivalent to the input key, begin
                #probing
                if self.hash_map[hash_position][0] != key:
                    x = hash_position + 1
                    #Collisions are resolved through linear probing
                    while x <= self.capacity:
                        if x >= self.capacity:
                            x = 0
                        else:
                            #If the hash map at the current position is equivalent to None
                            #continue
                            if self.hash_map[x] == None:
                                x += 1
                                #This is used to determine if a full loop has been made within
                                #the hash table. If it has, break the loop, the key doesn't exist
                                if x == hash_position + 1:
                                    return False
                                    break
                                continue
                            #If there is a key in the hash map with the same name as the
                            #input key, return true
                            if self.hash_map[x][0] == key:
                                return True
                            else:
                                x += 1
                                if x == hash_position + 1:
                                    return False
                                    break
                                continue
                #Return true if the key has been found
                else:
                    return True
                
            #If there is a key in the currently hashed position, begin probing
            else:
                #A probe limit is introduced. The concept is: if a well enough hashing
                #function is built, a table should have very few collisions. Thus, with
                #smaller tables, in order to determine if there ISN'T a key within a smaller table
                #there should be a limit to how many times it linearly probes for a key value.
                #I have very generously set the probing limit to 5, which enables 5 linear probes
                #before the table determines the value doesn't exist within the table. In reality
                #My code only needs 3 or so for very small tables.
                probe_limit = 5
                
                #Very similar probing loop to __contains__
                x = hash_position + 1
                while x <= self.capacity:
                    if probe_limit == 0:
                        return False
                    if x >= self.capacity:
                        x = 0
                    else:
                        if self.hash_map[x] == None:
                            x += 1
                            probe_limit -= 1
                            if x == hash_position + 1:
                                return False
                                break
                            continue
                        if self.hash_map[x][0] == key:
                            return True
                        else:
                            x += 1
                            probe_limit -= 1
                            if x == hash_position + 1:
                                return False
                                break
                            continue
                
                return False

    #A function I have designed to resize the table if the load factor reaches
    #a certain point
    def table_size_check(self):
        if (self.size/self.capacity) >= self.max_load_factor:
            #Create a temporary copy of the current hash map
            temp_map = self.hash_map
            #Double the total capacity
            self.capacity *= 2
            #Create a new hash map with the new capacity
            self.hash_map = [None]*self.capacity
            
            #take all of the values from the old map, and re-hash them into
            #the new map
            for key_item in temp_map:
                if key_item == None:
                    continue
                
                #Re-hashing is ABSOLUTELY NEEDED for the new table! If these
                #values aren't re-hashed, the table becomes out of alignment
                #when attempting to re-index it
                hashed_key = hash(key_item[0])
                hash_position = hashed_key % self.capacity
                
                #Simply runs through the old map, and creates a new map
                #from it
                if self.hash_map[hash_position] != None:
                       
                    x = hash_position + 1
                    while x <= self.capacity:
                        if x == self.capacity:
                            x = 0
                        else:
                            if self.hash_map[x] != None:
                                x += 1
                                continue
                            else:
                                self.hash_map[x] = key_item
                                break
                                
                else:
                    self.hash_map[hash_position] = key_item
             
    #__getitem__ function find the hash position in the hash table and
    #retrieves the values associated with the keys
    def __getitem__(self, key):
        
        hashed_key = hash(key)
        
        hash_position = hashed_key % self.capacity
        
        #Once again, similar in principal to the __contains__ function
        if self.size > 0:
            
            if self.hash_map[hash_position] != None:
                if self.hash_map[hash_position][0] != key:
                    x = hash_position + 1
                    while x <= self.capacity:
                        if x >= self.capacity:
                            x = 0
                        else:
                            if self.hash_map[x] == None:
                                x += 1
                                if x == hash_position + 1:
                                    raise KeyError(key)
                                    break
                                continue
                            if self.hash_map[x][0] == key:
                                value = self.hash_map[x][1]
                                return value[-1]
                            else:
                                x += 1
                                if x == hash_position + 1:
                                    raise KeyError(key)
                                    break
                                continue
                else:
                    #With the way my hash table is set up, each entry is a list
                    #with a key and a list pairing. The list associated with the
                    #key contains ALL of the key's associated values. The specification
                    #of the function simply wants me to return the last element in that
                    #value list (since the project states it wants only the most recent
                    #value associated with the key)
                    value = self.hash_map[hash_position][1]
                    return value[-1]
            else:
                x = hash_position + 1
                while x <= self.capacity:
                    if x >= self.capacity:
                        x = 0
                    else:
                        if self.hash_map[x] == None:
                            x += 1
                            if x == hash_position + 1:
                                raise KeyError(key)
                                break
                            continue
                        if self.hash_map[x][0] == key:
                            value = self.hash_map[x][1]
                            return value[-1]
                        else:
                            x += 1
                            if x == hash_position + 1:
                                raise KeyError(key)
                                break
                            continue
        #Raises key error if the value does not exist
        raise KeyError(key)

    #Set item inserts a key and value pair into the hash map
    def __setitem__(self, key, value):
        
        #Hashes a key
        hashed_key = hash(key)
        #Use hash function to insert into table
        hash_position = hashed_key % self.capacity
        
        #This value is what is stored into the physical hash table
        #Upon creation, a key is stored within a list, followed by
        #a list for values. every time a key is found in the list,
        #and it matches the input key, it's value list is updated
        mapping = [key, []]
        
        #Similar hashing structure as with other functions
        if self.hash_map[hash_position] != None:
            if self.hash_map[hash_position][0] == key:
                self.hash_map[hash_position][1].append(value)
                
            #Uses linear probing to resolve collisions
            else:
                x = hash_position + 1
                while x <= self.capacity:
                    if x == self.capacity:
                        x = 0
                    else:
                        if self.hash_map[x] != None:
                            if self.hash_map[x][0] == key:
                                self.hash_map[x][1].append(value)
                                break
                            x += 1
                            continue
                        else:
                            mapping[1].append(value)
                            self.hash_map[x] = mapping
                            self.size += 1
                            #Checks the table after every insert, to ensure
                            #the load factor is at the correct level. If the
                            #load factor goes over the maximum leve, the table
                            #is resized
                            HashMap.table_size_check(self)
                            break
                        
        else:
            mapping[1].append(value)
            self.hash_map[hash_position] = mapping
            self.size += 1
            HashMap.table_size_check(self)
        
        
    #This function is used to desize the table after enough elements from the
    #Hash table have been deleted.
    def desize_table_check(self):
        
        #Finite starting capacity is set to 20, thus don't resize the table
        #if the capacity is equivalent to or lower than 20 (The table size
        #should never be under 20)
        if (self.capacity > 20):
            if self.size <= (self.capacity/2)*self.max_load_factor:
                #Create a temporary map as a copy of the old map
                temp_map = self.hash_map
                #divide the total capacity by 2
                self.capacity //= 2
                #Create a new hash map with the new capacity
                self.hash_map = [None]*self.capacity
          
                #Similar to resizing a table
                for key_item in temp_map:
                    if key_item == None:
                        continue
                    
                    hashed_key = hash(key_item[0])
                    hash_position = hashed_key % self.capacity
                    
                    if self.hash_map[hash_position] != None:
                           
                        x = hash_position + 1
                        while x <= self.capacity:
                            if x == self.capacity:
                                x = 0
                            else:
                                if self.hash_map[x] != None:
                                    x += 1
                                    continue
                                else:
                                    self.hash_map[x] = key_item
                                    break
                                    
                    else:
                        self.hash_map[hash_position] = key_item
            

    #similar style of function to __contains__ or __getitem__
    #This function takes a key, looks it up in the hash map,
    #and if it finds it, it deletes it (replaces it's key,value pair
    #with 'None')
    def __delitem__(self, key):
        
        
        probe_limit = 5
        
        hashed_key = hash(key)
        
        hash_position = hashed_key % self.capacity
        
        #Once again, similar in principal to the __contains__ function
        if self.size > 0:
            
            if self.hash_map[hash_position] != None:
                if self.hash_map[hash_position][0] != key:
                    x = hash_position + 1
                    while x <= self.capacity:
                        if probe_limit == 0:
                            raise KeyError(key)
                            break
                        if x >= self.capacity:
                            x = 0
                        else:
                            if self.hash_map[x] == None:
                                x += 1
                                probe_limit -= 1
                                if x == hash_position + 1:
                                    raise KeyError(key)
                                    break
                                continue
                            if self.hash_map[x][0] == key:
                                self.hash_map[x] = None
                                self.size -= 1
                                HashMap.desize_table_check(self)
                                return
                            else:
                                x += 1
                                probe_limit -= 1
                                if x == hash_position + 1:
                                    raise KeyError(key)
                                    break
                                continue
                else:
                    self.hash_map[hash_position] = None
                    self.size -= 1
                    HashMap.desize_table_check(self)
                    return
            else:
                x = hash_position + 1
                while x <= self.capacity:
                    if probe_limit == 0:
                        raise KeyError
                        break
                    if x >= self.capacity:
                        x = 0
                    else:
                        if self.hash_map[x] == None:
                            x += 1
                            probe_limit -= 1
                            if x == hash_position + 1:
                                raise KeyError(key)
                                break
                            continue
                        if self.hash_map[x][0] == key:
                            self.hash_map[x] = None
                            self.size -= 1
                            HashMap.desize_table_check(self)
                            return
                        else:
                            x += 1
                            probe_limit -= 1
                            if x == hash_position + 1:
                                raise KeyError(key)
                                break
                            continue
        raise KeyError(key)

    #Iterates through the hash map, and yields all value pairs
    def __iter__(self):
        for key_item in self.hash_map:
            if key_item:
                #Simply yields the last element of the value list
                #for a given key
                yield (key_item[0],key_item[1][-1])

    #Clear function runs through the hash map and replaces all key, value
    #pairs with 'None' if such a pair is found
    def clear(self):
        
        x = 0
        for key_item in self.hash_map:
            if key_item:
                self.hash_map[x] = None
            x += 1
        
        #Reconstructs the original table after all key, value pairs have
        #have been cleared from the original list
        self.hash_map = [None]*20
        self.size = 0
        self.capacity = 20
        pass
    
    
    #This is a special helper function that calculates the occurence of a
    #particular key within the hash map. This is done by returning the length
    #of the key's value list (which is why I designed the project this way)
    def value_occurence(self, key):
        
        #Once again, this uses a similar hashing function as compared to some
        #of the others. Hashes a key, finds that key's position, if the key isn't
        #found at it's position, resolve the collision using linear probing, with
        # a set probing limit
        hashed_key = hash(key)
        hash_position = hashed_key % self.capacity
        
        if self.hash_map[hash_position] != None:
            if self.hash_map[hash_position][0] != key:
                x = hash_position + 1
                while x <= self.capacity:
                    if x >= self.capacity:
                        x = 0
                    else:
                        if self.hash_map[x] == None:
                            x += 1
                            if x == hash_position + 1:
                                return None
                            continue
                        if self.hash_map[x][0] == key:
                            return len(self.hash_map[x][1])
                        else:
                            x += 1
                            if x == hash_position + 1:
                                return None
                            continue
            else:
                return len(self.hash_map[hash_position][1])
        else:
            probe_limit = 1
                
            x = hash_position + 1
            while x <= self.capacity:
                if probe_limit == 0:
                    return False
                if x >= self.capacity:
                    x = 0
                else:
                    if self.hash_map[x] == None:
                        x += 1
                        probe_limit -= 1
                        if x == hash_position + 1:
                            return None
                            break
                        continue
                    if self.hash_map[x][0] == key:
                        return len(self.hash_map[x][0])
                    else:
                        x += 1
                        probe_limit -= 1
                        if x == hash_position + 1:
                            return None
                            break
                        continue
            
            return None
        

    #This function simply runs through the hash map and adds all of the keys
    #within it, to a set, then it returns the set
    def keys(self):
        key_set = set()
        
        for key_item in self.hash_map:
            if key_item:
                key_set.add(key_item[0])
        return key_set

    # supplied methods

    def __repr__(self):
        return '{{{0}}}'.format(','.join('{0}:{1}'.format(k, v) for k, v in self))

    def __bool__(self):
        return not self.is_empty()

    def is_empty(self):
        return len(self) == 0


# Required Function
        
#This function takes in a sequence, then for every element within the sequence,
#if the key isn't in the hashing map, add the key to the hashing map. The very first
#value is irrelevant. It's simply set because it is required. After the initial
#key is created, a new value containing the current occurence of a particular key, is appended
#into the value list. Thus, when checking to see if a key is within the map, that key will return
#its number of occurences
def word_frequency(seq):
    
    hashing_map = HashMap()
    
    for value, key in enumerate(seq):
        if key not in hashing_map:
            hashing_map[key] = value
        #This sets the new value equal to the key occurence
        hashing_map[key] = hashing_map.value_occurence(key)
       
        
    
    return hashing_map
