import itertools
import numpy as np
from sympy import to_cnf

operands = []
operandsAssigned = []
truthvals = []
gpermutations = []
operators = [" & ", " | "]
symbol = "abcdefghijklmnopqrstuvwxyz"


def listOP(x):
    construcop = []
    isAssigned = False
    for p in operands:
        if x == p:
            isAssigned = True
    if not isAssigned:
        operands.append(x)


def listOPAss(x, assigned):
    operandsAssigned.append([x, assigned])


def addOperands(x):
    for p in operators:
        if p in x:
            split = x.split(p)
            for element in split:
                isNegated(element, False)
            return
    else:
        isNegated(x, False)
        return


def isNegated(x, assigned):
    if not assigned:
        if "~" in x:
            listOP(x[1])
        else:
            listOP(x)
    else:
        if "~" in x:
            listOPAss(x[1], False)
        else:
            listOPAss(x, True)


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


def revise(operands):
    # calculate how many permutations there are of the number of operands
    n = len(operands)
    # append the letters in operand and their negated form
    letters = []
    for x in operands:
        if x not in letters:
            letters.append(x[0])
            letters.append("~" + x[0])

    # add a permutation if it holds no duplicates
    permutations = []
    usedstrings = []
    for x in foo(letters, n):
        if stringtester(x, usedstrings):
            print(''.join(x))
            permutations.append(''.join(x))
            usedstrings.append(x)
    print("number of permutations = ", len(permutations))

    return permutations


def foo(l, length):
    yield from itertools.product(*([l] * length))


def stringtester(str, permutations):
    sortedlist = sorted(str)
    for i in range(len(permutations)):
        if sorted(permutations[i]) == sortedlist:
            return False

    for i in range(len(sortedlist)):
        for j in range(len(sortedlist)):
            if i != j:
                if sortedlist[i] in sortedlist[j]:
                    return False
    return True


def checkPermutations(permutations, bbtocnf):
    points = []

    for v in permutations:
        x =[]
        neg = False
        for c in v:
            if c == '~':
                neg = True
            elif(neg):
                x.append("~"+c)
                neg = False
            else:
                x.append(c)

        point = 0
        for clause in bbtocnf:
            if '|' in str(clause):
                vars = str(clause).split(" | ")
                for var in vars:
                    if var in x:
                        point = point + 1

            elif '&' in str(clause):
                vars = str(clause).split(" & ")
                for var in vars:
                    if var in x:
                        point = point + 1
            else:
                if str(clause) in x:
                    point = point + 1
        points.append(point)

    print(points)
    print(permutations)


    res = []

    for i in range(len(points)):
        ind = int(points.index(max(points)))
        res.append(permutations[ind])
        points.pop(ind)
        permutations.pop(ind)

    print("------------RES------------")
    print(res)




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
            x1 = split[0]
            x2 = split[1]
            iffs = "(" + x1 + ">>" + x2 + ")" + "&" + "(" + x2 + ">>" + x1 + ")"
            bbtocnf.append(to_cnf(iffs))
        else:
            bbtocnf.append(to_cnf(elements))

    for x in bbtocnf:
        print(x)
        addOperands(str(x))
    print("_________________hey_________________")
    list = revise(operands)
    print("_________________hey_________________")
    checkPermutations(list, bbtocnf)
