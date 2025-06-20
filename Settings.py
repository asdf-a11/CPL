import sys

OPERATING_SYSTEM = sys.platform
match OPERATING_SYSTEM:
    case "Linux":
        FILE_SEPERATOR = "/"
    case "Windows":
        FILE_SEPERATOR = "\\"
    case _:
        print("OS unknown might cause weird behavoir os=", OPERATING_SYSTEM)
        FILE_SEPERATOR = "/"
