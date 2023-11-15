import molecule
import ascii

class Register:
    def __init__(self, mol = molecule.Molecule()):
        self.set(mol)

    def set(self, mol):
        self.mol = mol

    def inscription(self, IMols):
        for mol in IMols:
            self.doAllBinding(mol)
            self.removeUnbinded()
            self.removeReplaced()
            self.removeUnstable()
        
    def removeReplaced(self):
        while True:
            done = True
            # for all chains in register
            # primary detach newer 
            for chainI in range(self.mol.chainsCount() - 1, 0, -1):
                # for all bases in molecule
                binded = False
                for pos in range(len(self.mol)):
                    if molecule.isComplementary(self.mol.getBase(chainI, pos), self.mol.getBase(0, pos)) and self.mol.bindedCountAt(pos) == 1: # binde minimaly once

                        binded = True
                        break

                if not(binded):
                    self.mol.removeChain(chainI)
                    done = False
                    break

            
            if done:
                break

    def removeUnbinded(self):
        while True:
            done = True
            # for all chains in register
            for chainIA in range(1, self.mol.chainsCount()):
                for chainIB in range(1, self.mol.chainsCount()):
                    # for all bases in molecule
                    bindScore = 0
                    for pos in range(len(self.mol)):
                        if not(molecule.isComplementary(self.mol.getBase(chainIA, pos), self.mol.getBase(chainIB, pos))):
                            if not(self.mol.getBase(chainIB, pos) == molecule.nothing and self.mol.getBase(chainIA, pos) == molecule.nothing):
                                bindScore -= 1

                    if bindScore == 0:
                        self.mol.removeChain(max(chainIA, chainIB))
                        self.mol.removeChain(min(chainIA, chainIB))
                        done = False
                        break

                if not(done):
                    break
            
            if done:
                break

    def removeUnstable(self):
        while True:
            done = True
            # for all chains in register
            # primary detach newer 
            for chainI in range(self.mol.chainsCount() - 1, 0, -1):
                # for all bases in molecule
                bindScore = 0
                for pos in range(len(self.mol)):
                    if molecule.isComplementary(self.mol.getBase(chainI, pos), self.mol.getBase(0, pos)) and self.mol.bindedCountAt(pos) == 1: # binde minimaly once
                        bindScore += 1

                if bindScore < 2:
                    self.mol.removeChain(chainI)
                    done = False
                    break

            
            if done:
                break

    def doAllBinding(self, imol):
        # for all chains in register
        for chainI in range(self.mol.chainsCount()):
            # for all possible aligment in molecule
            for aligment in range(len(self.mol)):
                # calculate align score for all possible aligments
                align_score = 0
                for baseID in range(min(len(imol), len(self.mol) - aligment)):
                    if molecule.isComplementary(self.mol.getBase(chainI, baseID + aligment), imol.getBase(0, baseID)):
                        align_score += 1
                    elif align_score < 2:
                        align_score = 0
                    
                    # this will definitly bind
                    if align_score >= 2:
                        break

                # ok now finded binding
                if align_score >= 2:
                    chain = self.mol.addChain()
                    self.mol.padChain(chain, aligment)
                    self.mol.chain2chain(chain, imol.getChain(0))
                    self.mol.endPad()
    
    def show(self):
        return self.mol.rawPrint()

    def asciiShow(self, spaceing = ""):
        return ascii.showMolecule(self.mol, spaceing)


print("---------------------------------")
print("Before")
print("---------------------------------\n")

# create register
num1 = "{A}[BCDE]"
num0 = "[ABC][DE]"

myreg = Register(molecule.parse(
    num1 + num0 + num0 + num1 + num1 + num1 + num1 + num0 + num1 + num0
))

myreg.asciiShow()

print("\n---------------------------------")
print("After")
print("---------------------------------\n")

# do inscription
# mark
# myreg.inscription([
#    molecule.parse("<A*B*C*D*E*>")
# ])

# do instruction
# remove

myreg.inscription([
    molecule.parse("{D*E*A*F*}")
])

myreg.asciiShow(" ")

myreg.inscription([
    molecule.parse("{D*E*A*B*C*G*}")
])

myreg.asciiShow(" ")

myreg.inscription([
    molecule.parse("{DEABCG}")
])

myreg.asciiShow(" ")

myreg.inscription([
    molecule.parse("{A*B*C*}"),
    molecule.parse("{D*E*}")
])

myreg.asciiShow(" ")

myreg.inscription([
    molecule.parse("{DEAF}")
])

myreg.asciiShow(" ")

myreg.inscription([
    molecule.parse("{B*C*D*E*}")
])

myreg.asciiShow(" ")