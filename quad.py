class Quad():
    def __init__(self):
        self.list = []
        self.count = 0

    def getCount(self):
        return self.count

    def get(self, counter):
        return self.list[counter]

    def add(self, op, operRight=None, operLeft=None, result=None):
        self.list.append([op, operRight, operLeft, result])
        self.count = self.count + 1

    def update(self, index, result):
        self.list[index][3] = result

    def print(self):
        for index, value in enumerate(self.list):
            switcher = {
                'None': '_'
            }
            
            print(index, str(value[0]) + "," + switcher.get(str(value[1]), str(value[1])) + "," + switcher.get(str(value[2]), str(value[2])) + "," + switcher.get(str(value[3]), str(value[3])))