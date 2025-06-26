MAX_BIDMAS = 0

class Operator():
    def __init__(self,name,argCount, bidmasLevel=-1):
        self.name = name
        self.argCount = argCount
        self.bidmasLevel = bidmasLevel
        self.tokenSize = None
    def SetTokenSize(self):
        splitList = list("<>:;@~#[]{}()*&^%$£!¬\\/?|+=-") 
        hap = False
        tokenCounter = 0
        for c in self.name:
            if c in splitList:
                tokenCounter += 1
                hap = True
        if hap == False:
            tokenCounter = 1
        self.tokenSize = tokenCounter


operatorList = [
    Operator("==",2,2),
    Operator("<",2,2),
    Operator(">",2,2),
    Operator("<=",2,2),
    Operator(">=",2,2),
    Operator("!=",2,2),
    Operator("and",2,1), #logic and
    Operator("or",2,1), #logic or
    Operator("|",2,1), #bitwise or
    Operator("&&",2,1), #bitwise and
    Operator("xor",1,1),    
    Operator("+",2,3),
    Operator("-",2,3),
    Operator("*",2,4),
    Operator("<<",2,4),
    Operator(">>",2,4),
    Operator("%",2,4),
    Operator("@",2,4),
    Operator("/",2,4),
    Operator("//",2,4),
    Operator("^",2,5),
    Operator("!",1,6), #logical not
    Operator("$",1,6),
    Operator("&",1,6),
    Operator(".",1,6),
    Operator("VOID_OP",2,1),
    

    Operator("+=",0),
    Operator("-=",0),
    Operator("/=",0),
    Operator("*=",0),
    Operator("^=",0),
    
    Operator("#",-1,-1),#single line comment
    Operator("##",-1,-1)#multi line comment
]
operatorNameList = []

def Init():
    global MAX_BIDMAS
    for o in operatorList:
        operatorNameList.append(o.name)
        MAX_BIDMAS = max(o.bidmasLevel, MAX_BIDMAS)
        o.SetTokenSize()
def IndexOperatorByName(name,throwError=True):
    for odx,o in enumerate(operatorList):
        if o.name == name:
            return operatorList[odx]
    if throwError:
        raise Exception("Failed to find operator")
    else:
        return -1
def PerformConstOperation(v1,op,v2):
    pythonComp = [
        "==", "<",">","<=",">=", "and", "or",
        "!=", "*", "+", "-"
    ]
    if op in pythonComp:
        return eval(v1 + " " + op + " " + v2)
    if op == "^":
        return eval(v1 + " ** " + v2)
    elif op == "xor":
        return eval(v1 + " ^ " + v2)
    elif op == "!":
        binList = bin(v1)[2:].zfill(8*4)
        for i in range(len(binList)):
            binList[i] = "1" if binList[i] == "0" else "0"
        return int(binList, 2)
    raise Exception("Invalid operator")