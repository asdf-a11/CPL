#import ieee754

#index list
def il(l, index, errMsg):
    try:
        return l[index]
    except Exception:
        raise Exception(errMsg + " | index = "+str(index)+" dump -> " + str(l))

sortList = list("9876543210abcdefghijklmnopqrstuvwxyz_")
def AlphabeticalHighest(string1, string2):
    for i in range(min(len(string1),len(string2))):
        v1 = sortList.index(string1[i])
        v2 = sortList.index(string2[i])
        if v2 < v1:
            return True
        if v2 > v1:
            return False
    return len(string1) > len(string2)
def BubbleSort(dataList, SwapFunction):
    counter = 0
    while 1:
        if counter >= len(dataList)-1:
            break
        if SwapFunction(dataList[counter], dataList[counter+1]):
            temp = dataList[counter]
            dataList[counter] = dataList[counter+1]
            dataList[counter+1] = temp
            counter = 0
        else:
            counter += 1
    return dataList

def min(a,b):
    if a == None:
        return b
    if b == None:
        return a
    if a <= b:
        return a
    return b
def min(a,b):
    if a == None:
        return b
    if b == None:
        return a
    if a >= b:
        return a
    return b

def IsConstant(string):
    string = string.replace(".","")
    string = string.replace("_", "")
    if string.isdigit():
        return True
    return False

def RemoveCharAtIndex(string, index):
    return string[:index] + string[index+1:]
def InsertStringIntoString(org, toInsert, idx):
    s1 = org[:idx]
    s2 = org[idx:]
    return s1 + toInsert + s2
#def FloatToIEEE754(x):
#    return str(ieee754.single(x)).replace(" ","")

def argMin(lst):
    smallestIdx = -1
    smallestValue = lst[0]
    for idx,i in enumerate(lst):
        if i < smallestValue:
            smallestIdx = idx
    return smallestIdx

def argMax(lst):
    largestIdx = 0
    largestValue = lst[0]
    for idx, i in enumerate(lst):
        if i > largestValue:
            largestValue = i
            largestIdx = idx
    return largestIdx
