from memoryConstants import *
from err import *

class MemoryManager():
    def __init__(self):
        self.memCounters = memBase

    def resetTemp(self):
        self.memCounters['LOCAL_INT']                = LOCAL_INT
        self.memCounters['LOCAL_FLOAT']              = LOCAL_FLOAT
        self.memCounters['LOCAL_CHAR']               = LOCAL_CHAR
        self.memCounters['LOCAL_TEMP_INT']           = LOCAL_TEMP_INT
        self.memCounters['LOCAL_TEMP_FLOAT']         = LOCAL_TEMP_FLOAT
        self.memCounters['LOCAL_TEMP_CHAR']          = LOCAL_TEMP_CHAR
        self.memCounters['LOCAL_TEMP_BOOL']          = LOCAL_TEMP_BOOL
        self.memCounters['LOCAL_TEMP_POINTER_INT']   = LOCAL_TEMP_POINTER_INT
        self.memCounters['LOCAL_TEMP_POINTER_FLOAT'] = LOCAL_TEMP_POINTER_FLOAT
        self.memCounters['LOCAL_TEMP_POINTER_CHAR']  = LOCAL_TEMP_POINTER_CHAR
   
    def get(self, memType, size=None):
        if size:
            mem = self.exist(memType)
            self.memCounters[memType] += size
            self.validate(memType, self.memCounters[memType])
            return mem
        return self.exist(memType)

    def setNext(self, memType, size):
        self.exist(memType)
        self.memCounters[memType] += size
        self.validate(memType, self.memCounters[memType])
    
    def exist(self, memType):
        m = self.memCounters.get(memType, None)
        if m != None:
            return m
        else: 
            invalidMemType(memType)

    def validate(self, memType, newMemType):
        if newMemType - memBase[memType] >= 1000:
            notEnoughMem()