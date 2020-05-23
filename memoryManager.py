from memoryConstants import *
from err import *

class MemoryManager():
    def __init__(self):
        self.globalInt       = GLOBAL_INT
        self.globalFloat     = GLOBAL_FLOAT
        self.globalChar      = GLOBAL_CHAR
        self.globalTempInt   = GLOBAL_TEMP_INT
        self.globalTempFloat = GLOBAL_TEMP_FLOAT
        self.globalTempChar  = GLOBAL_TEMP_CHAR
        self.globalTempBool  = GLOBAL_TEMP_BOOL
        self.globalTempIntP  = GLOBAL_TEMP_POINTER_INT
        self.globalTempFloatP= GLOBAL_TEMP_POINTER_FLOAT
        self.globalTempCharP = GLOBAL_TEMP_POINTER_CHAR
        self.localInt        = LOCAL_INT
        self.localFloat      = LOCAL_FLOAT
        self.localChar       = LOCAL_CHAR
        self.localTempInt    = LOCAL_TEMP_INT
        self.localTempFloat  = LOCAL_TEMP_FLOAT
        self.localTempChar   = LOCAL_TEMP_CHAR
        self.localTempBool   = LOCAL_TEMP_BOOL
        self.localTempIntP   = LOCAL_TEMP_POINTER_INT
        self.localTempFloatP = LOCAL_TEMP_POINTER_FLOAT
        self.localTempCharP  = LOCAL_TEMP_POINTER_CHAR
        self.constInt        = CONST_INT
        self.constFloat      = CONST_FLOAT
        self.constChar       = CONST_CHAR
        self.constString     = CONST_STRING
    
##########################################################        

    def getGlobalInt(self, size):
        self.globalInt = self.globalInt + size
        return self.globalInt - size
    
    def getGlobalFloat(self, size):
        self.globalFloat = self.globalFloat + size
        return self.globalFloat - size

    def getGlobalChar(self, size):
        self.globalChar = self.globalChar + size
        return self.globalChar - size

    def getGlobalTempInt(self, size):
        self.globalTempInt = self.globalTempInt + size
        return self.globalTempInt - size
    
    def getGlobalTempFloat(self, size):
        self.globalFloat = self.globalFloat + size
        return self.globalFloat - size

    def getGlobalTempChar(self, size):
        self.globalTempChar = self.globalTempChar + size
        return self.globalTempChar - size

    def getGlobalTempBool(self, size):
        self.globalTempBool = self.globalTempBool + size
        return self.globalTempBool - size
    
    def getGlobalTempIntP(self, size):
        self.globalTempIntP = self.globalTempIntP + size
        return self.globalTempIntP - size

    def getGlobalTempFloatP(self, size):
        self.globalTempTempFloatP = self.globalTempTempFloatP + size
        return self.globalTempTempFloatP - size

    def getGlobalTempCharP(self, size):
        self.globalTempCharP = self.globalTempCharP + size
        return self.globalTempCharP - size
##########################################################

    def resetTemp(self):
        self.localInt        = LOCAL_INT
        self.localFloat      = LOCAL_FLOAT
        self.localChar       = LOCAL_CHAR
        self.localTempInt    = LOCAL_TEMP_INT
        self.localTempFloat  = LOCAL_TEMP_FLOAT
        self.localTempChar   = LOCAL_TEMP_CHAR
        self.localTempBool   = LOCAL_TEMP_BOOL
        self.localTempIntP   = LOCAL_TEMP_POINTER_INT
        self.localTempFloatP = LOCAL_TEMP_POINTER_FLOAT
        self.localTempCharP  = LOCAL_TEMP_POINTER_CHAR
        
    def getLocalInt(self, size):
        self.localInt = self.localInt + size
        return self.localInt - size
    
    def getLocalFloat(self, size):
        self.localFloat = self.localFloat + size
        return self.localFloat - size

    def getLocalChar(self, size):
        self.localChar = self.localChar + size
        return self.localChar - size

    def getLocalTempInt(self, size):
        self.localTempInt = self.localTempInt + size
        return self.localTempInt - size
    
    def getLocalTempFloat(self, size):
        self.localTempFloat = self.localTempFloat + size
        return self.localTempFloat - size

    def getLocalTempChar(self, size):
        self.localTempChar = self.localTempChar + size
        return self.localTempChar - size

    def getLocalTempBool(self, size):
        self.localTempBool = self.localTempBool + size
        return self.localTempBool - size

    def getLocalTempIntP(self, size):
        self.localTempIntP = self.localTempIntP + size
        return self.localTempIntP - size
    
    def getLocalTempFloatP(self, size):
        self.localTempFloatP = self.localTempFloatP + size
        return self.localTempFloatP - size

    def getLocalTempCharP(self, size):
        self.localTempCharP = self.localTempCharP + size
        return self.localTempCharP - size

