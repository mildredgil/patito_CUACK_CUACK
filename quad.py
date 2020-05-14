class Quad():
    def __init__(self):
        self.list = []
        self.count = 0

    def getCount(self):
        return self.count

    def add(self, op, operRight=None, operLeft=None, result=None):
        self.list.append([op, operRight, operLeft, result])
        self.count = self.count + 1

    def update(self, index, result):
        self.list[index][3] = result

    def print(self):
        for index, value in enumerate(self.list):
            print(index, value)

