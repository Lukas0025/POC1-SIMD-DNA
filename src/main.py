
from SIMDDNA.register import Register
from SIMDDNA          import molecule
from SIMDDNA.assembly import Assembly

asm = Assembly(
"""
define:
    0 [ABC][DE]
    1 {A}[BCDE]

data:
    1001111010

instructions:
    {D*E*A*F*}      # mark 01
    {D*E*A*B*C*G*}  # mark 11
    {DEABCG}        # remove mark 11
    {A*B*C*} {D*E*} # write 0
    {DEAF}          # remove mark 01
    {B*C*D*E*}      # write 1
"""
)

print("=================================")
print("|         Inital state          |")
print("=================================")
print("\n")

regs = []

for data in asm.getData():
    regs.append(Register(molecule.parse(data)))
    regs[-1].asciiShow(spaceing = " ")


iId = 0
for ins in asm.getInstructions():
    print("=================================")
    print(f"|        Instruction {iId}         |")
    print("=================================")
    print("\n")

    for reg in regs:
        reg.instruction(ins)
        reg.asciiShow(spaceing = " ")

    iId += 1