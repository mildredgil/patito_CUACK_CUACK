from parserLexer import CalcLexer, CalcParser
from virtualMachine import VirtualMachine
from writer import Writer

import sys, getopt

def main(filename,argv):
    inputfile = ''
    verbose = False
    justCompile = False
    
    try:
        opts, args = getopt.getopt(argv,"i:vch",["ifile=","verbose","compile","help"])
    except getopt.GetoptError:
        print('usage: {} -i <inputfile>'.format(filename))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: {} -i <inputfile>'.format(filename))
            print('usage: {} -i <inputfile> -v'.format(filename))
            print('       {} --ifile=<inputfile> --verbose'.format(filename))
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-c", "--compile"):
            justCompile = True
    
    return inputfile, verbose, justCompile

if __name__ == '__main__':
    filename, verbose, justCompile = main(sys.argv[0],sys.argv[1:])
    
    lexer = CalcLexer()
    parser = CalcParser()
    
    f=open(filename, "r")
    data = f.read()
    
    if verbose:
        lexer.printTokens(data)

    parser.parse(lexer.tokenize(data))
    
    if verbose:
        parser.printParser()
        parser.quad.print()
        parser.dataTable.print()
        print(parser.constTable.table)
    
    #CREATE OBJ FILE
    Writer.prepareOBJ(filename, parser)
    
    #RUN OBJ
    if not justCompile:
        VirtualMachine(filename + "_obj")
    