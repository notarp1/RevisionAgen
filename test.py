from sympy import to_cnf

operands = []
truthvals = []
operators = [" & ", " | ", "<=>", "->"]
symbol = "abcdefghijklmnopqrstuvwxyz"

def listOP(x):
    construcop = []
    isAssigned = False
    for p in operands:
        if x == p:
            isAssigned = True
    if not isAssigned:
        operands.append(x)

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
        listOP(x[1])
    else:
        listOP(x)

def getOP(x):
    for p in operands:
        if x == p[0]:
            return p

def orOP(list, truthvalues):
    ops = []
    for x in list:
        if "~" in x:
            ops.append(getOP(x[1]))
        else:
            ops.append(getOP(x))
    return ops[0] or ops[1]

def andOP(list, truthvalues):
    ops = []
    for x in list:
        if "~" in x:
            ops.append(getOP(x[1]))
        else:
            ops.append(getOP(x))
    return ops[0] and ops[1]


if __name__ == '__main__':
    print("Enter belief state, seperated by comma")
    print("Valid operands: '|', '&', '>>', '<->'")
    bb = input()
    list = bb.split(",")

    bbtocnf = []
    inverted = []
    for elements in list:
        if "<->" in elements:
            split = elements.split("<->")
            x1=split[0]
            x2=split[1]
            iffs = "("+x1+">>"+x2+")"+"&"+"("+x2+">>"+x1+")"
            bbtocnf.append(to_cnf(iffs))
        else:
            bbtocnf.append(to_cnf(elements))

    for x in bbtocnf:
        print(x)
        addOperands(str(x))
    for x in bbtocnf:
        vals = []
        vals.append("a")
        vals.append(True)
        vals.append("b")
        vals.append(True)
        truthvals.append(vals)
        orOP(bbtocnf, truthvals)
    print(operands)

