
dic = {}

def exist(varName, dic):
  if varName in dic:
    return True
  else:
    return False

def basicInsert(varTipe, varValue, varScope, dic):
    dic["value"]=varValue
    dic["tipe"]=varTipe
    dic["scope"]=varScope

def insert(varName,varTipe, varValue = 0, varScope = "global"):
  if varScope != "global":
    if exist(varName,dic[varScope]):
      print("Exist already")
      return
    else:
      dic[varScope][varName] = {}
      basicInsert(varTipe, varValue, varScope,dic[varName])
      return

  if exist(varName, dic):
    print("Exist already")
    return

  if varTipe == "function":
    dic[varName] = {}
    dic[varName][varTipe] = "function"
    return
  
  else:
    dic[varName] = {}
    basicInsert(varTipe, varValue, varScope,dic[varName])

def look(varName, varScope="global"):
  if varScope == "global":
    if exist(varName, dic):
      return dic[varName]
    else:
      print("does not exist")
      return
  else:
    if exist(varName, dic[varScope]):
      return dic[varScope][varName]
    else:
      print("does not exist")
      return

# Testing
insert("a", "int",  7)
print("inserting a")
print(dic)

insert("a", "int",  8)
print("inserting a again")
print(dic)
print("look",look("a"))

insert("f", "function",  0)
print("making function f again")
print(dic)

insert("a", "int",  8, "f")
print("inserting a intro f")
print(dic)

print("look",look("a"))