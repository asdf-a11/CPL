import copy
#if boolean operator then bool
#bigger beat smaller of same style
#float beat int
#signed beat unsigned


class Type():
    def __init__(self,  name, style, sizeInBytes):
        self.name = name
        self.style = style
        self.sizeInBytes = sizeInBytes
        self.isPtr = 0
    def __str__(self):
        return self.name

unknownType = Type("UNKNOWN", None, None)
voidType = Type("void", None, None)
i32Type = Type("i32", "int", 4)
i8Type = Type("i8", "int", 4)
ui8Type = Type("ui8", "unsigned", 1)
f32Type = Type("f32", "float", 4)
typeType = Type("type", "type", -1)

typeList = [
    unknownType,
    voidType,
    i32Type,
    i8Type,
    ui8Type,
    f32Type,
    typeType
]

#typeList = baseTypeList.copy()

typeNameList = []

def Init():
    for t in typeList:
        typeNameList.append(t.name)
def GetTypeByName(name) -> Type | bool:
    cleanedName = name.replace("$", "")
    isPtr = "$" in name
    for t in typeList:
        if t.name == cleanedName:
            retType = copy.deepcopy(t)
            retType.isPtr = isPtr
            return retType
    return False
    #raise Exception("Failed to find type with name -> " + name)
def GetTypeByStyleAndSize(style, sizeInBytes):
    if style == "float":
        if sizeInBytes == 4:
            return copy.deepcopy(f32Type)
        #elif sizeInBytes == 4:
        #    return f64Type
        else:
            raise Exception("Invlaid size for float")
    elif style == "int":
        if sizeInBytes == 1:
            return copy.deepcopy(i8Type)
        elif sizeInBytes == 4:
            return copy.deepcopy(i32Type)
        else:
            raise Exception("Invalid size for int")
    elif style == "unsigned":
        if sizeInBytes == 1:
            return copy.deepcopy(ui8Type)
        elif sizeInBytes == 8:
            return copy.deepcopy(ui64Type)
        else:
            raise Exception("Invalid size for style unsigned")
    else:
        raise Exception("Invalid style")