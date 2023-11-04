import molecule
import ascii

class Register:
    def __init__(self, mol = molecule.Molecule()):
        self.set(mol)

    def set(self, mol):
        self.mol = mol

    def inscription(self, IMols):
        pass

    def asciiShow(self, spaceing = ""):
        return ascii.showMolecule(self.mol, spaceing)


print("---------------------------------")
print("Before")
print("---------------------------------\n")

# create register
myreg = Register(molecule.parse(
    "<AB>[CD]"
))

myreg.asciiShow()

print("\n---------------------------------")
print("After")
print("---------------------------------\n")

# do inscription
myreg.inscription([
    molecule.parse("{A*B*C*D*E*}"),
    molecule.parse("<ABCDE>")
])

myreg.asciiShow()