class TypeMatching():
    # left op right
    typeMatchingTable = {
        'int': {
            '+': {
                'int': 'int',
                'float': 'float'
            },
            '-': {
                'int': 'int',
                'float': 'float'
            },
            '*': {
                'int': 'int',
                'float': 'float'
            },
            '/': {
                'int': 'int',
                'float': 'float'
            },
            '=': {
                'int': 'int',
                'float': 'int'
            },
            '<': {
                'int': 'bool',
                'float': 'bool'
            },
            '>': {
                'int': 'bool',
                'float': 'bool'
            },
            '==': {
                'int': 'bool',
                'float': 'bool'
            },
            '!': 'int',
            '?': 'float',
            '$': 'float'
        },
        'float': {
            '+': {
                'int': 'float',
                'float': 'float'
            },
            '-': {
                'int': 'float',
                'float': 'float'
            },
            '*': {
                'int': 'float',
                'float': 'float'
            },
            '/': {
                'int': 'float',
                'float': 'float'
            },
            '=': {
                'int': 'float',
                'float': 'float'
            },
            '<': {
                'int': 'bool',
                'float': 'bool'
            },
            '>': {
                'int': 'bool',
                'float': 'bool'
            },
            '==': {
                'int': 'bool',
                'float': 'bool'
            },
            '!': 'float',
            '?': 'float',
            '$': 'float'
        },
        'char': {
            '=': {
                'char': 'char'
            },
            '==': {
                'char': 'bool'
            },
            '!': 'char'
        },
        'bool': {
            '&': {
                'bool': 'bool'
            },
            '|': {
                'bool': 'bool'
            }
        }
    }

    def error(self, line, right, op, left=''):
        print('Line %d: Cant assign %s %s %s' % (line, right, op, left))

        
    @classmethod
    def sem(self, line, right, op, left=None):
        if left is None:
            try:
                return self.typeMatchingTable[right][op]
            except:
                self.error(self, line, right, op, '')
        else:
            try:
                return self.typeMatchingTable[right][op][left]
            except:
                self.error(self, line, right, op, left)

'''    
print(TypeMatching.sem(1,'int', '*', 'int'))
print(TypeMatching.sem(1,'int', '*', 'char'))
print(TypeMatching.sem(1,'int', '!', 'int'))
'''