'''
Author: Avery Berninger
Date: 1/26/2018
Time: 1:40A.M.
'''  


  
def order_first_name(a, b):
    """
    Orders two people by their first names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    #Case checking for a string
    if isinstance(a, str):
        if isinstance(b, str):
            if a < b:
                return True
            elif a == b:
                if a.last <= b.last:
                    return True
                else:
                    return False
            else:
                return False
    
    #Case checking for the object of a function
    if a.first < b.first:
        return True
    elif a.first == b.first:
        if a.last <= b.last:
            return True
        else:
            return False
    else:
        return False
    
def order_last_name(a, b):
    """
    Orders two people by their last names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    #Case checking for a string
    if isinstance(a, str):
        if isinstance(b, str):
            if a < b:
                return True
            elif a == b:
                if a.first <= b.first:
                    return True
                else:
                    return False
            else:
                return False
            
    #Case checking for the object of a function
    if a.last < b.last:
        return True
    elif a.last == b.last:
        if a.first <= b.first:
            return True
        else:
            return False
    else:
        return False
   

def is_alphabetized(roster, ordering):
    """
    Checks whether the roster of names is alphabetized in the given order
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: True if the roster is alphabetized and False otherwise
    """
    
    #A loop used to quickly check through people in the roster
    person2 = 1
    for person in roster:
        if person2 >= len(roster):
                break
        if ordering(person, roster[person2]) == False: 
            return False
        person2 += 1
    return True
    
def alphabetize(roster, ordering):
    """
    Alphabetizes the roster according to the given ordering
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: a sorted version of roster
    :return: the number of comparisons made
    """
    
    #Used to determine the length of the list
    member_cnt = len(roster)
    
    
    #Preparing for a merge-sort by splitting the roster (list)
    #into two separate lists divided roughly in half
    roster_pt1 = roster[:int(member_cnt/2)]
    roster_pt2 = roster[int(member_cnt/2):]
    
    #Calls check_swap function to order two smaller lists
    check_swap(roster_pt1, ordering)
    check_swap(roster_pt2, ordering)

    #Finally, merge the two smaller lists with the merge function
    merged_list = merge(roster_pt1, roster_pt2, ordering)

    return (merged_list, 0)

#Sorts a list by checking current person and neighbor
#then swapping if the neighbor comes before the current person
#Runs recursively
def check_swap(roster, ordering):
    person1 = 0
    person2 = 1
    sorted_list = True
    
    for person in roster:
        if person2 > len(roster)-1:
                break
        #Either a simple check and swap...
        if ordering(person, roster[person2]) == False:
            switcheroo(roster, person1, person2)
            sorted_list = False
        #Or a pass
        else:
            pass
        person2 += 1
        person1 += 1
    
    if sorted_list == False:
        roster = check_swap(roster, ordering)
    
#Performs the actual switching in the list
#The ol' switcheroo
def switcheroo(roster, x, y):
    roster[x], roster[y] = roster[y], roster[x]
    
#Used for the actual merging of two separate lists
def merge(list_a, list_b, ordering):
    merged_list = []
    iter1 = 0
    iter2 = 0
    #Merge Formula
    while((iter1 < len(list_a)) and (iter2 < len(list_b))):
        if ordering(list_a[iter1], list_b[iter2]) == True:
            merged_list.append(list_a[iter1])
            iter1 += 1
        else:
            merged_list.append(list_b[iter2])
            iter2 += 1
    #If there's any elements remaining
    #append them to the rest of the list
    if iter1 < iter2:
        for item in list_a[iter1:]:    
            merged_list.append(item)
    else:
        for item in list_b[iter2:]:    
            merged_list.append(item)
            
    return merged_list
    
