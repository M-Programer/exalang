# In this file:
#
# *INSTRUCTIONS*
#   *MANIPULATION*
#     *InstrCOPY*
#     *InstrADDI*
#     *InstrSUBI*
#     *InstrMULI*
#     *InstrDIVI*
#     *InstrMODI*
#     *InstrSWIZ*
#   *BRANCHING*
#     *InstrMARK*
#     *InstrJUMP*
#     *InstrTJMP*
#     *InstrFJMP*
#   *TESTING*
#     *InstrTEST*
#   *LIFECYCLE*
#     *InstrREPL*
#     *InstrHALT*
#     *InstrKILL*
#   *COMMUNICATION*
#     *InstrMODE*
#   *FILES*
#     *InstrMAKE*
#     *InstrGRAB*
#     *InstrFILE*
#     *InstrSEEK*
#     *InstrDROP*
#     *InstrWIPE*
#   *MISC*
#     *InstrNOTE*
#     *InstrNOOP*
#     *InstrRAND*
# *DICT*
# *get*

import random
from .exa import EXA, File
from os import system

#################################################
# INSTRUCTIONS
#################################################


class Instruction:
    def __init__(self, name, args):
        self.name = name
        self.rawargs = args
        self.mark = False

    def __call__(self, exa):
        # print(self)
        self.run(exa)

    def _checkargs(self, *nums):
        nargs = len(self.rawargs)
        if(nargs in nums):
            return True
        else:
            # TODO: Better error message
            raise Exception(
                f"Invalid instruction {self.name} with {nargs} arguments: {self.rawargs}")

    def __repr__(self):
        return f"<{self.name} {self.rawargs}>"


#################################################
# MANIPULATION
#################################################


class InstrCOPY(Instruction):
    def __init__(self, args):
        super().__init__("COPY", args)
        self._checkargs(2)

        self.src = args[0]
        self.dest = args[1]

    def run(self, exa):
        #print(f"COPY: {self.dest} <- {self.src}")
        exa[self.dest] = exa[self.src]


class InstrADDI(Instruction):
    def __init__(self, args):
        super().__init__("ADDI", args)
        self._checkargs(3)

        self.a = args[0]
        self.b = args[1]
        self.dest = args[2]

    def run(self, exa):
        exa[self.dest] = exa[self.a] + exa[self.b]


class InstrSUBI(Instruction):
    def __init__(self, args):
        super().__init__("ADDI", args)
        self._checkargs(3)

        self.a = args[0]
        self.b = args[1]
        self.dest = args[2]

    def run(self, exa):
        exa[self.dest] = exa[self.a] - exa[self.b]


class InstrMULI(Instruction):
    def __init__(self, args):
        super().__init__("ADDI", args)
        self._checkargs(3)

        self.a = args[0]
        self.b = args[1]
        self.dest = args[2]

    def run(self, exa):
        exa[self.dest] = exa[self.a] * exa[self.b]


class InstrDIVI(Instruction):
    def __init__(self, args):
        super().__init__("ADDI", args)
        self._checkargs(3)

        self.a = args[0]
        self.b = args[1]
        self.dest = args[2]

    def run(self, exa):
        exa[self.dest] = exa[self.a] // exa[self.b]


#################################################
# BRANCHING
#################################################


class InstrMARK(Instruction):
    def __init__(self, args):
        super().__init__("MARK", args)
        self._checkargs(1)
        self.label = args[0]
        self.mark = True

    def run(self, exa):
        pass


class InstrJUMP(Instruction):
    def __init__(self, args):
        super().__init__("JUMP", args)
        self._checkargs(1)
        self.target = args[0]

    def run(self, exa):
        #print(f"[JUMP -> {self.label}]")
        exa.jump(self.target)


class InstrTJMP(Instruction):
    def __init__(self, args):
        super().__init__("TJMP", args)
        self._checkargs(1)
        self.target = args[0]

    def run(self, exa):
        #print(f"[TJMP:{exa.T} -> {self.label}]")
        if(exa.T):
            exa.jump(self.target)


class InstrFJMP(Instruction):
    def __init__(self, args):
        super().__init__("FJMP", args)
        self._checkargs(1)
        self.target = args[0]

    def run(self, exa):
        #	print(f"[FJMP:{exa.T} -> {self.label}]")
        if(not exa.T):
            exa.jump(self.target)


#################################################
# TESTING
#################################################


class InstrTEST(Instruction):
    def __init__(self, args):
        super().__init__("TEST", args)
        self._checkargs(1, 3)
        self.nargs = len(args)
        self.a = args[0]
        if len(args) > 1:
            self.op = args[1]
            self.b = args[2]

    def run(self, exa: EXA):
        if self.nargs > 1:
            left = exa[self.a]
            right = exa[self.b]
            result = None
            if(self.op == "="):
                result = (left == right)
            if(self.op == ">"):
                result = (left > right)
            if(self.op == "<"):
                result = (left < right)

            if(result):
                exa.T = 1
            else:
                exa.T = 0
        elif self.a == "MRD":
            if exa.__class__.M != None:
                exa.T = 1
            else:
                exa.T = 0
        # print(f"({right}{self.op}{left})({exa.T})")

