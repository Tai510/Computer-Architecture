"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    
    OPCODES = {
    "ADD":  {"type": 2, "code": "10100000"},
    "AND":  {"type": 2, "code": "10101000"},
    "CALL": {"type": 1, "code": "01010000"},
    "CMP":  {"type": 2, "code": "10100111"},
    "DEC":  {"type": 1, "code": "01100110"},
    "DIV":  {"type": 2, "code": "10100011"},
    "HLT":  {"type": 0, "code": "00000001"},
    "INC":  {"type": 1, "code": "01100101"},
    "INT":  {"type": 1, "code": "01010010"},
    "IRET": {"type": 0, "code": "00010011"},
    "JEQ":  {"type": 1, "code": "01010101"},
    "JGE":  {"type": 1, "code": "01011010"},
    "JGT":  {"type": 1, "code": "01010111"},
    "JLE":  {"type": 1, "code": "01011001"},
    "JLT":  {"type": 1, "code": "01011000"},
    "JMP":  {"type": 1, "code": "01010100"},
    "JNE":  {"type": 1, "code": "01010110"},
    "LD":   {"type": 2, "code": "10000011"},
    "LDI":  {"type": 8, "code": "10000010"},
    "MOD":  {"type": 2, "code": "10100100"},
    "MUL":  {"type": 2, "code": "10100010"},
    "NOP":  {"type": 0, "code": "00000000"},
    "NOT":  {"type": 1, "code": "01101001"},
    "OR":   {"type": 2, "code": "10101010"},
    "POP":  {"type": 1, "code": "01000110"},
    "PRA":  {"type": 1, "code": "01001000"},
    "PRN":  {"type": 1, "code": "01000111"},
    "PUSH": {"type": 1, "code": "01000101"},
    "RET":  {"type": 0, "code": "00010001"},
    "SHL":  {"type": 2, "code": "10101100"},
    "SHR":  {"type": 2, "code": "10101101"},
    "ST":   {"type": 2, "code": "10000100"},
    "SUB":  {"type": 2, "code": "10100001"},
    "XOR":  {"type": 2, "code": "10101011"},
    }
    opCodeMap = {}
    for op, x in OPCODES.items():
        opCodeMap[int("0b" + x["code"],2)] = op

    def getOperation(self, opcode):
        if opcode in self.opCodeMap:
            return self.opCodeMap[opcode]
    print("OPCODE library > ", opCodeMap)


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg=[0]*8
        self.pc=0
        self.ir=0
        self.SP=7
        self.Flags = [0]*8


    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue  # Ignore blank lines ​
                    value = int(num,2)   # Base 10, but ls-8 is base 2  
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self,MAR):
        
        return self.ram[MAR]

    def ram_write(self,MAR,MDR):
        self.ram[MAR]=MDR

    def run(self):
        """Run the CPU."""
        # for i in self.ram:
        #     print(i)
        Running=True
        # print(chr(self.ram_read(self.pc)))
        LDI=0b10000010
        HLT=0b00000001
        PRN=0b01000111 
        MUL=0b10100010
        PUSH=0b01000101
        POP=0b01000110
        CALL=0b01010000
        RET=0b00010001
        ADD=0b10100000
        CMP=0b10100111
        JMP=0b01010100
        JEQ=0b01010101
        JNE=0b01010110
        L= 0
        E= 0
        G= 0

        while Running:


            Command=self.ram_read(self.pc)
            # print(Command)
            if Command == LDI:
                # print("LDI")
                operand_a=self.ram_read(self.pc+1)
                operand_b=self.ram_read(self.pc+2)
                self.reg[operand_a]=operand_b
                # print("LDI", self.reg)
                self.pc+=3
                # print(self.reg)
            elif Command == HLT:
                print("HLT")
                Running=False
                self.pc+=1
            elif Command == PRN:
                # print("PRN", self.reg)
                reg = self.ram[self.pc + 1]
                # self.reg=self.ram[self.pc+1]
                print(self.reg[reg])
                self.pc+=2
            elif Command== MUL:
                # print("MUL")
                operand_a=self.ram_read(self.pc+1)
                operand_b=self.ram_read(self.pc+2)
                self.reg[operand_a]=self.reg[operand_a]*self.reg[operand_b]
                self.pc+=3
            elif Command==PUSH:
                # print("PUSH")
                reg=self.ram[self.pc+1]
                val=self.reg[reg]
                self.SP-=1
                self.ram[self.reg[self.SP]]= val
                self.pc+=2
                
            elif Command==POP:
                # print("POP")
                reg=self.ram[self.pc+1]
                val=self.ram[self.reg[self.SP]]
                self.reg[reg]=val
                self.reg[self.SP] += 1
                self.pc+=2

            elif Command == CALL:
                val=self.pc+2
                
                reg=self.ram[self.pc+1]
                subroutine_address=self.reg[reg]
                self.reg[self.SP]-=1  
                self.ram[self.reg[self.SP]]=val

                self.pc=subroutine_address  
            
            elif Command ==ADD:
                self.alu("ADD",self.ram_read(self.pc+1),self.ram_read(self.pc+2))
                self.pc+=3

            elif Command == RET:
                return_address=self.reg[self.SP]
                self.pc=self.ram[return_address]

                self.reg[self.SP]+=1
            elif Command==CMP:
                self.Flags = CMP
                if self.reg[self.ram_read(self.pc+1)] < self.reg[self.ram_read(self.pc+2)]:                  
                    L=1
                    G=0
                    E=0
                    self.Flags=CMP-0b00000100
                elif self.reg[self.ram_read(self.pc+1)] > self.reg[self.ram_read(self.pc+2)]:
                    G=1
                    L=0
                    E=0
                    self.Flags=CMP-0b00000010
                elif self.reg[self.ram_read(self.pc+1)] ==self.reg[self.ram_read(self.pc+2)]:
                    E=1
                    L=0
                    G=0
                    self.Flags=CMP-0b00000001
                self.pc+=3
                
            elif Command==JMP:
                self.pc = self.reg[self.ram_read(self.pc+1)]
            elif Command==JEQ:
                if E==1:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc+=2
            elif Command==JNE:
                if E ==0:
                    self.pc = self.reg[self.ram_read(self.pc+1)] 
                else:
                    self.pc+=2