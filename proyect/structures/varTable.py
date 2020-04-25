import json

class VarTable():
	def __init__(self):
		self.table = {}

	def exist(self, a, b):
		return b in a

	def insertElement(self, a, b):
		a.update({b: {}})

	def insert(self, type, var, value, scope='global'):
		if(not self.exist(self.table, scope)):
			self.insertElement(self.table, scope)

		if(not self.exist(self.table[scope], var)):
			self.insertElement(self.table[scope], var)

		self.table[scope][var].update({type: value})

	def look(self, type, var, scope='global'):
		try:
			return True, self.table[scope][var][type]
		except:
			return False, None

	def print(self):
		print(json.dumps(self.table, indent=2))

'''	
def main():
	dic = VarTable()
	dic.insert('int', 'a', 1)
	dic.print()
	dic.insert('int', 'a', 2, 'f1')
	dic.print()
	dic.insert('char', 'a', 'b', 'f1')
	print(dic.look('int','c', 'f1'))
	a, b = dic.look('int','a', 'f1')
	print(a,b)
	

if __name__ == "__main__":
    main()

dic = {
	'global': {
		'a': {
			'int': 1,
			'float':3.0
		}
	},
	'func':{
		'a': {
			'int': 2,
			'char': 'a'
		}
	},
	'a': {
		'a': {
			'char': 'a'
		}
	}
}
'''