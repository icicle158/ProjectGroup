# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 21:51:30 2018

@author: Avery
"""

def recurse_reorder(self, node):
        
        if node != None:
            
                
        
       
                temp_l_traverse = self.recurse_reorder(node.left)
                temp_r_traverse = self.recurse_reorder(node.right)
                
                if (self.test_check == True):
                    print("HALLO")
                    print(node.data)
                    node.right = self.test
                    self.test_check = False
                    
                
                if temp_l_traverse == 2 and temp_r_traverse == 4:
                    
                
                if temp_l_traverse == 2 and temp_r_traverse == 0:
                    
                    if(node.left.left != None):
                        temp_node = node
                        node = temp_node.left
                        
                        if temp_node.data == self.head.data:
                            self.head = node
                        
                        node.left = temp_node.left.left
                        node.right = temp_node
                        node.right.left = None
                        temp_node = None
                        
                    if(node.left.right != None):
                        temp_node = node
                        node = temp_node.left.right
                        
                        if temp_node.data == self.head.data:
                            self.head = node
                        
                        node.left = temp_node.left
                        node.left.right = None
                        node.right = temp_node
                        node.right.left = None
                        temp_node = None
                        
                        
                if(temp_l_traverse == (temp_r_traverse - 2) and temp_l_traverse != 2):
                    temp_node = node
                    temp_node_spec = temp_node.right.left
                    node = temp_node.right
                    node.left = temp_node
                    node.left.right = temp_node_spec
                    
                    
                if temp_l_traverse == 0 and temp_r_traverse == 2:
                    if(node.right.right != None):
                        
 
                        temp_node = node
                        
                        #COPY THESE THINGS INTO OTHER 3
                        new_node = TreeNode(temp_node.right.data)  
                        
                        node = new_node
                        
                        if temp_node.data == self.head.data:
                            self.head = node
                        
                        node.right = temp_node.right.right
                        node.left = temp_node
                        
                        #Some crazy stuff here
                        if(temp_node.prior != None):
                            temp_node.prior.right = node
                            node.prior = temp_node.prior
                            self.test_check = True
                            
                            
                            #Will be renamed to :  self.small_reorder
                            self.test = node
                            
                            print("I ACTUALLY FOUND IT: ", temp_node.prior.right)
                            print(temp_node.prior)
                        
                        
                        node.left.right.right = None
                        node.left.right = None
                        temp_node = None
                        
                        
                    if(node.right.left != None):
                        temp_node = node
                        node = temp_node.right.left
                        
                        if temp_node.data == self.head.data:
                            self.head = node
                        
                        node.right = temp_node.right
                        node.right.left = None
                        node.left = temp_node
                        node.left.right = None
                        temp_node = None
                        
                
                print("ltrav: ", temp_l_traverse)
                print("rtrav: ", temp_r_traverse)
                print(node.data)
                
                if node.right:
                    print("right node data: ", node.right.data)
                
                if temp_l_traverse > temp_r_traverse:
                    print("ONE LEFT TRAVERSAL")
                    return 1 + temp_l_traverse
               
                else:
                    print("ONE RIGHT TRAVERSAL")
                    return 1 + temp_r_traverse
          
            
        
        else:
            return 0