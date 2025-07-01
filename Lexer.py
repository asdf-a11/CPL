import Types
import Operators
import copy


Operators.Init()
Types.Init()

specialCharacters = list(";:[]{}()~,#<>=/+-.*!$%^&~¬?¬|\n\t \'")
specialCharactersTokens = list(";:[]{}()~,.?=¬|")

keyWordList = [
    "fn", "return", "if", "else", "while", "struct"
]

class Token():
    def __init__(self, typ="NONE", subset="NONE"):
        self.tokenType = subset
        self.tokenSubset = typ
        #self.tokenContent = "NONE"
        self.tokenContent = self.tokenSubset
        self.newLine = 0
        self.whiteSpace = 0
    def Print(self,ret=False,nl=True, whiteSpace=True) -> None:
        outString = ""
        s = self.tokenSubset
        if self.tokenType == "WHITE_SPACE":
            s = "nts"[list("\n\t ").index(s)]
        outString = (" " * self.whiteSpace)*int(whiteSpace) + self.tokenType+":"+str(s)
        if nl: outString += "\n"
        if ret: return outString
        print(outString)
    def __repr__(self):
        return "Token("+self.Print(ret=True,nl=False,whiteSpace=False)+")"
    def __str__(self):
        return str(self.tokenSubset)
        #return self.Print(ret=True,nl=False)
def CmpTokens(token1, token2):
    if token1.tokenType == token2.tokenType:
        if token1.tokenSubset == token2.tokenSubset:
            return True
    return False
def StringSplit(string, splitter):
    out = []
    hitCounter = 0
    hap = True
    didSplit = False
    while hap:
        if len(string) == 0: break
        for idx,s in enumerate(string):
            if s == splitter[hitCounter]:
                hitCounter += 1
                if hitCounter == len(splitter):
                    prevString = string[:idx-len(splitter)+1]
                    if len(prevString) != 0:
                        out.append(prevString)
                    out.append(splitter)
                    hap = True
                    didSplit = True
                    string = string[idx+1:]
                    hitCounter = 0
                    break
            else:
                hitCounter = 0
            hap = False
    if didSplit:
        if len(string) != 0:
            out.append(string)
    if didSplit == False: out = [string]
    return out
def SplitViaSpecialCharacters(stringList):
    for c in specialCharacters:
        outList = []
        for s in stringList:
            if s not in Operators.operatorNameList:
                outList += StringSplit(s,c)
            else:
                outList.append(s)
        #print(outList, c)
        stringList = outList
    return stringList
def GenerateSplitList(string):
    tokenList = SplitViaSpecialCharacters([string])
    return tokenList
def GenerateTokenFromWithinList(idx, splitList, tokenList, searchList, subset = None):
    word = splitList[idx]
    for w in searchList:
        if w == word:
            t = Token()
            if subset == None:
                t.tokenType = w.upper()
            else:
                t.tokenType = subset
                t.tokenSubset = word
            t.tokenContent = word
            tokenList.append(t)
            return True
    return False
def GenerateTokenFromKeyword(idx, splitList, tokenList):
    return GenerateTokenFromWithinList(idx, splitList, tokenList, keyWordList)
def GenerateTokenFromOperator(idx, splitList, tokenList):
    #if idx == 53:
    #    print("")
    word = splitList[idx]
    if word == "=":
        pass    
    operatorIndex = -1
    maxWordLength = -1
    for wdx,w in enumerate(Operators.operatorList):
        if w.tokenSize + idx >= len(splitList):
            continue
        testList = splitList[idx : idx + w.tokenSize]
        testList = "".join(testList)
        if testList == w.name and w.tokenSize > maxWordLength:
            maxWordLength = w.tokenSize
            operatorIndex = wdx
    if operatorIndex != -1:
        t = Token()
        t.tokenType = "OPERATOR"
        t.tokenSubset = Operators.operatorNameList[operatorIndex]
        t.tokenContent = word
        tokenList.append(t)
        return maxWordLength
    return False
def GenerateTokenFromType(idx, splitList, tokenList):
    return GenerateTokenFromWithinList(idx, splitList, tokenList, Types.typeNameList, "TYPE")
def GenerateTokenFromBase10Number(idx, splitList, tokenList):
    word = splitList[idx]
    if word.isdigit():
        t = Token()
        t.tokenType = "CONST"
        if "." in word:
            t.tokenSubset = float(word)
        else:
            t.tokenSubset = int(word)
        t.tokenContent = word
        tokenList.append(t)
        return True
    return False
