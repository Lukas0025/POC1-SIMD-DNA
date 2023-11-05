import molecule
import ascii

class Register:
    def __init__(self, mol = molecule.Molecule()):
        self.set(mol)

    def set(self, mol):
        self.mol = mol

    def inscription(self, IMols):
        for _ in range(1):
            used = False
            for imol in IMols:
                bindIndex, unbindChain = self.getNearestBinding(imol)

                if unbindChain is not None:
                    used = True
                    self.mol.removeChain(unbindChain)

                if bindIndex is not None:
                    used = True
                    chain = self.mol.addChain()
                    self.mol.padChain(chain, bindIndex)
                    self.mol.chain2chain(chain, imol.getChain(0))
                    self.mol.endPad()

            if not used:
                break

    def getNearestBinding(self, imol):
        for chainI in range(self.mol.chainsCount()):
            for aligment in range(len(self.mol)):
                align_score = 0
                for baseID in range(min(len(imol), len(self.mol) - aligment)):
                    if molecule.isComplementary(self.mol.getBase(chainI, baseID + aligment), imol.getBase(0, baseID)):
                        align_score += 1
                    elif align_score > 0:
                        break

                # ok now finded binding
                if align_score >= 2:
                    if chainI == 0:
                        return aligment, None


        return None, None
    
    def show(self):
        return self.mol.rawPrint()

    def asciiShow(self, spaceing = ""):
        return ascii.showMolecule(self.mol, spaceing)


print("---------------------------------")
print("Before")
print("---------------------------------\n")

# create register
myreg = Register(molecule.parse(
    "{EEEBCDEEEBCD}"
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
    molecule.parse("{A*B*C*D*A*}")
])


myreg.show()

myreg.asciiShow()