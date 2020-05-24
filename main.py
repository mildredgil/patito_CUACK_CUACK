from parserLexer import CalcLexer, CalcParser
from virtualMachine import VirtualMachine
from writer import Writer

def printParser(parser):
    print("dataTable:")
    parser.dataTable.print()
    print("quadruple:")
    parser.quad.print()
    print(parser.constTable.table)

def printTokens(lexer):
    for tok in lexer.tokenize(data):
        print(tok)

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    filename = input("write the file name:")
    f=open(filename, "r")
    data = f.read()

    parser.parse(lexer.tokenize(data))

    printParser(parser)
    #printTokens(lexer)
        
    #CREATE OBJ FILE
    Writer.prepareOBJ(filename, parser)

    #RUN OBJ
    #VirtualMachine(filename + "_obj")
    #parser.printTokens()
    