def GenerateTokenFromBase16Number(idx, splitList, tokenList):
    word = splitList[idx]
    if len(word) > 2:
        if word[0] == "0" and word[1] == "x":
            t = Token()
            t.tokenType = "CONST"
            t.tokenSubset = str(t.tokenSubset)#int(word,16)
            t.tokenContent = word
            tokenList.append(t)
            return True
    return False
def GenerateTokenFromBase2Number(idx, splitList, tokenList):
    word = splitList[idx]
    if len(word) > 2:
        if word[0] == "0" and word[1] == "b":
            t = Token()
            t.tokenType = "CONST"
            t.tokenSubset = int(word,2)
            t.tokenContent = str(t.tokenSubset)#word
            tokenList.append(t)
            return True
    return False
def GenerateTokenFromString(idx, splitList, tokenList):
    word = splitList[idx]
    if "\"" in word:
        #small chance of weird behavvoier
        stringContent = word[1:]
        while 1:
            stringContent += splitList[idx]
            if "\"" in splitList[idx]:
                stringContent = stringContent[:len(stringContent)-1]
                break
            idx += 1
        t = Token()
        t.tokenType = "ARRAY"
        t.tokenSubset = list(stringContent)
        t.tokenContent = str(t.tokenSubset)#word
        tokenList.append(t)
        return True
    return False
def GenerateTokenFromWhiteSpace(idx, splitList, tokenList):
    word = splitList[idx]
    if len(word) == 1:
        if word in list("\n\t "):
            t = Token()
            t.tokenContent = word
            t.tokenType = "WHITE_SPACE"
            t.tokenSubset = word
            tokenList.append(t)
            return True
    return False
def GenerateTokenFromSpecialChar(idx, splitList, tokenList):
    word = splitList[idx]
    if len(word) == 1:
        if word in specialCharactersTokens:
            t = Token()
            t.tokenType = word
            t.tokenContent = word
            tokenList.append(t)
            return True
    return False
def ReformConstFloats(tokenList):
    idx = 1
    while idx < len(tokenList)-1:
        if tokenList[idx].tokenType == ".":
            if tokenList[idx-1].tokenType == "CONST":
                if tokenList[idx+1].tokenType == "CONST":
                    reformedString = float(str(tokenList[idx-1].tokenSubset) + "." + str(tokenList[idx+1].tokenSubset))
                    tokenList.pop(idx-1); tokenList.pop(idx-1)
                    newToken = Token()
                    newToken.tokenType = "CONST"
                    newToken.tokenContent = reformedString
                    newToken.tokenSubset = reformedString
                    tokenList[idx-1] = newToken
        idx += 1
def GenerateTokenFromConstChar(idx, splitList, tokenList):
    if splitList[idx] == "'":
        charString = ""
        hasClosingChar = False
        idx += 1
        while idx < len(splitList):
            if splitList[idx] == "'":
                hasClosingChar = True
                break
            charString += splitList[idx]
            idx += 1
        if hasClosingChar == False:
            raise Exception("Unclosed character constant at index: " + str(idx))
        value = None
        try:
            value = ord(charString)
        except Exception:
            raise Exception("Cannot get ord value of character: " + charString)
        t = Token()
        t.tokenType = "CONST"
        t.tokenSubset = value
        t.tokenContent = value
        tokenList.append(t)
        return 1 + len(charString) + 1  # +1 for the closing ' and opening '
    return 0

def GenerateTokenList(splitList):
    tokenList = []
    counter = 0
    while counter < len(splitList):
        if GenerateTokenFromKeyword(counter,splitList,tokenList):
            counter += 1; continue
        opSize = GenerateTokenFromOperator(counter,splitList,tokenList)
        if opSize != False:
            counter += opSize; continue
        if GenerateTokenFromType(counter,splitList,tokenList):
            counter += 1; continue
        #TODO weird
        if GenerateTokenFromBase10Number(counter,splitList,tokenList):
            counter += 1; continue
        if GenerateTokenFromBase16Number(counter,splitList,tokenList):
            counter += 1; continue
        if GenerateTokenFromBase2Number(counter,splitList,tokenList):
            counter += 1; continue
        
        v = GenerateTokenFromConstChar(counter, splitList, tokenList)
        counter += v
        if v != 0: continue

        if GenerateTokenFromWhiteSpace(counter,splitList,tokenList):
            counter += 1; continue
        if GenerateTokenFromSpecialChar(counter,splitList,tokenList):
            counter += 1; continue
        #---------name-----------
        t = Token()
        content = "_" + splitList[counter]
        t.tokenContent = content
        t.tokenType = "NAME"
        t.tokenSubset = content
        tokenList.append(t)
        counter += 1 
    ReformConstFloats(tokenList)
    return tokenList  
