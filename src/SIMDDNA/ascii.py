from molecule import isComplementary
from molecule import nothing

def toBindingLen(chainID, curPOS, molecule):
    toBLen = 0

    # is in front
    for basePos in range(curPOS, len(molecule)):
        if molecule.getBase(chainID, basePos) != nothing:
            if isComplementary(molecule.getBase(chainID, basePos), molecule.getBase(0, basePos)):
                #if only this binded here
                if molecule.bindedCountAt(basePos) == 1:
                    return toBLen
            
        toBLen += 1

    toBLen = 0

    # is in back
    for basePos in range(curPOS, -1, -1):
        if molecule.getBase(chainID, basePos) != nothing:
            if isComplementary(molecule.getBase(chainID, basePos), molecule.getBase(0, basePos)):
                if molecule.bindedCountAt(basePos) == 1:
                    return toBLen
            
        toBLen -= 1


    return None

def showMolecule(molecule, spacing = ""):
    Invlines = [
        "", # register strand
        "", # binding strand
        "", # data strand
    ]

    for basePos in range(len(molecule)):
            
        if molecule.getBase(0, basePos) == nothing:
            Invlines[0] += " "
        else:
            Invlines[0] += "-"

        # find binded bases
        bounded = False
        for chainID in range(1, molecule.chainsCount()):

            if molecule.getBase(chainID, basePos) == nothing:
                continue

            lenToBinding = toBindingLen(chainID, basePos, molecule)

            if lenToBinding is None:
                print(f"Warning: no binded for chain {chainID}")

            elif lenToBinding == 0:
                bounded     = True
                    
                Invlines[1] += "|"

                if (basePos + 1 == len(molecule)) or (molecule.getBase(chainID, basePos + 1) == "-"):
                    Invlines[2] += ">"
                elif not isComplementary(molecule.getBase(chainID, basePos + 1), molecule.getBase(0, basePos + 1)):
                    Invlines[2] += "/"
                elif basePos > 0 and molecule.getBase(chainID, basePos - 1) != nothing and not isComplementary(molecule.getBase(chainID, basePos - 1), molecule.getBase(0, basePos - 1)):
                    Invlines[2] += "\\"
                else:
                    Invlines[2] += "-"

            elif lenToBinding > 0:
                for _ in range(lenToBinding - len(Invlines) + 3):
                    Invlines.append("")

                for _ in range(basePos - len(Invlines[lenToBinding + 2])):
                    Invlines[lenToBinding + 2] += " "

                if len(Invlines[lenToBinding + 2]) > basePos and (Invlines[lenToBinding + 2][basePos] == "/"):
                    Invlines[lenToBinding + 2] = Invlines[lenToBinding + 2][:-1] + 'X'
                else:
                    Invlines[lenToBinding + 2] += "\\"

            elif lenToBinding < 0:
                lenToBinding = abs(lenToBinding)

                for _ in range(lenToBinding - len(Invlines) + 3):
                    Invlines.append("")

                for _ in range(basePos - len(Invlines[lenToBinding + 2])):
                    Invlines[lenToBinding + 2] += " "

                if len(Invlines[lenToBinding + 2]) > basePos and (Invlines[lenToBinding + 2][basePos] == "\\"):
                    Invlines[lenToBinding + 2] = Invlines[lenToBinding + 2][:-1] + 'X'
                else:
                    Invlines[lenToBinding + 2] += "/"

        if not bounded:
            Invlines[1] += " "
            Invlines[2] += " "

    for line in reversed(Invlines):
        print(spacing.join(line))

    # print bases in bottom
    label = []
    for i in range(len(molecule)):
        if (molecule.getBase(0, i) != nothing):
            label.append(molecule.getBase(0, i) + spacing)
        else:
            label.append(" " + spacing)

    print("".join(label))