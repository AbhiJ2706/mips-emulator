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
        def eval(self, regs, pc, program=-1):
            return self.val

    class Add(BaseOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[self.s] + regs[self.t]
            return pc

    class Sub(BaseOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[self.s] - regs[self.t]
            return pc

    class Mult(BaseOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d != 33: raise InvalidOperationException("Destination register is not hi for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[self.s] * regs[self.t]
            return pc

    class Div(BaseOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d != 32: raise InvalidOperationException("Destination register is not lo for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[self.s] / regs[self.t]
            regs[self.d + 1] = regs[self.s] % regs[self.t]
            return pc

    class Multu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd="0"):
            super()
            if d != 33: raise InvalidOperationException("Destination register is not hi for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = self.unsigned(regs[self.s]) * self.unsigned(regs[self.t])
            return pc

    class Divu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d != 32: raise InvalidOperationException("Destination register is not lo for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] =  self.unsigned(regs[self.s]) /  self.unsigned(regs[self.t])
            regs[self.d + 1] = self.unsigned(regs[self.s]) %  self.unsigned(regs[self.t])
            return pc

    class Mfhi(BaseOperation):
        def __init__(self, d, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[33]
            return pc

    class Mflo(BaseOperation):
        def __init__(self, d, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[32]
            return pc

    class Lis(BaseOperation):
        def __init__(self, d, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program):
            inp = int("0b" + program[pc].strip("\n"), 2)
            regs[self.d] = inp
            pc += 4
            return pc

    class Lw(BaseOperation):
        def __init__(self, s, t, i, cmd="0"):
            self.i = i
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.t] = sm.lwmem(regs[self.s] + self.i * 4)
            return pc

    class Sw(BaseOperation):
        def __init__(self, s, t, i, cmd="0"):
            self.i = i
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            sm.swmem(regs[self.s] + self.i * 4, regs[self.t])
            return pc

    class Slt(BaseOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = regs[self.s] < regs[self.t]
            return pc

    class Sltu(BaseUnsignedOperation):
        def __init__(self, d, s, t, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            regs[self.d] = self.unsigned(regs[self.s]) < self.unsigned(regs[self.t])
            return pc

    class Beq(BaseOperation):
        def __init__(self, s, t, i, cmd="0"):
            self.i = i
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            if regs[self.s] == regs[self.t]:
                pc += self.i * 4
            return pc

    class Bne(BaseOperation):
        def __init__(self, s, t, i, cmd="0"):
            self.i = i
            self.s = s
            self.t = t
        def eval(self, regs, pc, program=-1):
            if regs[self.s] != regs[self.t]:
                pc += self.i * 4
            return pc

    class Jr(BaseOperation):
        def __init__(self, d, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program=-1):
            pc = regs[self.d]
            return pc

    class Jalr(BaseOperation):
        def __init__(self, d, cmd="0"):
            if d == 0: raise InvalidOperationException("Destination register is 0 for command " + cmd)
            self.d = d
        def eval(self, regs, pc, program=-1):
            regs[31] = pc
            pc = regs[self.d]
            return pc

    def process3Regs(self, instr):
        s = int(int(instr) & 0b00000011111000000000000000000000) >> 21
        t = int(int(instr) & 0b00000000000111110000000000000000) >> 16
        d = int(int(instr) & 0b00000000000000001111100000000000) >> 11
        return [d, s, t]
    
    def process2Regs(self, instr):
        s = int(int(instr) & 0b00000011111000000000000000000000) >> 21
        t = int(int(instr) & 0b00000000000111110000000000000000) >> 16
        return [s, t]
    
    def process2Regsi(self, instr):
        s = int(int(instr) & 0b00000011111000000000000000000000) >> 21
        t = int(int(instr) & 0b00000000000111110000000000000000) >> 16
        i = int(int(instr) & 0b00000000000000001111111111111111)
        return [s, t, i]
    
    def process1Reg(self, instr):
        s = int(int(instr) & 0b00000011111000000000000000000000) >> 21
        return s

    def process1Regi(self, instr):
        s = int(int(instr) & 0b00000000000000001111100000000000) >> 11
        return s

    def createCmd(self, inp):
        inp = int("0b" + inp.strip("\n"), 2)
        cmd3reg = inp & 0b11111100000000000000011111111111
        cmd2reg = inp & 0b11111100000000001111111111111111 
        cmd1reg = inp & 0b11111100000111111111111111111111
        cmd1regi = inp & 0b11111111111111110000011111111111
        cmd2regi = inp & 0b11111100000000000000000000000000
        match bin(cmd3reg):
            case "0b100000":
                return CommandFactory.Add(*self.process3Regs(inp))
            case "0b100010":
                return CommandFactory.Sub(*self.process3Regs(inp))
            case "0b101010":
                return CommandFactory.Slt(*self.process3Regs(inp))
            case "0b101011":
                return CommandFactory.Sltu(*self.process3Regs(inp))
        match bin(cmd2reg):
            case "0b11000":
                return CommandFactory.Mult(*self.process2Regs(inp))
            case "0b11001":
                return CommandFactory.Div(*self.process2Regs(inp))
            case "0b11010":
                return CommandFactory.Multu(*self.process2Regs(inp))
            case "0b11011":
                return CommandFactory.Divu(*self.process2Regs(inp))
        match bin(cmd1regi):
            case "0b10000":
                return CommandFactory.Mfhi(self.process1Regi(inp))
            case "0b10010":
                return CommandFactory.Mflo(self.process1Regi(inp))
            case "0b10100":
                return CommandFactory.Lis(self.process1Regi(inp))
        match bin(cmd2regi):
            case "0b10001100000000000000000000000000":
                return CommandFactory.Lw(*self.process2Regsi(inp))
            case "0b10101100000000000000000000000000":
                return CommandFactory.Sw(*self.process2Regsi(inp))
            case "0b10000000000000000000000000000":
                return CommandFactory.Beq(*self.process2Regsi(inp))
            case "0b10100000000000000000000000000":
                return CommandFactory.Bne(*self.process2Regsi(inp))
        match bin(cmd1reg):
            case "0b1000":
                return CommandFactory.Jr(self.process1Reg(inp))
            case "0b1001":
                return CommandFactory.Jalr(self.process1Reg(inp))

            


