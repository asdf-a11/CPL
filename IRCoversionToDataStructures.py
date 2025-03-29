import IRConversionDataStructures as DataStructures
import Types

def ProgramToInstructionList(program):
    instList = []
    program = program.replace("\t","")
    lineList = program.split("\n")
    for l in lineList:
        if len(l) == 0: continue
        instName = ""
        while 1:
            if l[0] == " ":
                break
            instName += l[:1]
            l = l[1:]
        l = l.replace(" ","")
        wordList = l.split(",")
        instList.append(DataStructures.Instruction(instName, wordList))
    return instList
def StringArgsToArgs(instList):
    for idx,i in enumerate(instList):
        for adx,a in enumerate(i.argList):
            if "lab_" in a:
                instList[idx].argList[adx] = DataStructures.Argument("LABEL", a)
            elif a.isdigit():
                instList[idx].argList[adx] = DataStructures.Argument("CONST", a)
            elif a.lower() in Types.typeNameList:
                instList[idx].argList[adx] = DataStructures.Argument("TYPE", a)
            else:
                instList[idx].argList[adx] = DataStructures.Argument("NAME", a)
                
def ToInstructionList(program):
    instList = ProgramToInstructionList(program)
    #instList = StringArgsToArgs(instList)
    return instList


