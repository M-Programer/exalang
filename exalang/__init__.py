from . import instrs
from .exa import EXA


def parse(f):
    code = []
    with f:
        for i, line in enumerate(f):
            line = line.upper().rstrip()
            if(line):
                try:
                    line = line[:line.index(";")]
                except ValueError:
                    pass

                split = line.split()
                if(split):
                    instruction = instrs.get(split, lineno=i+1)
                    # print(instruction)
                    code.append(instruction)
                    continue

    return code


def run(f):
    code = parse(f)
    EXA.exas = [EXA(code)]
    while(len(EXA.exas) > 0):
        for i, xa in enumerate(EXA.exas):
            xa()
            # print(xa)
            # print(EXA.exas)
            if(not xa.alive):
                EXA.exas.pop(i)
