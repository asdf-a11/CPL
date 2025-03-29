class Arg():
    def __init__(self, dataType, content):
        self.dataType = dataType
        self.content = content
class Instruction():
    def __init__(self,name, argList=[]):
        self.name = name
        self.argList = argList    
    def Print(self,ret=False):
        out = self.name + " "
        for i in self.argList:
            out += str(i) + ", "
        if len(self.argList) >= 1:
            out = out[:-2]
        if ret:
            return out
        print(out)
        return ""
    def __repr__(self):
        return self.Print(ret=True)
def PrintInstList(instList, ret=False):
    out = ""
    tabs = ""
    for i in instList:
        if i.name == "OPENSCOPE":
            tabs += "\t"
        out += tabs + i.Print(ret=True)+"\n"
        if i.name == "CLOSESCOPE":
            tabs = tabs[1:]
    if ret:
        return out
    print(out)
    return ""        
class Variable():
    def __init__(self, expTemp = False, name = None):
        global varaibleCounter
        self.expTemp = expTemp
        self.name = name
        if self.name == None:
            self.name = "EXP_VAR_" + str(varaibleCounter)
        varaibleCounter += 1
    def __str__(self):
        out = "[IRVariable]"+self.name
        return out
varaibleCounter = 0
    



