class Heap:
    """
    A heap-based priority queue
    Items in the queue are ordered according to a comparison function
    """

    def __init__(self, comp):
        """
        Constructor
        :param comp: A comparison function determining the priority of the included elements
        """
        self.comp = comp
        #Set up some basic initializers
        self.size = 0
        #Woo list!
        self.heap_array = []
        # Added Members

    #Len function returns the length of the list.
    #Ironically, you can use the lists' len feature
    #to return the len for the heap
    def __len__(self):
        return len(self.heap_array)

    #Peek function looks at the first element of the heap,
    #Which is either max or min depending on the ordering
    def peek(self):
        if self.heap_array:
            self.heaped_up(self.heap_array, 0)
            return self.heap_array[0]
        else:
            raise IndexError

    #Insert function, inserts element into heap
    def insert(self, item):
        #If there isn't an array, make one and increment
        #the size counter
        if not self.heap_array:
            self.size += 1
            self.heap_array.append(item)
        #If thre is an array...
        else:
            #Increment a value into the heap that will be destroyed
            #such as -1 (because our heaps only have positive input)
            self.heap_array.append(-1)
            self.size += 1
            index = self.size - 1
            
            #Runs through the loop and performs a bit of sorting
            while index > 0 and item < self.heap_array[index//2]:
                self.heap_array[index] = self.heap_array[index//2]
                index = (index)//2
                
            self.heap_array[index] = item
            
            #Completely sort from the ground up
            element = (self.size)//2
            while(element>=1):
                self.heaped_up(self.heap_array, element)
                element-=1
            
            
    #This is the heapify function with a cooler name
    def heaped_up(self, heap, index):
        #Gather left and right children nodes
        left = index * 2
        right = (index * 2) + 1
        #Use comparison function to determine which kind of heap to make
        #Then set that value to the left child of the indexed node
        if left < len(heap) and self.comp(heap[left],heap[index]):
            val = left
        #Otherwise, use the index as the value
        else:
            val = index
        #Similar to the left child
        if right < len(heap) and self.comp(heap[right],heap[val]):
            val = right
        #If the current value and the indexed value don't match, swap
        #Then, sue recursion to fully sort
        if val != index:
            heap[index], heap[val] = heap[val], heap[index]
            self.heaped_up(heap, val)
        
        
    #Extracts a data element from the heap
    def extract(self):
        if not self.heap_array:
            raise IndexError
            
        else:
            #Set the value to be extracted to the first node of the heap
            val = self.heap_array[0]
            #put the current node at the end of the heap
            self.heap_array[0] = self.heap_array[-1]
            #Decrement the size
            self.size -= 1;
            #Pop the value off the end
            self.heap_array.pop()
            #Re-Heap due to inordering after movement of elements
            self.heaped_up(self.heap_array, 0)
            
            return val

    #Crams a whole list into the heap
    def extend(self, seq):
        #Add the new sequence to the heap
        self.heap_array += seq
        
        #Run through a loop and sort all of the elements
        element = (len(self.heap_array))//2
        while(element >= 0):
            self.heaped_up(self.heap_array, element)
            element-=1

    #Clear function removes all data from the heap
    def clear(self):
        
        self.heap_array = []
        self.size = 0
        pass

    #Iterator, iterates through the heap
    def __iter__(self):
        for element in self.heap_array:
            yield element

    # Supplied methods

    def __bool__(self):
        """
        Checks if this heap contains items
        :return: True if the heap is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks if this heap is empty
        :return: True if the heap is empty
        """
        return len(self) == 0

    def __repr__(self):
        """
        A string representation of this heap
        :return:
        """
        return 'Heap([{0}])'.format(','.join(str(item) for item in self))

    # Added methods


# Required Non-heap member function

#A function used to find the median of a heap
def find_median(seq):
    """
    Finds the median (middle) item of the given sequence.
    Ties are broken arbitrarily.
    :param seq: an iterable sequence
    :return: the median element
    """
    if not seq:
        raise IndexError
    min_heap = Heap(lambda a, b: a <= b)
    #Forgive me, but I didn't know if we were supposed
    #to implement both heaps. I figured either or would
    #do, because the median is the median regardless of
    #the heap ordering for min or max
    #max_heap = Heap(lambda a, b: a >= b)
  
    #Add the sequence to the heap
    min_heap.extend(seq)
    
    #Run through the heap and extract all elements up to 
    #the halfway mark. If it is an even list, either
    #median works (for the context of this assignment)
    size = len(min_heap)//2
    index = 0
    while(index <= size):
        med = min_heap.extract()
        index += 1
        
    return med
