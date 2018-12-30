
import collections



#Used to check if a subsequence exists within a sequence
def verify_subseq(seq, subseq):
    
    #Runs through the subsequence
    for element in subseq:
        
        #If that element doesn't exist in the sequence, return false
        if element not in seq:
            return False
    
    #If every element is in the sequence, return true
    return True 


#Checks to see if the sequence is in increasing order
def verify_increasing(seq):
    
    #If the length of the sequence is empty (0) or 1, the sequence is automatically
    #increasing by default (trivially)
    if (len(seq) == 0) or (len(seq) == 1):
        return True
    
    #If the sequence has a length greater than 1...
    if len(seq) > 1:
        
        #Run a loop with an index and if the sequence has an increasing
        #sequence for all indexes, return true
        i = 0
        while True:
            if (i+1) == len(seq):
                return True
                break
            
            if seq[i] >= seq[i+1]:
                return False
            
            i += 1
       
    #Otherwise, return false
    return False


#Used to find the longest common subsequence within a given sequence
def find_lis(seq):
    
    #Initialize lists, boolean variables
    seq_list = collections.deque()
    temp_list = []
    
    
    smallest_word = False
    biggest_word = False
    mid_word = False
    
    #Finds when the element in the sequence changes from greater to less than
    #the last element in a recorded list
    cmp_change_index = 0
    
    #This runs through all elements in the sequence...
    for element in seq:
        
        if seq_list:
            i = 0
            #Then it runs through all elements in a list that consists of 
            #recorded lists. 
            for word_list in seq_list:
           
                #If the elements are equal, move on
                if element == word_list[-1]:
                    mid_word = False
                    biggest_word = False
                    smallest_word = False
                    break
         
                
                #The principal is when an element is smaller than
                #the end element of all lists, a new list of size 1 is constructed
                if element < word_list[-1]:
                    smallest_word = True
                    
        
                    #If there is a change from biggest element to smallest element
                    #then this element exists in between two lists in the list of
                    #lists. Thus, take the next smallest list from this point,
                    #append the element to it, and replace any lists of the same
                    #size as the newly constructed list, with the new list
                    if biggest_word == True and (seq_list[i - 1][-1] < element):
                        mid_word = True
                        biggest_word = False
                        smallest_word = False
                        cmp_change_index = i
                        break
                    
                #If the element is larger than the end element of all constructed
                #lists, take the longest list and append the element to it. Then,
                #add it to the list of lists
                if element > word_list[-1]:
                    biggest_word = True
                    

                i += 1
            
            if biggest_word == True:
                temp = list(max(seq_list,key=len))
                temp.append(element)
                seq_list.append(temp)
                biggest_word = False
                smallest_word = False
                mid_word = False
                continue
                
            if smallest_word == True:
                seq_list.popleft()
                seq_list.appendleft([element])
                #del seq_list[1]
                smallest_word = False
                biggest_word = False
                mid_word = False
                continue
                
            if mid_word == True:
                copy_list = seq_list[cmp_change_index-1][:]
                copy_list.append(element)
                
                seq_list[cmp_change_index] = copy_list
                mid_word = False
                smallest_word = False
                biggest_word = False
                continue
            
        else:
            seq_list.append([element])

    #Finally, return the list with the largest length
    return max(seq_list, key=len)
