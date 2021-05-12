import itertools

from sympy import to_cnf

operands = []
operandsAssigned = []
truthvals = []
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


def addOperands(x, bool):
    for p in operators:
        if p in str(x):
            split = x.split(p)
            for element in split:
                isNegated(element, bool)
            return
    else:
        isNegated(x, bool)
        return


def isNegated(x, assigned):
    if not assigned:
        if "~" in x:
            listOP(x[1])
        else:
            listOP(x)
    else:
        if "~" in str(x):
            listOPAss(x[1], False)
        else:
            listOPAss(x, True)


def getOP(x):
    for p in operandsAssigned:
        if x == p[0]:
            return p[1]


def andOPor(list, number):
    ops = []
    for x in list:
        if "~" in x:
            ops.append(not getOP(x[1]))
        else:
            ops.append(getOP(x))
    if number == 0:
        return ops[0] or ops[1]
    else:
        return ops[0] and ops[1]


def revise(operands):
    # calculate how many permutations there are of the number of operands
    n = len(operands)
    # append the letters in operand and their negated form
    letters = []
    for x in operands:
        if x not in letters:
            letters.append(x[0]+" ")
            letters.append("~" + x[0]+" ")

    # add a permutation if it holds no duplicates
    permutations = []
    usedstrings = []
    for x in foo(letters, n):
        # if the permutation is a duplicate dont add it
        if not sorted(x) in usedstrings:
            # check if str contains duplicate symbols
            if stringtester(x):
                print(''.join(x))
                permutations.append(''.join(x))
                usedstrings.append(sorted(x))
    print("number of permutations = ", len(permutations))

    return permutations


def foo(l, length):
    yield from itertools.product(*([l] * length))


def stringtester(str):
    sortedlist = sorted(str)

    for i in range(len(sortedlist)):
        for j in range(len(sortedlist)):
            if i != j:
                if sortedlist[i] in sortedlist[j]:
                    return False
    return True

def checkPermutations(permutations, bbtocnf):
    points = []
    global operandsAssigned
    for x in permutations:
        point = 0
        list = x.split(" ")
        for clause in list:
            if clause != "":
                addOperands(clause, True)
        print(operandsAssigned)

        for believestate in bbtocnf:
            sentence = str(believestate)
            if "&" in sentence:
                vars = sentence.split(" & ")
                bools = []
                breakIt = False
                for x in vars:
                    if "|" in x:
                        breakIt = True
                        vals = x.strip("(").strip(")").split(" | ")

                        bools.append(andOPor(vals, 0))
                if breakIt:
                    if (bools[0] and bools[1]):
                        point = point + 1
                else:
                    if andOPor(vars, 1):
                        point = point + 1
            elif "|" in sentence:
                vars = sentence.split(" | ")
                if andOPor(vars, 0):
                    point = point + 1
            else:
                if "~" in sentence:
                    if not getOP(sentence[1]):
                        point = point + 1
                else:
                    if getOP(sentence):
                        point = point + 1

        points.append(point)
        operandsAssigned = []
    print(points)
    res = []
    print("------------RES------------")
    print(sorted(points,reverse=True))
    for i in range(len(points)):
        ind = int(points.index(max(points)))
        res.append(permutations[ind])
        points.pop(ind)
        permutations.pop(ind)
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
        addOperands(str(x), False)
    print("_________________hey_________________")
    list = revise(operands)
    print("_________________hey_________________")
    checkPermutations(list, bbtocnf)
