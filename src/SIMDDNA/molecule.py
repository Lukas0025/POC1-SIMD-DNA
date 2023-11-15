#
# [aa] - double strand of aa (domain a and domain a)
# {aa} - single strand of aa (domain a and domain a) [upper]
# <aa> - single strand of aa (domain a and domain a) [downer]
# 
# example:
# <abc>[ABC]*{abc}<C>{ba}*[CC]*{CA}
#
#                          c
#                  b    b        A
#                    a        C
#          A* B* C*     C* C*
#          |  |  |      |  |
# a  b  c  A  B  C   C  C  C
#

nothing = "-"

def isComplementary(baseA, baseB):
    return (f"{baseA}*" == baseB) or (baseA == f"{baseB}*")

class Molecule:
    def __init__(self):
        self.chains = []

    def __len__(self):
        return self.maxChainSize()

    def chainsCount(self):
        return len(self.chains)

    def endPad(self):
        targetSize = self.maxChainSize()

        for id in range(self.chainsCount()):
            while (targetSize > len(self.chains[id])):
                self.chains[id].append(nothing)

    def addToChain(self, base, chainId):
        self.chains[chainId].append(base)

    def getChain(self, chain):
        return self.chains[chain]

    def removeChain(self, chainId):
        del self.chains[chainId]

    def maxChainSize(self):
        maxLen = 0
        for chain in self.chains:
            maxLen = max(maxLen, len(chain))

        return maxLen

    def chain2chain(self, chainID, chain):
        for base in chain:
            self.chains[chainID].append(base)
    
    def padChain(self, chainID, count):
        for _ in range(count):
            self.chains[chainID].insert(0, nothing)

    def padChainToLen(self, chainID, targetID):
        targetSize = len(self.chains[targetID])
        curSize    = len(self.chains[chainID])

        self.padChain(chainID, targetSize - curSize)

    def padAllChains(self, length):
        for id in range(len(self.chains)):
            self.padChain(id, length)

    def addBase(self, chainID, base):
        self.chains[chainID].append(base)

    def addChain(self):
        chainId = len(self.chains)
        self.chains.append([])
        return chainId
    
    def updateBase(self, chainID, baseID, base):
        self.chains[chainID][baseID] = base

    def getBase(self, chainID, baseID):
        return self.chains[chainID][baseID]
    
    def bindedCountAt(self, baseID):
        binding = 0
        for chain in self.chains:
            if isComplementary(self.chains[0][baseID], chain[baseID]):
                binding += 1

        return binding
    
    def charAddBase(self, chainID, char, isBackward = False):
        if isBackward:
            if len(self.chains[chainID]) == 0 or self.getBase(chainID, 0) != nothing:
                self.padAllChains(1)
            
            del self.chains[chainID][0]

        if char == "*":
            curBase = self.getBase(chainID, -1)
            if curBase[-1] == "*":
                self.updateBase(chainID, -1, f"{curBase[0]}")
            else:
                self.updateBase(chainID, -1, f"{curBase}*")
        else:
            self.addBase(chainID, char)
    
    def rawPrint(self):
        for chan in self.chains:
            raw = ""
            for base in chan:
                raw += base.ljust(3, " ")

            print(raw)

def parse(notationStr):
    newMolecule  = Molecule()
    state        = "init"
    lowerChain   = newMolecule.addChain()
    lastChain    = None
    isBackward   = False
    workingChain = None

    for char in notationStr:
        
        # check if is not whitespace
        if char.isspace():
            continue

        if state == "init":
            
            if   char == "{":
                lastChain = state = "lower"
            elif char == "[":
                lastChain = state = "double"
            elif char == "<":
                lastChain = state = "upper"
            elif char == ".":
                if lastChain is not None and lastChain != "lower":
                    workingChain = -1
                else:
                    print("lastchain is none or lower but have . (chain concatenation operation)")
                    exit(1)
            else:
                print("Parsing error expecting <, [, { or . but have " + char)
                exit(1)

        elif state == "lower":
            if char == "}":
                state = "init"
                continue

            newMolecule.charAddBase(lowerChain, char)

        elif state == "upper":
            if char == ">":
                workingChain = None
                isBackward   = False
                state        = "init"
                continue

            if workingChain is None:
                isBackward   = True
                workingChain = newMolecule.addChain()
                newMolecule.padChainToLen(workingChain, lowerChain)

            newMolecule.charAddBase(workingChain, char, isBackward)
            
        elif state == "double":
            if char == "]":
                workingChain = None
                state        = "init"
                continue

            if workingChain is None:
                workingChain = newMolecule.addChain()
                newMolecule.padChainToLen(workingChain, lowerChain)

            newMolecule.charAddBase(lowerChain,   char)
            newMolecule.charAddBase(workingChain, char)

            if char != "*":
                newMolecule.charAddBase(workingChain, "*")

    newMolecule.endPad()

    return newMolecule