def RemoveWhiteSpace(tokenList):
    newTokenList = []
    currentWhiteSpace = 0
    currentNewLine = 0
    for t in tokenList:
        if t.tokenType == "WHITE_SPACE":
            if t.tokenSubset == "\t":
                currentWhiteSpace += 4
            if t.tokenSubset == " ":
                currentWhiteSpace += 1
            if t.tokenSubset == "\n":
                currentNewLine += 1
                currentWhiteSpace = 0
        else:
            newTokenList.append(t)
            newTokenList[-1].whiteSpace = currentWhiteSpace
            newTokenList[-1].newLine = currentNewLine
            currentWhiteSpace = 0
            currentNewLine = 0
    return newTokenList
def RemoveComments(tokenList):
    #tokenList = tokenList.copy()
    comment = False
    multiLineComment = False
    idx = 0
    while idx < len(tokenList):
        i = tokenList[idx]
        justChanged = False
        if i.tokenType == "OPERATOR":
            if i.tokenSubset == "#":
                comment = True
                justChanged = True
            if i.tokenSubset == "##":
                if not(comment and multiLineComment == False):
                    comment = not comment
                    multiLineComment = not multiLineComment
                    justChanged = True
        if i.tokenType == "WHITE_SPACE" and i.tokenSubset == "\n" and multiLineComment == False:
            comment = False
        if comment or justChanged:
            tokenList.pop(idx)
            idx -= 1
        idx += 1
    return tokenList
def SeperateData(tokenList):
    dataCounter = 0
    idx = 0
    tokenListSize = len(tokenList)
    while idx < tokenListSize:
        if tokenList[idx].tokenContent == "[":
            #check to make sure it is not liek i32[4]
            isPartOfTypeName = False
            if idx > 0:
                if tokenList[idx-1].tokenType == "TYPE":
                    isPartOfTypeName = True
            if isPartOfTypeName == False:
                arrayStartIdx = idx
                arrayTokenList = []
                squareBracketCounter = 0
                while 1:
                    arrayTokenList.append(copy.deepcopy(tokenList[idx]))
                    if tokenList[idx].tokenContent == "[":
                        squareBracketCounter += 1
                    if tokenList[idx].tokenContent == "]":
                        squareBracketCounter -= 1
                        if squareBracketCounter == 0:
                            break
                    idx += 1
                del tokenList[arrayStartIdx+1: idx+1]
                idx = arrayStartIdx         
                name = "data_"+str(dataCounter)
                tokenList.append(Token())  
                tokenList[idx].tokenType == "NAME"
                tokenList[idx].tokenSubset, tokenList[idx].tokenContent = name, name

                tokenList.append(Token())  
                tokenList[-1].tokenType == "TYPE"
                tokenList[-1].tokenSubset, tokenList[-1].tokenContent = "UNKNOWN", "UNKNOWN"
                tokenList.append(Token())  
                tokenList[-1].tokenType == "NAME"            
                tokenList[-1].tokenSubset, tokenList[-1].tokenContent =   name,name
                tokenList.append(Token())  
                tokenList[-1].tokenType == "NONE"
                tokenList[-1].tokenSubset, tokenList[-1].tokenContent = "=", "="
                tokenList += arrayTokenList
                tokenList.append(Token())  
                tokenList[-1].tokenType == "NONE"
                tokenList[-1].tokenSubset, tokenList[-1].tokenContent = ";", ";"             
        idx += 1
    return tokenList
def PrintTokenList(tokenList):
    for t in tokenList:
        if t.newLine > 0: print("\n")
        s = t.tokenSubset
        if t.tokenType == "WHITE_SPACE":
            s = "nts"[list("\n\t ").index(s)]
        print((" " * t.whiteSpace) + t.tokenType+":"+str(s), end=", ")
    print("")