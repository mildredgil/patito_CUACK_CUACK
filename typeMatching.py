class TypeMatching():
    """Type Matching is incharge of the assignation of types"""

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

    def error(self, line, left, op, right=''):
        raise Exception('Line {}: Cant assign {} {} {}'.format(line, right, op, left))

        
    @classmethod
    def sem(self, line, left, op, right=None):
        """
            Here do we decide if the matches are correctly or not.
        """
        
        if right is None:
            try:
                return self.typeMatchingTable[left][op]
            except:
                self.error(self, line, left, op, '')
        else:
            try:
                return self.typeMatchingTable[left][op][right]
            except:
                self.error(self, line, left, op, right)
