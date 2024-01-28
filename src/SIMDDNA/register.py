##
# @file register.py
# @autor Lukáš Plevač <xpleva07@vutbr.cz>
# @brief implments REGISTER from SIMD|DNA

from . import molecule
from . import ascii

from joblib import Parallel, delayed

class Register:
    ##
    # Init register
    # @param mol molecule reprezenting register
    #
    def __init__(self, mol = molecule.Molecule()):
        self.set(mol)

    ##
    # set register molecule
    # @param mol molecule reprezenting register
    #
    def set(self, mol):
        self.mol = mol

    ##
    # Perform instruction on register
    # @param mol molecule reprezenting register
    #
    def instruction(self, IMols):
        # @todo: while chainging
        for _ in range(20):
            for mol in IMols:
                # try bind mol to all possible bindings
                self.doAllBinding(mol)

            for mol in IMols:
                # remove unbinded chains from register (because new imol have bind on older chain with more bases that register)
                # ---
                # |||
                # ---
                #
                # ---- R
                self.removeUnbinded()

            for mol in IMols:
                # remove unbinded chains from register (because new imol have bind on more posisin on register that older)
                # --
                #
                # ---
                # |||
                # ---- R
                self.removeReplaced()

            for mol in IMols:
                # remove all unstable binded chains binded on 1 base or lower
                self.removeUnstable()

        return self


    ##
    # remove unbinded chains from register (because new imol have bind on more posisin on register that older)
    # --
    #
    # ---
    # |||
    # ---- R
    #
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

    ##
    # remove unbinded chains from register (because new imol have bind on older chain with more bases that register)
    # ---
    # |||
    # ---
    #
    # ---- R
    #
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

                    # chack if strand have any free binding base to strap it
                    if bindScore == 0 and self.haveChainFreeBaseFor(chainIA, chainIB) and self.haveChainFreeBaseFor(chainIB, chainIA):
                        self.mol.removeChain(max(chainIA, chainIB))
                        self.mol.removeChain(min(chainIA, chainIB))
                        done = False
                        break

                if not(done):
                    break
            
            if done:
                break

    ##
    # remove all unstable binded chains binded on 1 base or lower
    def removeUnstable(self):
        while True:
            done = True
            # for all chains in register
            # primary detach newer 
            for chainI in range(1, self.mol.chainsCount()):
                # for all bases in molecule
                bindScore = 0
                finalBindScore = 0
                for pos in range(len(self.mol)):
                    if molecule.isComplementary(self.mol.getBase(chainI, pos), self.mol.getBase(0, pos)) and self.mol.bindedCountAt(pos) == 1: # binde minimaly once
                        bindScore += 1
                    elif not molecule.isComplementary(self.mol.getBase(chainI, pos), self.mol.getBase(0, pos)):
                        finalBindScore = max(bindScore, finalBindScore)
                        bindScore      = 0

                if max(bindScore, finalBindScore) < 2:
                    self.mol.removeChain(chainI)
                    done = False
                    break

            
            if done:
                break

    def haveChainFreeBaseFor(self, chainA, chainB):
        for baseID in range(len(self.mol)):
            if molecule.isComplementary(self.mol.getBase(chainA, baseID), self.mol.getBase(chainB, baseID)):
                if not molecule.isComplementary(self.mol.getBase(chainA, baseID), self.mol.getBase(0, baseID)):
                    return True
                elif self.mol.bindedCountAt(baseID) >= 2:
                    return True
                
        return False

    ##
    # try bind mol to all possible bindings
    # Added all imol bindings as new chains
    # do not chech if other chain is ocupation this postion
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
    
    ##
    # Show register with raw print molecule
    def show(self):
        return self.mol.rawPrint()

    ##
    # Show register with ascii reprezentation of molecule
    def asciiShow(self, spaceing = ""):
        return ascii.showMolecule(self.mol, spaceing)