#################################################
# LIFECYCLE
#################################################


class InstrREPL(Instruction):
    def __init__(self, args):
        super().__init__("REPL", args)
        self._checkargs(1)
        self.label = args[0]

    def run(self, exa: EXA):
        xb = EXA(exa.code)
        InstrJUMP([self.label]).run(xb)
        exa.__class__.exas.append(xb)


class InstrHALT(Instruction):
    def __init__(self, args):
        super().__init__("HALT", args)
        self._checkargs(0)

    def run(self, exa):
        exa.halt()


class InstrKILL(Instruction):
    def __init__(self, args):
        super().__init__("KILL", args)
        self._checkargs(0)

    def run(self, exa: EXA):
        killed: EXA = random.choice(exa.exas)
        killed.halt()


#################################################
# COMMUNICATION
#################################################


class InstrMODE(Instruction):
    def __init__(self, args):
        super().__init__("MODE", args)
        self._checkargs(0)

    def run(self, exa):
        exa.switchmode()


#################################################
# FILES
#################################################

FILE_NO = 200


class InstrMAKE(Instruction):
    def __init__(self, args):
        super().__init__("MAKE", args)
        self._checkargs(0)

    def run(self, exa: EXA):
        global FILE_NO
        try:
            open(f"{FILE_NO}.txt", "x").close()
        except FileExistsError:
            pass
        exa.file[File.file] = open(f"{FILE_NO}.txt", "r+")
        FILE_NO += 1


class InstrGRAB(Instruction):
    def __init__(self, args):
        super().__init__("GRAB", args)
        # self._checkargs(1)
        self.file_name = "".join(args)

    def run(self, exa: EXA):
        try:
            open(f"{self.file_name}.txt", "x").close()
        except FileExistsError:
            exa.file[File.file] = open(f"{self.file_name}.txt", "r+")


class InstrFILE(Instruction):
    def __init__(self, args):
        super().__init__("FILE", args)
        self._checkargs(1)
        self.dest = args[0]

    def run(self, exa: EXA):
        exa[self.dest] = exa.file[File.file].name.split(".")[0]


class InstrSEEK(Instruction):
    def __init__(self, args):
        super().__init__("SEEK", args)
        self._checkargs(1)
        self.value = args[0]

    def run(self, exa: EXA):
        exa.file[File.pointer] = self.value


class InstrDROP(Instruction):
    def __init__(self, args):
        super().__init__("DROP", args)
        self._checkargs(0)

    def run(self, exa: EXA):
        exa.file[File.file].close()
        exa.file[File.content] = []
        exa.file[File.pointer] = 0


class InstrWIPE(Instruction):
    def __init__(self, args):
        super().__init__("WIPE", args)
        self._checkargs(0)

    def run(self, exa: EXA):
        filename = exa.file[File.file].name
        InstrDROP().run(exa)
        if system(f"rm {filename}") > 0:
            system(f"del {filename}")


#################################################
# MISC
#################################################


class InstrNOTE(Instruction):
    def __init__(self, args):
        super().__init__("NOTE", args)

    def run(self, exa):
        pass


class InstrNOOP(Instruction):
    def __init__(self, args):
        super().__init__("NOOP", args)
        self._checkargs(0)

    def run(self, exa):
        pass


class InstrRAND(Instruction):
    def __init__(self, args):
        super().__init__("RAND", args)
        self._checkargs(3)
        self.low = args[0]
        self.high = args[1]
        self.dest = args[2]

    def run(self, exa: EXA):
        exa[self.dest] = random.randint(self.low, self.high)


#################################################
# DICT
#################################################


instrs = {
    # Manipulation
    "COPY": InstrCOPY,
    "ADDI": InstrADDI,
    "SUBI": InstrSUBI,
    "MULI": InstrMULI,
    "DIVI": InstrDIVI,
    # Branching
    "MARK": InstrMARK,
    "JUMP": InstrJUMP,
    "TJMP": InstrTJMP,
    "FJMP": InstrFJMP,
    # Testing
    "TEST": InstrTEST,
    # Lifecycle
    "HALT": InstrHALT,
    "REPL": InstrREPL,
    "KILL": InstrKILL,
    # Communication
    "MODE": InstrMODE,
    # Files
    "MAKE": InstrMAKE,
    "GRAB": InstrGRAB,
    "FILE": InstrFILE,
    "SEEK": InstrSEEK,
    "WIPE": InstrWIPE,
    "DROP": InstrDROP,
    # Misc
    "NOTE": InstrNOTE,
    "NOOP": InstrNOOP,
    "RAND": InstrRAND
}


def get(args, lineno=None):
    instrclass = instrs.get(args[0], None)
    if(instrclass):
        return instrclass(args[1:])
    else:
        message = "Invalid instruction \"{name}\""
        if(lineno):
            message += " at line {n}."
        raise Exception(message.format(name=args[0], n=lineno))
