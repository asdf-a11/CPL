class Argument():
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data

class Instruction():
    def __init__(self, name, argList=[]):
        self.name = name
        self.argList = argList
    def Print(self, ret = False):
        out = self.name + " " +str(self.argList)
        if ret: return out
        print(out)
    def __repr__(self):
        return self.Print(ret=True)
