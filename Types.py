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
        self.isPtr = False
    def __str__(self):
        return self.name

unknownType = Type("UNKNOWN", None, None)
voidType = Type("void", None, None)
i32Type = Type("i32", "int", 4)
i8Type = Type("i8", "int", 4)
f32Type = Type("f32", "float", 4)

typeList = [
    unknownType,
    voidType,
    i32Type,
    i8Type,
    f32Type
]

#typeList = baseTypeList.copy()

typeNameList = []

def Init():
    for t in typeList:
        typeNameList.append(t.name)
def GetTypeByName(name) -> Type | bool:
    for t in typeList:
        if t.name == name:
            return t
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
    else:
        raise Exception("Invalid style")