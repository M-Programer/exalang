import sys
from enum import Enum


class Mode(Enum):
    GLOBAL = 0
    LOCAL = 1


class File(Enum):
    content = "content"
    file = "file"
    pointer = "pointer"


class EXA:
    M = None
    exas = []

    def __init__(self, code, ip=0):
        self.code = code
        self.ip = ip
        self.alive = True

        self.X = 0
        self.T = 0

        self.mode = Mode.GLOBAL
        self.file = {
            "content": [],
            "file": None,
            "pointer": 0,
        }

    def switchmode(self):
        if(self.mode == Mode.GLOBAL):
            self.mode == Mode.LOCAL
        else:
            self.mode == Mode.GLOBAL

    def halt(self):
        self.running = False

    def jump(self, label):
        for i, line in enumerate(self.code):
            if(line.mark and line.label == label):
                self.ip = i
                # print(f"[Jumping to {label}. IP={self.ip} {self.code[self.ip]}]")
                return
        raise Exception(f"Label {label} not found.")

    def __call__(self):
        # print(self)
        if(self.ip >= len(self.code)):
            self.alive = False
            return

        self.code[self.ip](self)
        self.ip += 1

    def __getitem__(self, value):
        try:
            return int(value)
        except:
            if(value == "X"):
                return self.X
            elif(value == "T"):
                return self.T
            elif(value == "M"):
                return self.__class__.M
            elif(value == "F"):
                val = self.file[File.content][self.file[File.pointer]]
                self.file[File.pointer] += 1
                return val
            elif(value == "#STDI"):
                read = sys.stdin.read(1)
                return ord(read[0]) if read else -1

        raise Exception("invalid value/register {}".format(value))

    def __setitem__(self, name, value):
        if(name == "X"):
            self.X = self[value]
        elif(name == "T"):
            self.T = self[value]
        elif(name == "M"):
            self.__class__.M = self[value]
        elif(name == "F"):
            self.file[File.content][self.file[File.pointer]] = self[value]
            self.file[File.pointer] += 1
        elif(name == "#STDO"):
            c = chr(value)
            sys.stdout.write(c)
        elif(name == "#STDE"):
            c = chr(value)
            sys.stderr.write(c)
        else:
            raise Exception("invalid value/register {}".format(value))

    def __repr__(self):
        return f"<EXA(X={self.X},T={self.T}) M={self.__class__.M}>"
