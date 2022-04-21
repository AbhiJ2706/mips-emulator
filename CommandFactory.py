class InvalidOperationException:
    def __init__(self, what):
        self.cause = what
    def what(self):
        return self.cause

class CommandFactory:

    class Word:
        val = 0
        def eval(self):
            return self.val

    class Add:
        d = 0
        s = 0
        t = 0
        def __init__(self, d, s, t, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs):
            regs[self.d] = regs[self.s] + regs[self.t]

    class Sub:
        pass

    class Mult:
        pass

    class Div:
        pass

    class Multu:
        pass

    class Divu:
        pass

    class Mfhi:
        pass

    class Mflo:
        pass

    class Lis:
        pass

    class Lw:
        pass

    class Sw:
        pass

    class Slt:
        pass

    class Sltu:
        pass

    class Beq:
        pass

    class Bne:
        pass

    class Jr:
        pass

    class Jalr:
        pass

    def createCmd(self, inp):
        cmd3reg = bin(int(inp) and 0b11111100000000000000011111111111)
        cmd2reg = bin(int(inp) and 0b11111100000000001111111111111111)
        cmd1reg = bin(int(inp) and 0b11111100000111111111111111111111)
        cmd2regi = bin(int(inp) and 0b11111100000000000000000000000000)
        match inp:
            case 0b00000000000000000000000000000000:
                pass