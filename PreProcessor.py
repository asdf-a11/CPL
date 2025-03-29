import Util
import Lexer

macroList = []
class Macro():
    def __init__(self, name, content, argList=[]):
        self.name = name
        self.content = content
        self.argList = argList
    def Replace(self, args=[]):
        return self.content
def ReadInInstruction(code, idx):
    inst = ""
    while 1:
        if code[idx] == " ":
            break
        inst += code[idx]
        idx += 1
    return inst, idx
def GetNameAndArgs(code, idx):
    bracketCounter = 0
    name = ""
    foundName = False
    word = ""
    while 1:
        if (code[idx] == " " or code[idx] == "(") and foundName == False:
            name = word
            word = ""            
            foundName = True
            if code[idx] == " ":
                break
            idx += 1
            continue
        if code[idx] == "(":
            bracketCounter += 1
            continue
        if code[idx] == ")":
            bracketCounter -= 1
            if bracketCounter == 0:
                idx += 1
                break
            continue        
        word += code[idx]
        idx += 1
    return name, word.split(","), idx
def ReadTillChar(lst, idx, endChar):
    out = []
    while 1:
        if lst[idx] == endChar:
            idx += 1
            break
        out.append(lst[idx])
        idx += 1
    return out, idx
def CheckIfMacro(lst, cdx):
    for m in macroList:
        if lst[cdx] == m.name:
            return m
    return False
def SplitListToString(lst):
    out = ""
    for i in lst:
        out += i
    return out
def IsMacroDef(splitList, counter):
    #define true 1#
    if splitList[counter] == "define":
        counter += 1
        name = splitList[counter]
        counter += 1
        content,counter = ReadTillChar(splitList, counter, "#")
        macroList.append(Macro(name, content,[]))
        return True, counter
    return False, None
def IsMultiLineComment(splitList, counter):
    if splitList[counter] == "#":
        counter += 1
        while not (splitList[counter] == "#" and splitList[counter+1] == "#"):
            counter += 1
            if counter >= len(splitList)-1:
                raise Exception("No close to multi line comment")
        return True, counter + 1
    return False, None        
        

def RemoveOneLineComments(code):
    counter = 0
    while counter < len(code) - 1:
        if code[counter] == "#" and code[counter + 1] == "c":
            while code[counter] != "\n":
                del code[counter]
        counter += 1
    return code     
def MacroExpantion(splitList, counter):
    hap = False
    for i in macroList:
        if i.name == splitList[counter]:
            splitList = splitList[:counter-1] + i.content + splitList[counter:]
            hap = True
    return hap

    

def PerformPass(splitList):
    anythingHappend = False
    counter = 0
    directiveFunctionList = [
        IsMacroDef, IsMultiLineComment
    ]
    while counter < len(splitList) - 1:
        if splitList[counter] == "#":
            validInstruction = False
            for function in directiveFunctionList:
                hap, newCounter = function(splitList, counter+1)
                if hap:
                    validInstruction = True
                    del splitList[counter: newCounter + 1]
                    anythingHappend = True
                    break
            if validInstruction == False:
                raise Exception("Invalid pre proc instruction")
        else:
            counter += 1
        anythingHappend = anythingHappend or MacroExpantion(splitList, counter)
        
    #check for trailing open preprocessor directive
    if splitList[-1] == "#":
        raise Exception("Code cannot end with unclosed #")
    return anythingHappend


def PreProcess(code):
    #handle one line comments
    code = RemoveOneLineComments(code)
    #loop through replacing macros and creating new macros
    splitList = Lexer.GenerateSplitList(code)
    PerformPass(splitList)
    

    return SplitListToString(splitList)



'''
    tokenCounter = 0
    anythingHappened = False
    while tokenCounter < len(splitList):
        if splitList[tokenCounter] == "#":            
            startCdx = tokenCounter
            tokenCounter += 1
            hap, newCdx = IsMacro(splitList, tokenCounter)
            anythingHappened = anythingHappened or hap
            pre = splitList[:startCdx]
            after = splitList[tokenCounter:]
            splitList = pre + after
        v = CheckIfMacro(splitList, tokenCounter)
        if v != False:
            pre = splitList[:tokenCounter]
            after = splitList[tokenCounter + 1:]
            splitList = pre + after
            for i in reversed(v.content):
                splitList.insert(tokenCounter, i)
            anythingHappened = True
        tokenCounter += 1
    if anythingHappened:
        splitList = PreProcess()

'''