
class StdFunction():
    def __init__(self, name, returnTypeList, parameterList):
        self.name = name
        self.returnTypeList = returnTypeList
        self.parameterList = parameterList
        self.includedAllready = False

stdFunctionList = [
    StdFunction("_shalloc", ["i32$"], ["i32"]),
    StdFunction("_graphicsinit", [], ["i32"]),
    StdFunction("_getkeypress", ["i32"], ["i32"]),
    StdFunction("_printc", [], ["i32"]),
    StdFunction("_graphicspump", [], []),
    StdFunction("_drawpixel", [], ["i32", "i32", "i32", "i32", "i32"]),
    StdFunction("_graphicssleep", [], ["i32"]),
]

compileTimeFunctionList = [
    "_declindtype", "_sizeof"
]