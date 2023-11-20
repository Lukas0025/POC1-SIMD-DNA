class Assembly:
    def __init__(self, asm):
        # remove whitespaces
        asm = asm.strip()
        # load macros from file
        self.macros = self.parseMacros(asm)

    def parseMacros(self, asm):
        