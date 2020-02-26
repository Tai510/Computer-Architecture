"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
   #  Add list properties to the `CPU` class to hold 256 bytes of memory
    # and 8 general-purpose registers.
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256

    # In `CPU`, add method `ram_read()` and `ram_write()`
    # that access the RAM inside the `CPU` object.

  # `ram_read()` should accept the address to read and return the value stored there.
    def ram_read(self, memory_address_register):
        value = self.ram[memory_address_register]
        return value

# `ram_write()` should accept a value to write, and the address to write it to.   
    def ram_write(self, memory_data_register, memory_address_register):
        self.ram[memory_address_register] = memory_data_register

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            # Open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # Cast number strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

        

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        running = True

        while running:

            IR = self.ram[self.pc]
        # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables
        # `operand_a` and `operand_b` in case the instruction needs them.
        # operand_a = ram_read(IR + 1)
        # operand_b = ram_read(IR + 2)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

         # It needs to read the memory address that's stored in register `PC`,
         # and store that result in `IR`, the _Instruction Register_.
         # This can just be a local variable in `run()`.

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == HLT:
                running = False
        

cpu = CPU()
# cpu.load()
print(cpu.ram_read(0)) # test for ram_read works (print 130)
cpu.ram_write(0b10000001, 0) # puts binary 129 in register 0
print(cpu.ram_read(0)) # test for ram_write works (print 129)