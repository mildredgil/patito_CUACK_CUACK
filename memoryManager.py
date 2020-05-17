from memoryConstants import *
from err import *

class memoryManager():
    def __init__(self):
        self.globalInt       = GLOBAL_INT
        self.globalFloat     = GLOBAL_FLOAT
        self.globalChar      = GLOBAL_CHAR
        self.globalTempInt   = GLOBAL_TEMPINT
        self.globalTempFloat = GLOBAL_TEMPFLOAT
        self.globalTempChar  = GLOBAL_TEMPCHAR
        self.globalTempBool  = GLOBAL_TEMPBOOL
        self.localInt        = LOCAL_INT
        self.localFloat      = LOCAL_FLOAT
        self.localChar       = LOCAL_CHAR
        self.localTempInt    = LOCAL_TEMPINT
        self.localTempFloat  = LOCAL_TEMPFLOAT
        self.localTempChar   = LOCAL_TEMPCHAR
        self.localTempBool   = LOCAL_TEMPBOOL
        self.constInt        = CONST_INT
        self.constFloat      = CONST_FLOAT
        self.constChar       = CONST_CHAR
        self.constString     = CONST_STRING
    
##########################################################        

    def getGlobalInt(self):
        self.globalInt = self.globalInt + 1
        return self.globalInt - 1
    
    def getGlobalFloat(self):
        self.globalFloat = self.globalFloat + 1
        return self.globalFloat - 1

    def getGlobalChar(self):
        self.globalChar = self.globalChar + 1
        return self.globalChar - 1

    def getGlobalTempInt(self):
        self.globalTempInt = self.globalTempInt + 1
        return self.globalTempInt - 1
    
    def getGlobalTempFloat(self):
        self.globalFloat = self.globalFloat + 1
        return self.globalFloat - 1

    def getGlobalTempChar(self):
        self.globalTempChar = self.globalTempChar + 1
        return self.globalTempChar - 1

    def getGlobalTempBool(self):
        self.globalTempBool = self.globalTempBool + 1
        return self.globalTempBool - 1
    
##########################################################

    def resetTemp(self):
        self.localInt        = LOCAL_INT
        self.localFloat      = LOCAL_FLOAT
        self.localChar       = LOCAL_CHAR
        self.localTempInt    = LOCAL_TEMPINT
        self.localTempFloat  = LOCAL_TEMPFLOAT
        self.localTempChar   = LOCAL_TEMPCHAR
        self.localTempBool   = LOCAL_TEMPBOOL
        
    def getLocalInt(self):
        self.localInt = self.localInt + 1
        return self.localInt - 1
    
    def getLocalFloat(self):
        self.localFloat = self.localFloat + 1
        return self.localFloat - 1

    def getLocalChar(self):
        self.localChar = self.localChar + 1
        return self.localChar - 1

    def getLocalTempInt(self):
        self.localTempInt = self.localTempInt + 1
        return self.localTempInt - 1
    
    def getLocalTempFloat(self):
        self.localFloat = self.localFloat + 1
        return self.localFloat - 1

    def getLocalTempChar(self):
        self.localTempChar = self.localTempChar + 1
        return self.localTempChar - 1

    def getLocalTempBool(self):
        self.localTempBool = self.localTempBool + 1
        return self.localTempBool - 1

##########################################################

    def getConstInt(self):
        self.constInt = self.constInt + 1
        return self.constInt - 1
    
    def getConstFloat(self):
        self.constFloat = self.constFloat + 1
        return self.constFloat - 1

    def getConstChar(self):
        self.constChar = self.constChar + 1
        return self.constChar - 1

    def getConstString(self):
        self.constString = self.constString + 1
        return self.constString - 1

##########################################################      

    def get(self, memType):
        funcSwitcher={
                'GLOBAL_INT'       : self.getGlobalInt,
                'GLOBAL_FLOAT'     : self.getGlobalFloat,
                'GLOBAL_CHAR'      : self.getGlobalChar,
                'GLOBAL_TEMPINT'   : self.getGlobalTempInt,
                'GLOBAL_TEMPFLOAT' : self.getGlobalTempFloat,
                'GLOBAL_TEMPCHAR'  : self.getGlobalTempChar,
                'GLOBAL_TEMPBOOL'  : self.getGlobalTempBool,
                'LOCAL_INT'        : self.getLocalInt,
                'LOCAL_FLOAT'      : self.getLocalFloat,
                'LOCAL_CHAR'       : self.getLocalChar,
                'LOCAL_TEMPINT'    : self.getLocalTempInt,
                'LOCAL_TEMPFLOAT'  : self.getLocalTempFloat,
                'LOCAL_TEMPCHAR'   : self.getLocalTempChar,
                'LOCAL_TEMPBOOL'   : self.getLocalTempBool,
                'CONST_INT'        : self.getConstInt,
                'CONST_FLOAT'      : self.getConstFloat,
                'CONST_CHAR'       : self.getConstChar,
                'CONST_STRING'     : self.getConstString,
            }
        func = funcSwitcher.get(memType, "Invalid Memory Type")

        constSwitcher={
                'GLOBAL_INT'       : GLOBAL_INT,
                'GLOBAL_FLOAT'     : GLOBAL_FLOAT,
                'GLOBAL_CHAR'      : GLOBAL_CHAR,
                'GLOBAL_TEMPINT'   : GLOBAL_TEMPINT,
                'GLOBAL_TEMPFLOAT' : GLOBAL_TEMPFLOAT,
                'GLOBAL_TEMPCHAR'  : GLOBAL_TEMPCHAR,      
                'GLOBAL_TEMPBOOL'  : GLOBAL_TEMPBOOL,       
                'LOCAL_INT'        : LOCAL_INT,
                'LOCAL_FLOAT'      : LOCAL_FLOAT,    
                'LOCAL_CHAR'       : LOCAL_CHAR,  
                'LOCAL_TEMPINT'    : LOCAL_TEMPINT,
                'LOCAL_TEMPFLOAT'  : LOCAL_TEMPFLOAT,
                'LOCAL_TEMPCHAR'   : LOCAL_TEMPCHAR,      
                'LOCAL_TEMPBOOL'   : LOCAL_TEMPBOOL,       
                'CONST_INT'        : CONST_INT,
                'CONST_FLOAT'      : CONST_FLOAT,
                'CONST_CHAR'       : CONST_CHAR,  
                'CONST_STRING'     : CONST_STRING
            }
        
        const = constSwitcher.get(memType, "Invalid Memory Type")
        mem = func()

        if mem - const >= 1000:
            notEnoughMem()
        else:
            return mem