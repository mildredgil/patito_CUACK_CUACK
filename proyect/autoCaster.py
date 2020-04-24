
def autoCaster(type1, type2, operator):
  floatno = 0
  if(type1 == 'float'):
    floatno=+1
  if(type2 == 'float'):
    floatno=+1
  if(operator == 'TIMES'):
    return 'float'
  if(floatno>0):
    return "float"
  return 'int'

print(autoCaster('int','int','TIMES'))
print(autoCaster('int','int','SUM'))
print(autoCaster('int','float','SUM'))