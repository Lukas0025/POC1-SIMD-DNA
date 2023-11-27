##
# @file molecule.py
# @autor Lukáš Plevač <xpleva07@vutbr.cz>
# @brief defines class molecule and functions to work with it

#
# [aa] - double strand of aa (domain a and domain a)
# {aa} - single strand of aa (domain a and domain a) [upper]
# <aa> - single strand of aa (domain a and domain a) [downer]
# 
# example:
# <abc>[ABC].{abc}<C>{ba}.[CC].{CA}
#
#                          c
#                  b    b        A
#                    a        C
#          A* B* C*     C* C*
#          |  |  |      |  |
# a  b  c  A  B  C   C  C  C
#

##
# @brief Char representing space in chain
#
nothing = "-"

##
# Check if two bases is complementary
# @param baseA one of base to check
# @param baseB second of base to check
# @return baseA is complementary to baseB 
#
def isComplementary(baseA, baseB):
    return (f"{baseA}*" == baseB) or (baseA == f"{baseB}*")

##
# Class representing moleculte
#
class Molecule:

    ##
    # Init empty molecule
    #
    def __init__(self):
        self.chains = []

    ##
    # Get length of longest chain in molecule
    # @return int
    #
    def __len__(self):
        return self.maxChainSize()
    
    ##
    # Return number of count of chains in molecule
    # @return int
    #
    def chainsCount(self):
        return len(self.chains)

    ##
    # Pad all chains to same length using insert spaces
    #
    def endPad(self):
        targetSize = self.maxChainSize()

        for id in range(self.chainsCount()):
            while (targetSize > len(self.chains[id])):
                self.chains[id].append(nothing)

    ##
    # Add base to end of chain
    # @param base base to add
    # @param chainId id of chain to add base
    #
    def addToChain(self, base, chainId):
        self.chains[chainId].append(base)

    ##
    # Get chain as array
    # @param chain id of chain
    # @return array of chain
    #
    def getChain(self, chain):
        return self.chains[chain]

    ##
    # Remove chain form molecule
    # @param chainId id of chain
    # @post all chains ids is reindex
    #
    def removeChain(self, chainId):
        del self.chains[chainId]

    ##
    # Get length of longest chain in molecule
    # @return int
    #
    def maxChainSize(self):
        maxLen = 0
        for chain in self.chains:
            maxLen = max(maxLen, len(chain))

        return maxLen

    ##
    # Add chain to end of chain in molecule
    # @param chainID id of chain in molecule to add other chain on end
    # @param chain array reprezentation of chain
    #
    def chain2chain(self, chainID, chain):
        for base in chain:
            self.chains[chainID].append(base)
    
    ##
    # Add spaces to start of chain in molecule
    # @param chainID id of chain in molecule
    # @param count count of spaces
    #
    def padChain(self, chainID, count):
        for _ in range(count):
            self.chains[chainID].insert(0, nothing)

    ##
    # Add spaces to start of chain in molecule by length of other chain in molecule
    # @param chainID id of chain in molecule to pad
    # @param targetID if of chain of len count of spaces
    #
    def padChainToLen(self, chainID, targetID):
        targetSize = len(self.chains[targetID])
        curSize    = len(self.chains[chainID])

        self.padChain(chainID, targetSize - curSize)

    ##
    # Add spaces to start of all chains in molecule
    # @param chainID id of chain in molecule to pad
    # @param count count of spaces
    #
    def padAllChains(self, length):
        for id in range(len(self.chains)):
            self.padChain(id, length)

    ##
    # Add base to end of chain same as addToChain()
    # @param base base to add
    # @param chainId id of chain to add base
    #
    def addBase(self, chainID, base):
        self.chains[chainID].append(base)

    ##
    # Add chain to molecule
    # @return id of new chain
    #
    def addChain(self):
        chainId = len(self.chains)
        self.chains.append([])
        return chainId
    
    ##
    # Update base in chain
    # @param base base to set
    # @param chainId id of chain to add base
    # @param baseID id of base in chain
    #
    def updateBase(self, chainID, baseID, base):
        self.chains[chainID][baseID] = base

    ##
    # Get base from chain
    # @param chainId id of chain to add base
    # @param baseID id of base in chain
    #
    def getBase(self, chainID, baseID):
        return self.chains[chainID][baseID]
    
    ##
    # Get Number of possible binding on position on molecule
    # @param baseID id of base in chain (position in molecule)
    #
    def bindedCountAt(self, baseID):
        binding = 0
        for chain in self.chains:
            if isComplementary(self.chains[0][baseID], chain[baseID]):
                binding += 1

        return binding
    
    ##
    # Add base to end of chain by char represetion
    # A   representing base A
    # A*  representing complement of base A
    # A** representing base A (complement of complement)
    # @param char char represetation of base to add
    # @param chainId id of chain to add base
    # @param isBackward is adding from back to front 
    #        -A (+B)
    #        AB
    #
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

    ##
    # Print raw reprezentation of molecule
    # aligmented chains as string
    #           D
    #     B* C* 
    #  A  B  C  A  B  C
    #
    # Print as:
    #
    #  A  B  C  A  B  C
    #  -  B* C* D* -  -
    #
    def rawPrint(self):
        for chan in self.chains:
            raw = ""
            for base in chan:
                raw += base.ljust(3, " ")

            print(raw)

##
# Convert string notation of molecule to molecule class object
# @param notationStr string notation of molecule
# @return Molecule object
#
# String notation:
# - <> for lower chain
# - [] for double chain
# - {} for upper chain
# - * for complement
# - . for concatenate upper strand with double strand
#
# String notation example:
# <abc>[ABC].{abc}<C>{ba}.[CC].{CA}
#
#                          c
#                  b    b        A
#                    a        C
#          A* B* C*     C* C*
#          |  |  |      |  |
# a  b  c  A  B  C   C  C  C
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

##
# Encode molecule to ASCII reprezentation
# @param mol moleculte to encode
# @retun STR of ascii reprezentation
# @todo support for overhangs
#
def encode(mol):
    outstr = ""
    lastClose = ""
    lastChain = -1
    lastBounded = None
    
    for basePos in range(len(mol)):
        bounded = False
        for chainID in range(1, mol.chainsCount()):
            if isComplementary(mol.getBase(chainID, basePos), mol.getBase(0, basePos)):
                if not lastBounded or lastBounded is None or lastChain != chainID:
                    lastBounded  = True
                    lastChain    = chainID
                    outstr      += lastClose + "["
                    lastClose    = "]"

                bounded = True
                break

        if (not bounded and lastBounded) or lastBounded is None:
            lastBounded = False
            outstr     += lastClose + "{"
            lastClose   = "}"

        if mol.getBase(0, basePos) == nothing:
            break

        outstr += mol.getBase(0, basePos)

    return (outstr + lastClose).replace("{}", "").replace("[]", "")
                