########################################################## 

    def getConstInt(self, size):
        self.constInt = self.constInt + size
        return self.constInt - size
    
    def getConstFloat(self, size):
        self.constFloat = self.constFloat + size
        return self.constFloat - size

    def getConstChar(self, size):
        self.constChar = self.constChar + size
        return self.constChar - size

    def getConstString(self, size):
        self.constString = self.constString + size
        return self.constString - size

##########################################################      

    def get(self, memType, size):
        funcSwitcher={
                'GLOBAL_INT'        : self.getGlobalInt,
                'GLOBAL_FLOAT'      : self.getGlobalFloat,
                'GLOBAL_CHAR'       : self.getGlobalChar,
                'GLOBAL_TEMP_INT'   : self.getGlobalTempInt,
                'GLOBAL_TEMP_FLOAT' : self.getGlobalTempFloat,
                'GLOBAL_TEMP_CHAR'  : self.getGlobalTempChar,
                'GLOBAL_TEMP_BOOL'  : self.getGlobalTempBool,
                'GLOBAL_TEMP_POINTER_INT'   : self.getGlobalTempIntP,
                'GLOBAL_TEMP_POINTER_FLOAT' : self.getGlobalTempFloatP,
                'GLOBAL_TEMP_POINTER_CHAR'  : self.getGlobalTempCharP,
                'LOCAL_INT'         : self.getLocalInt,
                'LOCAL_FLOAT'       : self.getLocalFloat,
                'LOCAL_CHAR'        : self.getLocalChar,
                'LOCAL_TEMP_INT'    : self.getLocalTempInt,
                'LOCAL_TEMP_FLOAT'  : self.getLocalTempFloat,
                'LOCAL_TEMP_CHAR'   : self.getLocalTempChar,
                'LOCAL_TEMP_BOOL'   : self.getLocalTempBool,
                'LOCAL_TEMP_POINTER_INT'    : self.getLocalTempIntP,
                'LOCAL_TEMP_POINTER_FLOAT'  : self.getLocalTempFloatP,
                'LOCAL_TEMP_POINTER_CHAR'   : self.getLocalTempCharP,
                'CONST_INT'         : self.getConstInt,
                'CONST_FLOAT'       : self.getConstFloat,
                'CONST_CHAR'        : self.getConstChar,
                'CONST_STRING'      : self.getConstString,
            }
        func = funcSwitcher.get(memType, "Invalid Memory Type")

        constSwitcher={
                'GLOBAL_INT'        : GLOBAL_INT,
                'GLOBAL_FLOAT'      : GLOBAL_FLOAT,
                'GLOBAL_CHAR'       : GLOBAL_CHAR,
                'GLOBAL_TEMP_INT'   : GLOBAL_TEMP_INT,
                'GLOBAL_TEMP_FLOAT' : GLOBAL_TEMP_FLOAT,
                'GLOBAL_TEMP_CHAR'  : GLOBAL_TEMP_CHAR,
                'GLOBAL_TEMP_BOOL'  : GLOBAL_TEMP_BOOL,       
                'GLOBAL_TEMP_POINTER_INT'   : GLOBAL_TEMP_POINTER_INT,
                'GLOBAL_TEMP_POINTER_FLOAT' : GLOBAL_TEMP_POINTER_FLOAT,
                'GLOBAL_TEMP_POINTER_CHAR'  : GLOBAL_TEMP_POINTER_CHAR,
                'LOCAL_INT'         : LOCAL_INT,
                'LOCAL_FLOAT'       : LOCAL_FLOAT,    
                'LOCAL_CHAR'        : LOCAL_CHAR,  
                'LOCAL_TEMP_INT'    : LOCAL_TEMP_INT,
                'LOCAL_TEMP_FLOAT'  : LOCAL_TEMP_FLOAT,
                'LOCAL_TEMP_CHAR'   : LOCAL_TEMP_CHAR,      
                'LOCAL_TEMP_BOOL'   : LOCAL_TEMP_BOOL,
                'LOCAL_TEMP_POINTER_INT'    : LOCAL_TEMP_POINTER_INT,
                'LOCAL_TEMP_POINTER_FLOAT'  : LOCAL_TEMP_POINTER_FLOAT,
                'LOCAL_TEMP_POINTER_CHAR'   : LOCAL_TEMP_POINTER_CHAR, 
                'CONST_INT'         : CONST_INT,
                'CONST_FLOAT'       : CONST_FLOAT,
                'CONST_CHAR'        : CONST_CHAR,  
                'CONST_STRING'      : CONST_STRING
            }
        
        const = constSwitcher.get(memType, "Invalid Memory Type")
        mem = func(size)
        
        if mem - const >= 1000:
            notEnoughMem()
        else:
            return mem