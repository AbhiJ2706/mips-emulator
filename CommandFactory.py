import stackmem as sm

class InvalidOperationException:
    def __init__(self, what):
        self.cause = what
    def what(self):
        return self.cause

class CommandFactory:

    class BaseOperation:
        pass

    class BaseUnsignedOperation:
        def unsigned(x):
            return x if x >= 0 else x + 2 ** 32

    class Word(BaseOperation):
        def __init__(self, val):
            self.val = val
        def eval(self, regs=[], pc=0, program=-1):
            return self.val

    class Add(BaseOperation):
        def __init__(self, d, s, t, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[self.s] + regs[self.t]

    class Sub(BaseOperation):
        def __init__(self, d, s, t, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[self.s] - regs[self.t]

    class Mult(BaseOperation):
        def __init__(self, d, s, t, cmd=0):
            if d != 33: raise InvalidOperationException("Destination register is not hi for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[self.s] * regs[self.t]

    class Div(BaseOperation):
        def __init__(self, d, s, t, cmd=0):
            if d != 32: raise InvalidOperationException("Destination register is not lo for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[self.s] / regs[self.t]
            regs[self.d + 1] = regs[self.s] % regs[self.t]

    class Multu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd=0):
            super()
            if d != 33: raise InvalidOperationException("Destination register is not hi for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = self.unsigned(regs[self.s]) * self.unsigned(regs[self.t])

    class Divu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd=0):
            if d != 32: raise InvalidOperationException("Destination register is not lo for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] =  self.unsigned(regs[self.s]) /  self.unsigned(regs[self.t])
            regs[self.d + 1] = self.unsigned(regs[self.s]) %  self.unsigned(regs[self.t])

    class Mfhi(BaseOperation):
        def __init__(self, d, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[33]

    class Mflo(BaseOperation):
        def __init__(self, d, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[32]

    class Lis(BaseOperation):
        def __init__(self, d, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program):
            regs[self.d] = program[pc + 4]
            pc += 4

    class Lw(BaseOperation):
        pass

    class Sw(BaseOperation):
        pass

    class Slt(BaseOperation):
        def __init__(self, d, s, t, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = regs[self.s] < regs[self.t]

    class Sltu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd=0):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc=0, program=-1):
            regs[self.d] = self.unsigned(regs[self.s]) < self.unsigned(regs[self.t])

    class Beq(BaseOperation):
        pass

    class Bne(BaseOperation):
        pass

    class Jr(BaseOperation):
        pass

    class Jalr(BaseOperation):
        pass

    def createCmd(self, inp):
        cmd3reg = bin(int(inp) and 0b11111100000000000000011111111111)
        cmd2reg = bin(int(inp) and 0b11111100000000001111111111111111)
        cmd1reg = bin(int(inp) and 0b11111100000111111111111111111111)
        cmd1regi = bin(int(inp) and 0b11111111111111110000011111111111)
        cmd2regi = bin(int(inp) and 0b11111100000000000000000000000000)
        match cmd3reg:
            case 0b00000000000000000000000000100000:
                pass
            case 0b00000000000000000000000000100010:
                pass
            case 0b00000000000000000000000000101010:
                pass
            case 0b00000000000000000000000000101011:
                pass
        match cmd2reg:
            case 0b00000000000000000000000000011000:
                pass
            case 0b00000000000000000000000000011001:
                pass
            case 0b00000000000000000000000000011010:
                pass
            case 0b00000000000000000000000000011011:
                pass
        match cmd1regi:
            case 0b00000000000000000000000000010000:
                pass
            case 0b00000000000000000000000000010010:
                pass
            case 0b00000000000000000000000000010100:
                pass
        match cmd2regi:
            case 0b10001100000000000000000000000000:
                pass
            case 0b10101100000000000000000000000000:
                pass
            case 0b00010000000000000000000000000000:
                pass
            case 0b00010100000000000000000000000000:
                pass
        match cmd1reg:
            case 0b00000000000000000000000000001000:
                pass
            case 0b00000000000000000000000000001001:
                pass

            


