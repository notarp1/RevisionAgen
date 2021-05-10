import itertools
operands = []
operators = ["&", "|", "<=>", "->"]

def listOP(x, bool):
    construcop = []
    if operands == None:
        construcop.append(x)
        construcop.append(bool)
        operands.append(construcop)
    else:
        isAssigned = False
        for p in operands:
            if x == p[0]:
                isAssigned = True
        if not isAssigned:
            construcop.append(x)
            construcop.append(bool)
            operands.append(construcop)

def addOperands(x):
    for p in operators:
        if p in x:
            split = x.split(p)
            for element in split:
                isNegated(element)
            return
    else:
        isNegated(x)
        return

def isNegated(x):
    if "~" in x:
        listOP(x[1], False)
    else:
        listOP(x, True)

def getOP(x):
    if x[0] == "~":
        for p in operands:
            if x[1] == p[0]:
                return p
    for p in operands:
        if x == p[0]:
            return p


#Add belief bases
beliefBase = []
def addBB(x):
    belief = []
    belief.append(x)
    if "&" in x:
        split = x.split("&")
        x1 = getOP(split[0])
        x2 = getOP(split[1])
        belief.append(x1[1] and x2[1])
        beliefBase.append(belief)
        return
    if "|" in x:
        split = x.split("|")
        x1 = getOP(split[0])
        x2 = getOP(split[1])
        belief.append(x1[1] or x2[1])
        beliefBase.append(belief)
        return
    if "->" in x:
        split = x.split("->")
        x1 = getOP(split[0])
        x2 = getOP(split[1])
        val = ((x1[1] and x2[1]) or not x1[1])
        belief.append(val)
        beliefBase.append(belief)
        return
    if "<->" in x:
        split = x.split("<->")
        x1 = getOP(split[0])
        x2 = getOP(split[1])
        val = x1 == x2
        belief.append(val)
        beliefBase.append(belief)
        return
    else:
        x1 = getOP(x)
        belief.append(x1[1])
        beliefBase.append(belief)
        return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("Enter belief state, seperated by comma")
    bb = input()
    temp1 = []
    temp2 = []
    list = bb.split(",")
    value = []
    for x in list:
        addOperands(x)

    for x in list:
        addBB(x)

    print("OPERANDS + VALUES")
    print(operands)
    print("BELIEF BASE")
    print(beliefBase)

    ##ikke færdig
    for p in operators:
        for x in beliefBase:
            if p in x[0]:
                if x[1] == False:
                    print("FEJL: IKKE VALID BELIEFBASE")










# See PyCharm help at https://www.jetbrains.com/help/pycharm/
