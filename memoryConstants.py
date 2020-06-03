#base constanst 
GLOBAL_INT=0
GLOBAL_FLOAT=10000
GLOBAL_CHAR=20000
GLOBAL_TEMP_INT=30000
GLOBAL_TEMP_FLOAT=40000
GLOBAL_TEMP_CHAR=50000
GLOBAL_TEMP_BOOL=60000
GLOBAL_TEMP_POINTER_INT=70000
GLOBAL_TEMP_POINTER_FLOAT=80000
GLOBAL_TEMP_POINTER_CHAR=90000

LOCAL_INT=100000
LOCAL_FLOAT=110000
LOCAL_CHAR=120000
LOCAL_TEMP_INT=130000
LOCAL_TEMP_FLOAT=140000
LOCAL_TEMP_CHAR=150000
LOCAL_TEMP_BOOL=160000
LOCAL_TEMP_POINTER_INT=170000
LOCAL_TEMP_POINTER_FLOAT=180000
LOCAL_TEMP_POINTER_CHAR=190000

CONST_INT=200000
CONST_FLOAT=210000
CONST_CHAR=220000
CONST_STRING=230000

MEM_GLOBAL = GLOBAL_INT
MEM_LOCAL = LOCAL_INT
MEM_CONST = CONST_INT
#################################################################################      
#get memBase Value
memBase={
    'GLOBAL_INT'                : GLOBAL_INT,
    'GLOBAL_FLOAT'              : GLOBAL_FLOAT,
    'GLOBAL_CHAR'               : GLOBAL_CHAR,
    'GLOBAL_TEMP_INT'           : GLOBAL_TEMP_INT,
    'GLOBAL_TEMP_FLOAT'         : GLOBAL_TEMP_FLOAT,
    'GLOBAL_TEMP_CHAR'          : GLOBAL_TEMP_CHAR,
    'GLOBAL_TEMP_BOOL'          : GLOBAL_TEMP_BOOL,       
    'GLOBAL_TEMP_POINTER_INT'   : GLOBAL_TEMP_POINTER_INT,
    'GLOBAL_TEMP_POINTER_FLOAT' : GLOBAL_TEMP_POINTER_FLOAT,
    'GLOBAL_TEMP_POINTER_CHAR'  : GLOBAL_TEMP_POINTER_CHAR,
    'LOCAL_INT'                 : LOCAL_INT,
    'LOCAL_FLOAT'               : LOCAL_FLOAT,    
    'LOCAL_CHAR'                : LOCAL_CHAR,  
    'LOCAL_TEMP_INT'            : LOCAL_TEMP_INT,
    'LOCAL_TEMP_FLOAT'          : LOCAL_TEMP_FLOAT,
    'LOCAL_TEMP_CHAR'           : LOCAL_TEMP_CHAR,      
    'LOCAL_TEMP_BOOL'           : LOCAL_TEMP_BOOL,
    'LOCAL_TEMP_POINTER_INT'    : LOCAL_TEMP_POINTER_INT,
    'LOCAL_TEMP_POINTER_FLOAT'  : LOCAL_TEMP_POINTER_FLOAT,
    'LOCAL_TEMP_POINTER_CHAR'   : LOCAL_TEMP_POINTER_CHAR, 
    'CONST_INT'                 : CONST_INT,
    'CONST_FLOAT'               : CONST_FLOAT,
    'CONST_CHAR'                : CONST_CHAR,  
    'CONST_STRING'              : CONST_STRING
}

#################################################################################      
#get memBase
MEM =  {
    'GLOBAL': {
        'INT': 'GLOBAL_INT',
        'FLOAT': 'GLOBAL_FLOAT',
        'CHAR': 'GLOBAL_CHAR',
        'BOOl': 'GLOBAL_BOOL',
        'TEMP': {
            'INT': 'GLOBAL_TEMP_INT',
            'FLOAT': 'GLOBAL_TEMP_FLOAT',
            'CHAR': 'GLOBAL_TEMP_CHAR',
            'BOOL': 'GLOBAL_TEMP_BOOL',
            'POINTER': {
                'INT': 'GLOBAL_TEMP_POINTER_INT',
                'FLOAT': 'GLOBAL_TEMP_POINTER_FLOAT',
                'CHAR': 'GLOBAL_TEMP_POINTER_CHAR',
            }
        }
    },
    'LOCAL': {
        'INT': 'LOCAL_INT',
        'FLOAT': 'LOCAL_FLOAT',
        'CHAR': 'LOCAL_CHAR',
        'BOOL': 'LOCAL_BOOL',
        'TEMP': {
            'INT': 'LOCAL_TEMP_INT',
            'FLOAT': 'LOCAL_TEMP_FLOAT',
            'CHAR': 'LOCAL_TEMP_CHAR',
            'BOOL': 'LOCAL_TEMP_BOOL',
            'POINTER': {
                'INT': 'LOCAL_TEMP_POINTER_INT',
                'FLOAT': 'LOCAL_TEMP_POINTER_FLOAT',
                'CHAR': 'LOCAL_TEMP_POINTER_CHAR',
            }
        }
    }, 
    'CONST': {
        'INT': 'CONST_INT',
        'FLOAT': 'CONST_FLOAT',
        'CHAR': 'CONST_CHAR',
        'STRING': 'CONST_STRING'
    }
}