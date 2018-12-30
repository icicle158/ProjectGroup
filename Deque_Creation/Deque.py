class Deque:
    """
    A double-ended queue
    """

    def __init__(self):
        """
        Initializes an empty Deque
        """
        
        #I decided to use a doubly-linked list for my
        #implementation of a deque. (Although, I'm
        #sure that's obvious from my head & tail pointers
        self.head = None
        self.tail = None
        self.parent_head = None
        
        self.size = 0
        self.retain_check = False
        
        pass

    def __len__(self):
        """
        Computes the number of elements in the Deque
        :return: The logical size of the Deque
        """
        #All it needs to return is the current size of the deque
        return self.size

    def peek_front(self):
        """
        Looks at, but does not remove, the first element
        :return: The first element
        """
        #Simply look at the data
        if self.head != None:
            return self.tail.data
        
        else:
            raise IndexError

    def peek_back(self):
        """
        Looks at, but does not remove, the last element
        :return: The last element
        """
        
        if self.tail != None:
            return self.head.data
        
        else:
            raise IndexError

    def push_front(self, e):
        """
        Inserts an element at the front of the Deque
        :param e: An element to insert
        """
        #Create a new node
        new_node = Node(e)
        #If the size is empty...
        if self.size == 0:
            #Set head and tail nodes to newly created node
            self.head = new_node
            self.tail = new_node
            
        #If not empty...
        else:
            #Find the current tail's next pointer and set it
            #to the new node
            self.tail.next = new_node
            #Create a temporary node holding the current node
            temp_node = self.tail
            #Set the current tail pointer to the newly created node
            self.tail = new_node
            #Set the tail's before pointer to point to the node before it
            self.tail.before = temp_node
        #increment the size by 1
        self.size += 1

        pass


    def push_back(self, e):
        """
        Inserts an element at the back of the Deque
        :param e: An element to insert
        """
        
        #A very similar process to push_front, though
        #done with the head pointer this time
        new_node = Node(e)
        
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
            
        else:
            self.head.before = new_node
            temp_node = self.head
            self.head = new_node
            self.head.next = temp_node       
                   
        self.size += 1
        
        pass

    def pop_front(self):
        """
        Removes and returns the first element
        :return: The (former) first element
        """
     
        #If the size is less than or equal to zero, you can't pop
        #thus, raise an error
        if self.size <= 0:
            raise IndexError
            
        #If the doubly linked list has exactly one element
        elif self.size == 1:
            #immediately decrement the size
            self.size -= 1
            #Set a temporary variable to the current tail pointer's
            #data payload
            temp_var = self.tail.data
            #Set the current tail value to None in order to free memory
            self.tail = None
            #Return the collected data
            return temp_var
            
        #If the doubly linked list has more than 1 element
        else:
            self.size -= 1
            
            temp_var = self.tail.data
            #Set the current tail to the one before it
            self.tail = self.tail.before
            self.tail.next = None
            
            return temp_var
            
        

    def pop_back(self):
        """
        Removes and returns the last element
        :return: The (former) last element
        """
        #Completely similar to pop_front, though done with
        #the head pointer
        if self.size <= 0:
            raise IndexError
            
        elif self.size == 1:
            
            self.size -= 1
            
            temp_var = self.head.data
            
            self.head = None
            
            return temp_var
            
        else:
            
            self.size -= 1
        
            temp_var = self.head.data
            
            self.head = self.head.next
            
            self.head.before = None
            
            return temp_var
        
        

    def clear(self):
        """
        Removes all elements from the Deque
        :return:
        """
        #If the size is greater than zero
        while self.size > 0:
            #Run through the doubly linked list until there
            #are no more nodes
            if self.tail.before == None:
                #Set everything to None
                self.tail = None
                self.head = None
                self.size -= 1
                break
            #Run through the doubly linked list...
            if self.tail.before != None:
                #If a value is found, make the tail equal to the one
                #before it
                self.tail = self.tail.before
                #Clear the node after the transfer
                self.tail.next = None
            #Decrement the size
            self.size -= 1
            
        pass

    def retain_if(self, condition):
        """
        Removes items from the Deque so that only items satisfying the given condition remain
        :param condition: A boolean function that tests elements
        """
        if self.head == None:
                return None
                pass
        else:
            #Use a loop to iterate through the doubly linked list
            while self.head.next != None:
                #Boolean value used for checking if this function
                #has been called
                self.retain_check = True
                #If the condition is true on the current head's data,
                #set the head node to the next node
                if condition(self.head.data) == True:
                    self.head = self.head.next
                    pass
                
                #Otherwise...
                else:
                    self.size -= 1
                    #Set a temporary head node as the current head node's
                    #previous head node
                    temphead = self.head.before
                    #Set a temporary head node as the current head node's
                    #next head node
                    tempheadnext = self.head.next
                    #Clear the current head value, thus freeing up memory
                    #and deleting it from the list
                    self.head = None
                    #Set the current head as the next head value, which was
                    #saved in the tempheadnext variable
                    self.head = tempheadnext
                    #Bind the current head's before pointer to the previous
                    #head node's before pointer
                    #(Long story short, this whole process binds two links
                    #together whilst removing a link in between them)
                    self.head.before = temphead
                
            #If there is no more head nodes to run through in the
            #doubly linked list, set the tail node to the correct
            #head node (in order to run the function as intended)
            if self.head.next == None:
                self.tail = self.head.before
    
                
            if condition(self.head.data) == True:
                pass
            else:
                self.size -= 1
            
        pass

    def __iter__(self):
        """
        Iterates over this Deque from front to back
        :return: An iterator
        """  
        
        #A simple iterator which runs through the doubly linked
        #list and yields the data payloads within the list
        if self.tail == None:
            yield None
            pass
        
        if self.tail != None:
            if self.tail.before != None:
                temp_var = self.tail.data
                self.tail = self.tail.before
                yield temp_var
            else:
                yield self.tail.data
                
    

    # provided functions

    def is_empty(self):
        """
        Checks if the Deque is empty
        :return: True if the Deque contains no elements, False otherwise
        """
        return len(self) == 0

    def __repr__(self):
        """
        A string representation of this Deque
        :return: A string
        """
        return 'Deque([{0}])'.format(','.join(str(item) for item in self))
    
    
#Node class which was created for the doubly linked list
#Nothing fancy, all it needs is a data payload, and pointers
#to the next and previous nodes
class Node:
    
    def __init__(self, data_payload, next_node = None, before_node = None):
        
        self.data = data_payload
        self.next = next_node
        self.before = before_node
        
   
        
        
        

