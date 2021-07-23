from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  main block                                  #
# ---------------------------------------------------------------------------- #

@block
def instMem(inst, address, data_in, write_enable):
    memory = [Signal(intbv(0)[8:]) for i in range(32*4)]
    @always(address, data_in)
    def fetch():
        if write_enable:
            memory[address+3].next = data_in[32:24]
            inst.next[32:24] = 0
            memory[address+2].next = data_in[24:16]
            inst.next[24:16] = 0
            memory[address+1].next = data_in[16:8]
            inst.next[16:8] = 0
            memory[address].next = data_in[8:0]
            inst.next[8:0] = 0
        else:
            inst.next[32:24] = memory[address+3]
            inst.next[24:16] = memory[address+2]
            inst.next[16:8] = memory[address+1]
            inst.next[8:0] = memory[address]
    return instances()


inst = Signal(intbv(0)[32:])
address = Signal(intbv(0)[32:])
data_in = Signal(intbv(0)[32:])
write_enable = Signal(intbv(0)[1:])
# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #
# @block
# def test_instMem():
    
#     tstInstMem = instMem(inst, address, data_in, write_enable)
    
#     @instance
#     def test():
#         write_enable.next = 1
#         i = 0
#         with open('InstructionCode.txt', 'r') as f:
#             for line in f:
#                 data_in.next = Signal(intbv(line))
#                 address.next = i*4
#                 i += 1
#                 yield delay(1)
#         address.next = 0
#         write_enable.next = 0
#         yield delay(1)
#         print("Reg  | Address |           Instruction")
#         print("---------------------------------------------------")
#         for i in range (32):
#             address.next = i*4
#             yield delay(1)

#             print("x%02d  |   %03d   |  %s" % (i,address,bin(inst, 32)))
    
#     return instances()

# test = test_instMem()
# test.run_sim(5000)

# ---------------------------------------------------------------------------- #
#                              Verilog conversion                              #
# ---------------------------------------------------------------------------- #

def convert():
    con = instMem(inst, address, data_in, write_enable)
    con.convert(hdl='Verilog')

# convert()