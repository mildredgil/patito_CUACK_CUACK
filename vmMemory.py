#POSITION IN MEM INFO
SCOPE = 0
ISTEMP = 1
ISPOINTER = 2
TYPE = 3

#TO ACCESS memory structs
#scope
GLOBAL = 0
LOCAL = 1
CONST = 2

NO_TEMP = 0
TEMP = 1

NO_POINTER = 0
POINTER = 1

INT = 0
FLOAT = 1
CHAR = 2
BOOL = 3
STRING = 3

MEM_INFO = [  
    [GLOBAL, NO_TEMP, NO_POINTER, INT],
    [GLOBAL, NO_TEMP, NO_POINTER, FLOAT],
    [GLOBAL, NO_TEMP, NO_POINTER, CHAR],
    [GLOBAL, TEMP,    NO_POINTER, INT],
    [GLOBAL, TEMP,    NO_POINTER, FLOAT],
    [GLOBAL, TEMP,    NO_POINTER, CHAR],
    [GLOBAL, TEMP,    NO_POINTER, BOOL],
    [GLOBAL, TEMP,    POINTER,    INT],
    [GLOBAL, TEMP,    POINTER,    FLOAT],
    [GLOBAL, TEMP,    POINTER,    CHAR],
    [LOCAL,  NO_TEMP, NO_POINTER,  INT],
    [LOCAL,  NO_TEMP, NO_POINTER,  FLOAT],
    [LOCAL,  NO_TEMP, NO_POINTER,  CHAR],
    [LOCAL,  TEMP,    NO_POINTER,  INT],
    [LOCAL,  TEMP,    NO_POINTER,  FLOAT],
    [LOCAL,  TEMP,    NO_POINTER,  CHAR],
    [LOCAL,  TEMP,    NO_POINTER,  BOOL],
    [LOCAL,  TEMP,    POINTER,     INT],
    [LOCAL,  TEMP,    POINTER,     FLOAT],
    [LOCAL,  TEMP,    POINTER,     CHAR],
    [CONST,  NO_TEMP, NO_POINTER,  INT],
    [CONST,  NO_TEMP, NO_POINTER,  FLOAT],
    [CONST,  NO_TEMP, NO_POINTER,  CHAR],
    [CONST,  NO_TEMP, NO_POINTER,  STRING]
]

class MemoryStruct():
    @classmethod
    def constStruct(self):
        const_struct = [
            [
                [{},{},{},{}],      #CONST_NO_TEMP_NO_POINTER
            ],
        ]
        return const_struct

    @classmethod
    def localStruct(self):
        local_struct = [
            [
                [{},{},{}]          #LOCAL_NO_TEMP_NO_POINTER
            ],
            [
                [{},{},{},{}],      #LOCAL_TEMP_NO_POINTER
                [{},{},{}]          #LOCAL_TEMP_POINTER
            ],
        ]
        return local_struct

    @classmethod
    def globalStruct(self):
        global_struct = [
            [
                [{},{},{}]          #GLOBAL_NO_TEMP_NO_POINTER
            ],
            [
                [{},{},{},{}],      #GLOBAL_TEMP_NO_POINTER
                [{},{},{}]          #GLOBAL_TEMP_POINTER
            ],
        ]
        return global_struct
    