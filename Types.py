class Type():
    def __init__(self,  name, style, sizeInBytes):
        self.name = name
        self.style = style
        self.sizeInBytes = sizeInBytes
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

typeNameList = []

def Init():
    for t in typeList:
        typeNameList.append(t.name)
def GetTypeByName(name):
    for t in typeList:
        if t.name == name:
            return t
    raise Exception("Failed to find type with name -> " + name)