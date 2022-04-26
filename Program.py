from CommandFactory import CommandFactory
import stackmem as sm

class Program:
    def __init__(self, fname):
        self.builder = CommandFactory()
        self.registers = [0 for i in range(34)]
        self.pc = 0
        self.memsize = 0
        self.fname = fname
        self.instrs = []
        self.memaddr = 0
    
    def setup(self):
        memregion = sm.rqmem()
        self.memaddr = memregion[0]
        self.memsize = memregion[1]
        self.registers[0] = 0
        self.registers[30] = memregion[0] + memregion[1]
        self.registers[31] = -1
    
    def __getitem__(self, k):
        return self.instrs[int(k / 4)]

    def twoints(self):
        self.registers[1] = int(input("Enter value for register 1: "))
        self.registers[2] = int(input("Enter value for register 2: "))
        with open(self.fname) as lines:
            for l in lines:
                self.instrs.append(l)
        while self.pc != -1:
            cmd = self.instrs[int(self.pc / 4)]
            self.pc += 4
            self.pc = self.builder.createCmd(cmd).eval(self.registers, self.pc, self)
        print(self.registers)
        sm.fmem(self.memaddr)
