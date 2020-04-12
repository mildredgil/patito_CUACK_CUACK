# -----------------------------------------------------------------------------
# proyecto patito++
# AUTHORS: Mildred Gil Melchor, RAUL FLORES
# -----------------------------------------------------------------------------

import sys
sys.path.append('../..')

from sly import Lexer, Parser

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { 
        STRING, INTNUMBER, FLOATNUMBER, CHARACTER, 
        ID, VAR, PROGRAM, PRINCIPAL,
        IF, ELSE, WHILE,
        PRINT, WRITE,
        DO, FROM, TO, DO2,
        FUNCTION, RETURN, INT, FLOAT, CHAR, VOID,
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
        EQ, LT, GT, NE, ELT, EGT, AND, OR, TRANSPOSE, INVERSE, DETERMINANT }

    literals = { '[', ']','(', ')', '{', '}', ';', ':', ',', '.', '$', '?', '¡', '&' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS        = r'\+'
    MINUS       = r'-'
    TIMES       = r'\*'
    DIVIDE      = r'/'
    EQ          = r'=='
    ASSIGN      = r'='
    ELT         = r'<='
    EGT         = r'>='
    NE          = r'!='
    LT          = r'<'
    GT          = r'>'
    AND         = r'&'
    OR          = r'\|'
    TRANSPOSE   = r'¡'
    INVERSE     = r'\$'
    DETERMINANT = r'\?'
    
    @_(r'[0-9]+\.[0-9]+')
    def FLOATNUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['var'] = VAR
    ID['si'] = IF
    ID['sino'] = ELSE
    ID['lee'] = PRINT
    ID['escribe'] = WRITE
    ID['mientras'] = WHILE
    ID['haz'] = DO
    ID['hacer'] = DO2
    ID['desde'] = FROM
    ID['hasta'] = TO
    ID['funcion'] = FUNCTION
    ID['regresa'] = RETURN
    ID['programa'] = PROGRAM
    ID['ent'] = INT
    ID['deci'] = FLOAT
    ID['letra'] = CHAR
    ID['nada'] = VOID
    ID['principal'] = PRINCIPAL

    ignore_comment = r'\#.*'

    @_(r'\"(.*?)\"')
    def STRING(self, t):
        t.value = str(t.value[1: len(t.value) - 1])
        return t

    @_(r'\'(.?)\'')
    def CHARACTER(self, t):
        t.value = str(t.value[1: len(t.value) - 1])
        return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = CalcLexer.tokens
    
    precedence = (
        ('left', PLUS, MINUS),
    )

    def __init__(self):
        self.ids = { }
        self.programs = { }
    
    # PROGRAMA

    @_('PROGRAM ID ";" programa2 programa3 PRINCIPAL "(" ")" bloque')
    def programa(self, p):
        pass
    
    @_('vars')
    def programa2(self, p):
        pass

    @_('empty')
    def programa2(self, p):
        pass

    @_('funcion programa2')
    def programa3(self, p):
        pass

    @_('empty')
    def programa3(self, p):
        pass

    # VARS
    
    @_('VAR var1')
    def vars(self, p):
        pass

    @_('tipo ids ";" var2')
    def var1(self, p):
        # self.ids[p.ID] = 0
        pass

    @_('var1')
    def var2(self, p):
        # self.ids[p.ID] = 0
        pass
        
    @_('empty')
    def var2(self, p):
        pass

    @_('identificadores ids2')
    def ids(self, p):
        pass
        # self.ids[p.ID] = 0

    @_('ids')
    def ids2(self, p):
        pass

    @_('empty')
    def ids2(self, p):
        pass

    # FUNCION
    
    @_('FUNCTION funcion2 ID parametros vars bloque')
    def funcion(self, p):
        pass

    @_('tipo')
    def funcion2(self, p):
        pass

    @_('VOID')
    def funcion2(self, p):
        pass

    # PARAMETROS
    
    @_('"(" parametros2 ")"')
    def parametros(self, p):
        pass

    @_('tipo ID parametros3')
    def parametros2(self, p):
        pass

    @_('"," parametros2')
    def parametros3(self, p):
        pass

    @_('empty')
    def parametros3(self, p):
        pass

    #BLOQUE

    @_('"{" bloque2 "}"')
    def bloque(self, p):
        pass

    @_('estatuto bloque2')
    def bloque2(self, p):
        pass

    @_('empty')
    def bloque2(self, p):
        pass

    #estatuto

    @_('asignacion',
        'escritura',
        'lee',
        'estDesicion',
        'estRepNoCond',
        'estRepCond',
        'regresa')
    def estatuto(self, p):
        pass

    #assignacion

    @_('identificadores ASSIGN expmat ";"')
    def asignacion(self, p):
        return p[0] != p[2]

    #lee

    @_('PRINT "(" lee2 ")" ";"')
    def lee(self, p):
        pass

    @_('identificadores  lee3')
    def lee2(self, p):
        pass

    @_('"," lee2')
    def lee3(self, p):
        pass

    @_('empty')
    def lee3(self, p):
        pass

    #escritura
    
    @_('WRITE "(" escritura2 ")" ";"')
    def escritura(self, p):
        pass

    @_('exp escritura3')
    def escritura2(self, p):
        pass

    @_('STRING escritura3')
    def escritura2(self, p):
        pass

    @_('"," escritura2')
    def escritura3(self, p):
        pass

    @_('empty')
    def escritura3(self, p):
        pass

    #regresa

    @_('RETURN "(" exp ")" ";"')
    def regresa(self, p):
        pass

    #estatuto de decision

    @_('IF "(" expLog ")" bloque ELSE bloque ')
    def estDesicion(self, p):
        pass

    # estatuto de repeticion condicional

    @_('WHILE "(" expLog ")" DO bloque')
    def estRepCond(self, p):
        pass

    # estatuto de repeticion no condicional

    @_('FROM identificadores ASSIGN expmat TO exp DO2 bloque')
    def estRepNoCond(self, p):
        pass
    
    # identificadores

    @_('ID identificadores2')
    def identificadores(self, p):
        pass

    @_('"[" exp "]" identificadores3')
    def identificadores2(self, p):
        pass

    @_('empty')
    def identificadores2(self, p):
        pass

    @_('"[" exp "]"')
    def identificadores3(self, p):
        pass

    @_('empty')
    def identificadores3(self, p):
        pass

    # TIPO
    
    @_('INT')
    def tipo(self, p):
        pass

    @_('CHAR')
    def tipo(self, p):
        pass

    @_('FLOAT')
    def tipo(self, p):
        pass

    # EXPLOG expLog
    
    @_('expresion expLog2')
    def expLog(self, p):
        pass

    @_('AND expLog')
    def expLog2(self, p):
        pass

    @_('OR expLog')
    def expLog2(self, p):
        pass

    @_('empty')
    def expLog2(self, p):
        pass

    #EXPRESION

    @_('exp expresion2')
    def expresion(self, p):
        pass

    @_('LT exp')
    def expresion2(self, p):
        pass

    @_('GT exp')
    def expresion2(self, p):
        pass

    @_('EQ exp')
    def expresion2(self, p):
        pass

    @_('ELT exp')
    def expresion2(self, p):
        pass

    @_('EGT exp')
    def expresion2(self, p):
        pass

    @_('NE exp')
    def expresion2(self, p):
        pass

    @_('empty')
    def expresion2(self, p):
        pass

    #expMat

    @_('exp expmat2')
    def expmat(self, p):
        pass

    @_('INVERSE')
    def expmat2(self, p):
        pass

    @_('TRANSPOSE')
    def expmat2(self, p):
        pass

    @_('DETERMINANT')
    def expmat2(self, p):
        pass

    @_('empty')
    def expmat2(self, p):
        pass

    #exp

    @_('termino exp2')
    def exp(self, p):
        pass

    @_('PLUS exp')
    def exp2(self, p):
        pass

    @_('MINUS exp')
    def exp2(self, p):
        pass

    @_('empty')
    def exp2(self, p):
        pass

    # factor

    @_('"(" exp ")"')
    def factor(self, p):
        pass

    @_('PLUS varcte')
    def factor(self, p):
        pass

    @_('MINUS varcte')
    def factor(self, p):
        pass

    @_('varcte')
    def factor(self, p):
        pass

    # TERMINO

    @_('factor termino2')
    def termino(self, p):
        pass

    @_('TIMES termino')
    def termino2(self, p):
        pass

    @_('DIVIDE termino')
    def termino2(self, p):
        pass

    @_('empty')
    def termino2(self, p):
        pass

    # LLAMADA    
    @_('ID "(" llamada2 ")"')
    def llamada(self, p):
        pass

    @_('exp llamada3')
    def llamada2(self, p):
        pass

    @_('"," llamada2')
    def llamada3(self, p):
        pass

    @_('empty')
    def llamada3(self, p):
        pass

    # VARCTE

    @_('identificadores')
    def varcte(self, p):
        pass

    @_('INTNUMBER')
    def varcte(self, p):
        pass

    @_('CHARACTER')
    def varcte(self, p):
        pass

    @_('FLOATNUMBER')
    def varcte(self, p):
        pass

    @_('llamada')
    def varcte(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    filename = input("write the file name:")
    f=open(filename, "r")
    data = f.read()

    for tok in lexer.tokenize(data):
        print(tok)
    
    parser.parse(lexer.tokenize(data))