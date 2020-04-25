class stack:
    def __init__(self):
        self.data = []

    def empty(self):
        return self.data == []

    def push(self, newData):
        self.data.append(newData)

    def pop(self):
        if(len(self.data) > 0):
            self.data.pop()
        else:
            print("Stack is empty")

    def top(self):
        return self.data[len(self.data) - 1]

    def print(self):
        print(self.data)
            
class queue:
    def __init__(self):
        self.data = []

    def empty(self):
        return self.data == []

    def enqueue(self, newData):
        self.data.insert(0, newData)

    def dequeue(self):
        if(len(self.data) > 0):
            self.data.pop()
        else:
            print("Queue is empty")

    def print(self):
        print(self.data)

def main():
    print("---- stack ----")
    print("push 1")
    print("push 2")
    print("push 3")
    s = stack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.print()

    if s.empty():
        print("stack is empty")
    else:
        print("stack isn't empty")
    
    print('top:' + str(s.top()))
    print("pop")
    s.pop()
    print('top:' + str(s.top()))
    print("pop")
    s.pop()
    print('top:' + str(s.top()))
    print("pop")
    s.pop()
    
    if s.empty():
        print("stack is empty")
    else:
        print("stack isn't empty")
    
if __name__ == "__main__":
    main()