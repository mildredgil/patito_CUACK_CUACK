from collections import deque


# set the size of the queue
q = deque() 
  
# qsize() give the maxsize of the Queue  


# Adding elements
q.append('a') 
q.append('b') 
q.append('c')
q.append('d') 
q.append('e') 
  
# Removing element from Queue 
print("\nElements deQueued from the Queue") 
print(q.pop()) 
print(q.pop()) 
print(q.pop()) 
  
#https://docs.python.org/2/library/collections.html