import Operators
import IRConversionDataStructures as IRDataStructures
import IRCoversionToDataStructures as IRToDataStructures


def Convert(program, convertTo, settings):
    global IRTox86
    instList = IRToDataStructures.ToInstructionList(program)
    match convertTo:
        case "x86":
            import IRTox86            
            converter = IRTox86.Converter()
        case "cpp":
            import IRToCpp
            converter = IRToCpp.Converter()
        case _:
            raise Exception("convert To did not match any casses -> " + convertTo)    
    return converter.Convert(instList, settings)


