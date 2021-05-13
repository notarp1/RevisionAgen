import itertools

from sympy import to_cnf

operands = []
operandsAssigned = []
truthvals = []
operators = [" & ", " | "]
symbol = "abcdefghijklmnopqrstuvwxyz"
test ="<->"



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


def getPermu(operands):
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

def recursive(belief):
    if "&" in belief:
        bool = []
        list = belief.split(" & ")
        for x in list:
            bool.append(recursive(x))
        return bool[0] and bool[1]
    if "|" in belief:
        list2 = belief.strip("(").strip(")").split(" | ")
        return andOPor(list2, 0)
    else:
        if "~" in belief:
            return(getOP(belief[1]))
        else:
            return(getOP(belief))


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
    #
        for believestate in bbtocnf:
            sentence = str(believestate)
            if recursive(sentence):
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
    return res

#Recursive funciton to convert biconditional symbols to implication symbols
def recursiveBiConditional(word, count):
    count = count + 1
    if count == 1:
        newWord=""
    bi = "<->"
    if bi not in word:
        return newWord
    if "&" in word:
        list = word.split("&")
        newWord= newWord + recursiveBiConditional(list[0], count)
        newWord = newWord + "&"
        newWord = newWord + recursiveBiConditional(list[1], count)
    elif "|" in word:
        list = word.split("|")
        newWord= newWord + recursiveBiConditional(list[0], count)
        newWord = newWord + "|"
        newWord = newWord + recursiveBiConditional(list[1], count)
    else:
        split = word.split("<->")
        x1 = split[0]
        x2 = split[1]
        iffs = "(" + x1 + ">>" + x2 + ")" + "&" + "(" + x2 + ">>" + x1 + ")"
        return iffs
    return newWord

def revise(clause,sortedStates):

    for c in bbtocnf:
        if contradict(c,clause):
            bbtocnf.pop(bbtocnf.index(c))
    bbtocnf.append(clause)

def contradict(clause1,newClause):

    return False


if __name__ == '__main__':
    print("Enter belief state, seperated by comma")
    print("Valid operands: '|', '&', '>>', '<->'")
    bb = input()
    list = bb.split(",")

    bbtocnf = []
    inverted = []
    for elements in list:
        if "<->" in elements:
            word = recursiveBiConditional(elements, 0)
            bbtocnf.append(to_cnf(word))
        else:
            bbtocnf.append(to_cnf(elements))

    for x in bbtocnf:
        print(x)
    for x in symbol:
        for p in str(bbtocnf):
            if x in p:
                addOperands(str(x), False)
    print("_________________hey_________________")
    list = getPermu(operands)
    print("_________________hey_________________")
    sortedList = checkPermutations(list, bbtocnf)
    print(sortedList)
    while True:
        print("Valid operands: '|', '&', '>>', '<->'")
        print("EXIT to end program")
        line = input()
        opp = []

        if line == "EXIT":
            break
        else:
            for c in line:
                if c in symbol and c in operands:
                    revise(to_cnf(line), sortedList)
                    break

            bbtocnf.append(to_cnf(line))


