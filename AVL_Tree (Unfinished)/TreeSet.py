class TreeSet:
    """
    A set data structure backed by a tree.
    Items will be stored in an order determined by a comparison
    function rather than their natural order.
    """
    def __init__(self, comp):
        """
        Constructor for the tree set.
        You can perform additional setup steps here
        :param comp: A comparison function over two elements
        """
        #A very large list of variables used for processing a multitude of information
        self.comp = comp
        
        #Head node, root nodes, temporary counters, re-order variabels: for holding nodes
        #to be reordered
        self.head = None
        self.root = None
        self.temp_cnt = 0
        self.node_cnt = 0
        self.big_reorder = None
        self.right_order = None
        self.left_order = None
        
        self.first_val = None
        self.last_val = None
        
    
        #Special list, with an unfortunate creation name. This list holds nodes
        #after len has been called. Can be used for reconstructing a tree
        self.test_list = []
        
        #A series of checks or flags that are used for discovering specific nodes
        #in a recursive call
        self.right_check = False
        self.left_check = False
        
        self.root_check = False
        self.rem_reorder = None
        
        self.none_check = False
        
        self.remove_check = False
        self.match_check = False
        self.final_rem_check = False
        self.head_remove_check = False
        
        
    #Straight-forward recursive function, used for checking if there is a node
    #Then it proceeeds to recursively count all nodes in that tree
    def recurse(self, node):
        
        if node != None:
            #Appends to the master node list (in order)
            self.test_list.append(node.data)
            if(node.left != None):
                #Increments count and calls more recursion
                self.node_cnt + self.recurse(node.left)
            if(node.right != None):
                self.node_cnt + self.recurse(node.right)
                
            if((node.left == None and node.right == None) and self.head == node):
                self.node_cnt = 1
                return self.node_cnt
            #Increments as the program is recursively called
            self.node_cnt += 1
            return self.node_cnt
        
        else:
            return 0
    
    #Length function that accesses a recursive function
    def __len__(self):
        element_cnt = 0
        if (self.head != None):
            
            element_cnt = self.recurse(self.head)
            self.test_list = []
            self.node_cnt = 0
            return element_cnt
            
        else:
            return 0

    #Another recursive function that has been created to define the height
    #of a given tree, starting at the head node. Counts the height of the
    #tree based on the count of connections between nodes
    def height_traverse(self, node):
        
       
        #Check if there is a node...
        if node != None:
            #It is important to check if there is a right node or a left node.
            #If so, proceed...
            if(node.left or node.right):
                
                #These two variables are used to hold the values returned
                #From traversing the tree. temp_l_traverse holds comparison value
                #from left nodes, and temp_r_traverse holds comparison value from 
                #right nodes. These are recursive calls and create sub-trees
                temp_l_traverse = self.height_traverse(node.left)
                temp_r_traverse = self.height_traverse(node.right)
                
                #This function takes the comparison value from the left
                #node and recursively compares itself with the right node.
                #If the value of the left node height is greater
                #than or equal to the right node height, add one to the total 
                #height and loop
                #(The very first leaf that is compared will always have a
                #left node at None and a right node at None. Thus, since this
                #recursive function returns 0 for a 'None' Node, the left and right
                #Node heights are set to 0, compared, and since they are always
                #Initially equal (because it's a leaf), there is a recursive call 
                #up the tree, setting the next node's left and right node heights
                #respectively)
                if temp_l_traverse >= temp_r_traverse:
                    return 1 + temp_l_traverse
                #Same as the left but this time checking if the right node height
                #is greater than the left. If it is, increment the total tree
                #height by 1
                if temp_r_traverse > temp_l_traverse:
                    return 1 + temp_r_traverse
                
            #Otherwise... if there is a node that doesn't have children, return 0.
            #This is used to keep track of the height with respect to sides, not 
            #nodes. Any node without children is returned as 0, which keeps the 
            #height correct with respect to the sides (connection between two nodes) 
            #of the tree
            else:
                return 0
        
        #If there isn't a node, return 0
        else:
            return 0
                
    #Height function with a simple, yet powerful recursive function. Allows
    #for a comparison between a node's children and returns a height based off 
    #those comparisons
    def height(self):
        
        if(self.head != None):
            #Used to hold the actual height of the tree
            height_cnt = self.height_traverse(self.head)
            return height_cnt
        
        else:
            return -1
        
    
    #The big balance function is used for the second part of the balanced tree.
    #The initial reording balances a list based off of smaller node clusters.
    #This balance function takes in a completed tree, and scans it for any
    #height irregularities. If it finds one, it rebalnces the tree based on
    #It's current root node and either it's left or right subchild
    def big_balance(self, node):
        if node != None:
            
            temp_l_traverse = self.recurse_reorder(node.left)
            temp_r_traverse = self.recurse_reorder(node.right)
            
            #Trick used to capture a specific height traversal
            if(temp_l_traverse == (temp_r_traverse - 2)):
                    #Ensure that this is a small balance, and not a big one
                    if(temp_r_traverse != 2):
                        #Set temporary nodes, and swap the values to the correct
                        #locations
                        temp_node = node
                        temp_node_spec = temp_node.right.left
                        
                        node = temp_node.right
                            
                        node.left = temp_node
                        node.left.right = temp_node_spec
                        
                        self.head = node
                        
            #Exactly the same except for the right side
            if(temp_r_traverse == (temp_l_traverse - 2)):
                if(temp_l_traverse != 2):
                    temp_node = node
                    temp_node_spec = temp_node.left.right
                    
                    node = temp_node.left
                    
                    node.right = temp_node
                    node.right.left = temp_node_spec
                    
                    self.head = node
  
            #Compares the two traversals, if one is greater than the other,
            #then return the height of the next node's right or left node
            if temp_l_traverse > temp_r_traverse:
                return 1 + temp_l_traverse
           
            else:
                return 1 + temp_r_traverse
 
        else:
            return 0
  
    
    #Seriously, look at this thing. It's beautiful. It is used to partially
    #re-order (Balance) the list. As nodes are being inserted into the list, this
    #sorting function goes through and performs a basic sort based on
    #the tree height at a given node. This function is ALSO recursive, so it
    #processes nodes' inputs into previous nodes right up the tree. However,
    #the function above performs the full balance
    def recurse_reorder(self, node):
        
        if node != None:
                
            
                #Create two integers to iterate with
                temp_l_traverse = self.recurse_reorder(node.left)
                temp_r_traverse = self.recurse_reorder(node.right)
                #Special check used to find the correct node when using a recursive call
                if (self.right_check == True and node.data == self.right_order.prior.data):
                    
                    node.right = self.right_order
                        
                    self.right_check = False
                #Similar to the one above
                if (self.left_check == True and node.data == self.left_order.prior.data):
                    
                    node.left = self.left_order
                    
                    self.left_check = False
                    
                #Similar traversal mechanism as with other recursive functions
                if(temp_l_traverse == (temp_r_traverse - 2) and self.__len__() >= 3):
                    if(temp_r_traverse == 2):
                        #Checks if a node has a right-right node that needs to
                        #be reorganized
                        if(node.right.right != None):
                            #Create temporary nodes, set data accordingly
                            temp_node = node
                            
                            new_node = TreeNode(temp_node.right.data)  
                            
                            node = new_node
                            
                            if temp_node.data == self.head.data:
                                self.head = node
                                self.head.left = temp_node
                            
                            node.right = temp_node.right.right
                            node.left = temp_node
                            
                            #This function is used for flagging the next upcalled
                            #node
                            if(temp_node.prior != None):
                                spec_node = TreeNode(node.data)
                                temp_node.prior.right = spec_node
                                node.prior = temp_node.prior
                                self.right_check = True
                                self.right_order = node
                            
                            #Clear out any node data that may exist
                            node.left.right.right = None
                            node.left.right = None
                            temp_node = None
                        
                        #Similar traversal and node swapping excpet for right-left case
                        if(node.right.left != None):
                            temp_node = node
                            
                            new_node = TreeNode(temp_node.right.left.data)
                            
                            node = new_node
                            
                            if temp_node.data == self.head.data:
                                self.head = node
     
                            node.right = temp_node.right
                            node.left = temp_node
         
                            if(temp_node.prior != None):
                                spec_node = TreeNode(node.data)
                                temp_node.prior.right = spec_node
                                node.prior = temp_node.prior
                                self.right_check = True
                                self.right_order = node
                            
                            node.right.left = None
                            node.left.right = None
                            temp_node = None
                
                #This time we traverse the left side for a small reorder
                if(temp_r_traverse == (temp_l_traverse - 2) and self.__len__() >= 3):
                    if(temp_l_traverse == 2):
                        if(node.left.left != None):
                            
                            temp_node = node
                            
                            new_node = TreeNode(temp_node.left.data)
                            
                            node = new_node
                            
                            if temp_node.data == self.head.data:
                                self.head = node
                                
                                
                            node.left = temp_node.left.left
                            node.right = temp_node
                                
                            #All the same stuff just flipped for the left side
                            if(temp_node.prior != None):
                                spec_node = TreeNode(node.data)
                                temp_node.prior.left = spec_node
                                node.prior = temp_node.prior
                                self.left_check = True
                                self.left_order = node
                                 
                            node.right.left.left = None
                            node.right.left = None
                            temp_node = None
                            
                        #Checks to see if we have the case of right-left node
                        if(node.left.right != None):
                            
                            temp_node = node
                            
                            new_node = TreeNode(temp_node.left.right.data)
                            
                            node = new_node
                            
                            if temp_node.data == self.head.data:
                                self.head = node
                            
                            node.left = temp_node.left
                            node.right = temp_node
                            
                            #Some crazy stuff here
                            if(temp_node.prior != None):
                                spec_node = TreeNode(node.data)
                                temp_node.prior.left = spec_node
                                node.prior = temp_node.prior
                                self.left_check = True
                                self.left_order = node
                            
                            node.left.right = None
                            node.right.left = None
                            temp_node = None
                #Same recursive call used for determining relative node heights
                if temp_l_traverse > temp_r_traverse:
                    return 1 + temp_l_traverse
               
                else:
                    return 1 + temp_r_traverse
        
        else:
            return 0
        

    #The insert function, which acts as the driver for the other functions it calls
    #The insert function takes in a value, and processes it so that was the tree
    #is pre-balanced for any type of modifications/functions
    def insert(self, item):
       
        new_node = TreeNode(item)
        
        height = 0
        #Sets a new head node if there isn't one
        if self.head == None:
            self.root = new_node
            self.head = new_node
            return True
        #Restart the root at the head node before traversal every time
        self.root = self.head
        
        #While there is a root...
        while self.root != None:
            if((self.comp(self.root.data, new_node.data) == 0)):
                return False
            #Runs through and checks if there are nodes, if so, compares them,
            #sets a new node into a position where there is None
            if self.root.left != None and self.comp(new_node.data, self.root.data) == -1:
                self.root = self.root.left
                
            elif self.root.left == None and self.comp(new_node.data, self.root.data) == -1:
                self.root.left = new_node
                self.root.left.prior = self.root
                #Used for reordering after the insert
                height += self.recurse_reorder(self.head)
                self.big_balance(self.head)
            
                return True
                
            if self.root.right != None and self.comp(new_node.data, self.root.data) == 1:
                self.root = self.root.right
            elif self.root.right == None and self.comp(new_node.data, self.root.data) == 1:
                self.root.right = new_node
                self.root.right.prior = self.root
                #Once again, used for reordering. This time on the opposite side
                height += self.recurse_reorder(self.head)
                self.big_balance(self.head)
                      
                return True
            
        return False
            
    #This is a powerful recursive function that detects and item within a tree
    #and deletes it if it is found. The key here is to reorder (balance) the tree after
    #every node removal. However, with the last three nodes, they can be removed
    #using only the head node
    def remove_recurse(self, node, item):
        
        if(node != None):
            #Once again, same recursive format
            left_recurse = self.remove_recurse(node.left, item)
            right_recurse = self.remove_recurse(node.right, item)
            #Runs through and checks for the root_check flag. Performs operations
            #if True
            if self.root_check == True:
                if(self.comp(self.rem_reorder.data, node.data) == 1):
                    
                    if(self.none_check == True):
                        #Check if the node we're looking for matches the
                        #previously deleted node's prior node. This is important
                        #for finding the correct position to reorder the tree
                        if(node.data == self.rem_reorder.prior.data):
                            node.right = None
                            self.root_check = False
                            self.none_check = False
                            
                        elif(node.data == self.rem_reorder.prior.prior.data):
                            node.right = self.rem_reorder
                            
                            special_node = TreeNode(node.data)
                            node.right.prior = special_node
                            
                            self.root_check = False
                            self.remove_check = True
                    else:
                        if(node.data == self.rem_reorder.prior.data):
                            node.right = self.rem_reorder
                            self.root_check = False
                            self.remove_check = True
                            
                #Does the exact same thing as the above code except for the left
                #side
                if(self.comp(self.rem_reorder.data, node.data) == -1):
                    
                    if(self.none_check != True): 
                        if(node.data == self.rem_reorder.prior.data):
                            node.left = self.rem_reorder
                            self.root_check = False
                            self.remove_check = True
                            
                        elif(node.data == self.rem_reorder.prior.prior.data):
                            node.left = self.rem_reorder
                            
                            special_node = TreeNode(node.data)
                            node.left.prior = special_node
                            
                            self.root_check = False
                            self.remove_check = True
                        
                    else:
                        if(node.data == self.rem_reorder.prior.data):
                            node.left = None
                            self.root_check = False
                            self.remove_check = True
                            self.none_check = False
                        

            #This checks for a match between the node we want to delete and
            #all the current nodes in the tree
            if(self.comp(node.data, item) == 0):
                self.match_check = True
                #Four possible deletion cases. With no children
                if(node.left == None and node.right == None):
                    if(item == self.head.data):
                        #self.head == None
                        self.remove_check = True
                        self.head_remove_check = True
                   
                    if(node.data != self.head.data):
                        temp_node = node
                        self.root_check = True
                        self.rem_reorder = node
                        self.none_check = True
                        
                #With a left child
                if(node.left != None and node.right == None):
                    self.root_check = True
                    self.none_check = False
                    temp_node = node
                    node = temp_node.left
                    self.rem_reorder = node
                    
                #With a right child
                if(node.right != None and node.left == None):
                        if(self.__len__() == 2):
                            self.head = self.head.right
                            self.remove_check = True
                        self.root_check = True
                        self.none_check = False
                        temp_node = node
                        node = temp_node.right
                        self.rem_reorder = node
                        
                #With two children
                if(node.left != None and node.right != None):
                    self.root_check = True
                    self.none_check = False
                    temp_node = node
                    #Perform a special check for head node
                    if(node.data == self.head.data):
                        node = temp_node.right
                        node.left = temp_node.right
                        self.rem_reorder = node
                    
                    else:
                        node = temp_node.right
                        node.left = temp_node.left
                        self.rem_reorder = node
                        
            if(self.__len__() == 1):
                if(self.head_remove_check == True):
                    self.head = None
                    self.final_rem_check = True
                    return self.final_rem_check
                else:
                    self.final_rem_check = False
            
            #More edge-case checking
            if(node.data == self.head.data and node.data != item): 
                if(self.remove_check == True):
                    if(self.head_remove_check == True):
                        self.head = None
                    self.final_rem_check = True
                    self.remove_check = False
                else:
                    self.final_rem_check = False
            
            if(node.left):
                return 0 + self.remove_recurse(node.left, item)
            if(node.right):
                return 0 + self.remove_recurse(node.right, item)
            if(node.right and node.left):
                return left_recurse + right_recurse
            if(node.left == None):
                return 0
            if(node.right == None):
                return 0
       
        else:
            if(self.__len__() == 0):
                return False
            return 0
        
    #The driver for the recurse_remove function, as well as a specialty
    #function that handles the last 3 nodes in a tree (for removing)
    def remove(self, item):
        if(self.head != None):
          
            #We have to throw the head-node into a recursive, remove function
            self.remove_recurse(self.head, item)
            #Followed by a small balance after deleting a node
            self.recurse_reorder(self.head)
            #Followed by a bigger balance after doing a smaller balance
            self.big_balance(self.head)
            
            
            #This is a special if statement that tracks the total number of
            #nodes in the tree. If there are three nodes, re-create the tree
            #The reason for this is so that the prior node pointers are properly
            #reset on all nodes, which makes balancing and further node removal
            #possible
            if(self.__len__() == 3):
                self.recurse(self.head)
                self.head = None
                for item in self.test_list:
                    self.insert(item)
                self.test_list = []
            
            
            return self.final_rem_check
        else:
            return False

    
    #This is a recursive function used to find a specific value within
    #the tree
    def find_recurse(self, node, item):
        
        if node != None:
            
            if(self.comp(node.data, item) == 0):
                return True
            
            if(node.left != None):
                if(self.comp(item, node.data) == -1):
                    return self.find_recurse(node.left, item)
                    
            if(node.right != None):
                if(self.comp(item, node.data) == 1):
                    return self.find_recurse(node.right, item)
            
        else:
            return False
        
    #This is the driver function for the find_recurse function
    def __contains__(self, item):
        val_check = False
        if(self.head != None):
            val_check = self.find_recurse(self.head, item)
            
        return val_check
    
    #This is the first_recurse function, it returns the smallest node in
    #the tree
    def first_recurse(self, node):
        if(node != None):
            
            l_recurse = self.first_recurse(node.left)
            r_recurse = self.first_recurse(node.right)
            
            if(self.first_val == None):
                self.first_val = node.data
            if(self.comp(node.data, self.first_val) == -1):
                self.first_val = node.data
            if(node.left):
                return 0 + self.first_recurse(node.left)
            if(node.right):
                return 0 + self.first_recurse(node.right)
            if(node.right and node.left):
                return l_recurse + r_recurse
            
            if(node.left == None):
                return 0
            if(node.right == None):
                return 0
        else:
            return 0
        
    #This is the driver function for first_recurse
    def first(self):
        if(self.head != None):
            self.first_recurse(self.head)
            return self.first_val
        else:
            raise KeyError
      
    #This function find the largest element in the tree
    def last_recurse(self, node):
        if(node != None):
            
            l_recurse = self.last_recurse(node.left)
            r_recurse = self.last_recurse(node.right)
            
            if(self.last_val == None):
                self.last_val = node.data
            if(self.comp(node.data, self.last_val) == 1):
                self.last_val = node.data
            if(node.left):
                return 0 + self.last_recurse(node.left)
            if(node.right):
                return 0 + self.last_recurse(node.right)
            if(node.right and node.left):
                return l_recurse + r_recurse
            
            if(node.left == None):
                return 0
            if(node.right == None):
                return 0
        else:
            return 0

    #This is the driver function for last_recurse
    def last(self):
        if(self.head != None):
            self.last_recurse(self.head)
        
            return self.last_val
        else:
            raise KeyError
            
    #This is a recursive function for clearing out all nodes (except the head)
    #within a tree
    def clear_recurse(self, node):
        
        if node != None:
            
            self.clear_recurse(node.left)
            self.clear_recurse(node.right)
            
            node.left = None
            node.right = None
            
        else:
            return 0
        
            
            
    #This is the driver function for the clear_recurse function
    def clear(self):
        self.clear_recurse(self.head)
        self.head = None
        pass


        
    #This is the iterator function: Currently, it does nothing
    def __iter__(self):
        return iter([])

    # Pre-defined methods

    def is_empty(self):
        """
        Determines whether the set is empty
        :return: False if the set contains no items, True otherwise
        """
        return len(self) == 0

    def __repr__(self):
        """
        Creates a string representation of this set using an in-order traversal.
        :return: A string representing this set
        """
        return 'TreeSet([{0}])'.format(','.join(str(item) for item in self))

    # Helper functions
    # You can add additional functions here

class TreeNode:
    """
    A TreeNode to be used by the TreeSet
    """
    def __init__(self, data):
        """
        Constructor
        You can add additional data as needed
        :param data:
        """
        self.data = data
        self.left = None
        self.right = None
        self.prior = None
        # added stuff below

    def __repr__(self):
        """
        A string representing this node
        :return: A string
        """
        return 'TreeNode({0})'.format(self.data)

