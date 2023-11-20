import re
from . import molecule

class Assembly:
    def __init__(self, asm):
        # load macros from file
        self.macros = self.parseMacros(asm)
        self.data   = self.parseData(asm)
        self.ins    = self.parseInstructions(asm)

    def getMacros(self):
        return self.macros

    def getData(self):
        return self.data
    
    def getInstructions(self):
        return self.ins

    def parseMacros(self, asm):
        asm = asm.splitlines()

        is_in = False
        macros = []
        for ins in asm:
            ins = re.sub("\s+" , " ", ins.strip()) # remove whitespaces
            ins = ins.split("#")[0] # remove comments
            
            if "define:" in ins:
                is_in = True
            elif ":" in ins and is_in:
                break
            elif is_in:
                name = ins.split(" ")[0]

                if not name.isspace() and len(name) > 0:
                    val = ins.split(" ")[1]

                    macros.append([name, val])

        return macros

    def useMacros(self, text):
        for macro in self.macros:
            text = text.replace(macro[0], macro[1])

        return text
    
    def parseData(self, asm):
        asm = asm.splitlines()

        is_in = False
        datas = []
        for ins in asm:
            ins = re.sub("\s+" , " ", ins.strip()) # remove whitespaces
            ins = ins.split("#")[0] # remove comments
            
            if "data:" in ins:
                is_in = True
            elif ":" in ins and is_in:
                break
            elif is_in:
                reg = ins.split(" ")

                if len(reg) > 1:
                    print("WARNING: ASM parsing data molecule with space. All after space is ignored!")

                reg = reg[0]

                if not reg.isspace() and len(reg) > 0:
                    datas.append(molecule.parse(self.useMacros(reg)))

        return datas        

    def parseInstructions(self, asm):
        asm = asm.splitlines()

        is_in = False
        gins = []
        for ins in asm:
            ins = re.sub("\s+" , " ", ins.strip()) # remove whitespaces
            ins = ins.split("#")[0] # remove comments
            
            if "instructions:" in ins:
                is_in = True
            elif ":" in ins and is_in:
                break
            elif is_in:
                DNAins = ins.split(" ")

                DNAInsArray = []
                for DNAin in DNAins:
                    if not DNAin.isspace() and len(DNAin) > 0:
                        DNAInsArray.append(molecule.parse(self.useMacros(DNAin)))

                if len(DNAInsArray) > 0:
                    gins.append(DNAInsArray)

        return gins     

