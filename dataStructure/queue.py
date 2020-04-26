from queue import Queue 
  
# set the size of the queue
q = Queue(maxsize = 5) 
  
# qsize() give the maxsize of the Queue  
print(q.qsize())

# Adding elements
q.put('a') 
q.put('b') 
q.put('c')
print(q.qsize())  
q.put('d') 
q.put('e') 
  
# Return Boolean for Full  
# Queue  
print("\nFull: ", q.full())  
  
# Removing element from queue 
print("\nElements dequeued from the queue") 
print(q.get()) 
print(q.get()) 
print(q.get()) 
  
# Return Boolean for Empty  
# Queue  
print("\nEmpty: ", q.empty()) 
  
q.put(1)
print("\nEmpty: ", q.empty())  
print("Full: ", q.full())
