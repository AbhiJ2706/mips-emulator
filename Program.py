from CommandFactory import CommandFactory
import stackmem as sm

class Program:
    def __init__(self):
        self.builder = CommandFactory()
        self.registers = [0 for i in range(34)]
        self.pc = 0