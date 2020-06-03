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
                'float':'int'
            },
            '<': {
                'int': 'bool',
                'float': 'bool'
            },
            '>': {
                'int': 'bool',
                'float': 'bool'
            },
            '<=': {
                'int': 'bool',
                'float': 'bool'
            },
            '>=': {
                'int': 'bool',
                'float': 'bool'
            },
            '!=': {
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
            '<=': {
                'int': 'bool',
                'float': 'bool'
            },
            '>=': {
                'int': 'bool',
                'float': 'bool'
            },
            '!=': {
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
        raise Exception('Line {}: Cant assign {} {} {}'.format(line, right, op, left))

        
    @classmethod
    def sem(self, line, left, op, right=None):
        """
            Here do we decide if the matches are correctly or not.
        """
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
