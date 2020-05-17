import csv
from quad import Quad
from dataTable import DirFunc

class VirtualMachine():
    def __init__(self, filename):
        self.filename = filename
        self.quad = Quad()
        self.dirFunc = DirFunc()
        self.readFile()
        
    def readFile(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            readingContext = 0
            for row in reader:
                if row['1'] == "#QUAD":
                    readingContext = 1
                elif row['1'] == "#DIRFUNC":
                    readingContext = 2
                elif row['1'] == "#CONST":
                    readingContext = 3
                else:
                    if readingContext == 1:
                        switcher = {
                            '_': None
                        }
                        self.quad.add(row['1'],switcher.get(row['2'],row['2']),switcher.get(row['3'],row['3']),switcher.get(row['4'],row['4']))
                    elif readingContext == 2:
                        self.dirFunc.insert(row['1'],row['2'],row['3'],row['4'],row['5'])
        self.quad.print()
        self.dirFunc.print()

a = VirtualMachine("samples/funciones_obj")