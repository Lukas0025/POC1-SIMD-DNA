#!/usr/bin/env python3

from SIMDDNA.register import Register
from SIMDDNA.assembly import Assembly
from SIMDDNA.ascii    import showMolecule
import argparse

parser = argparse.ArgumentParser(description='DNA|SIMD python simulator POC1')
parser.add_argument('assembly')
parser.add_argument('-s', '--spaceing', default=" ", help='space sentense between ascii char of DNA strands')
parser.add_argument('-v', '--verbose', help='show simulation step by step not only final', action='store_true', default=False)
parser.add_argument('-d', '--decode', help='use macros to decode final result', action='store_true', default=False)

args = parser.parse_args()

# Open a file
file = open(args.assembly, mode='r')
asm = file.read()
file.close()

asm = Assembly(asm)

print("=================================")
print("|         Inital state          |")
print("=================================")
print("")

regs = []

for data in asm.getData():
    regs.append(Register(data))
    regs[-1].asciiShow(spaceing = args.spaceing)


iId = 0
for ins in asm.getInstructions():

    if args.verbose:
        print("")
        print("=================================")
        print(f"|        Instruction {iId}         |")
        print("=================================")
        print()

        for insc in ins:
            insc.rawPrint()

        print()
        print("Registers")
        print("--------------------------------")
        print()

    for reg in regs:
        reg.instruction(ins)
        
        if args.verbose:
            reg.asciiShow(spaceing = args.spaceing)

    iId += 1

print("")
print("=================================")
print("|          FINAL state          |")
print("=================================")
print("")

for reg in regs:
    reg.asciiShow(spaceing = args.spaceing)

if args.decode:
    # todo: implement it
    pass