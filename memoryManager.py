class memoryManager():
    def __init__(self):
        self.globalInt=0
        self.globalFloat=1000
        self.globalChar=2000
        self.globalTempInt=3000
        self.globalTempFloat=4000
        self.globalTempChar=5000
        self.globalTempBool=6000
        self.localInt=7000
        self.localFloat=8000
        self.localChar=9000
        self.localTempInt=10000
        self.localTempFloat=11000
        self.localTempChar=12000
        self.localTempBool=13000
        self.constInt=14000
        self.constFloat=15000
        self.constChar=16000
        self.constString=17000
    
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
        self.localInt=7000
        self.localFloat=8000
        self.localChar=9000
        self.localTempInt=10000
        self.localTempFloat=11000
        self.localTempChar=12000
        self.localTempBool=13000

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
