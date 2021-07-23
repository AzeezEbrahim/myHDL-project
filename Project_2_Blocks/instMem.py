from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  main block                                  #
# ---------------------------------------------------------------------------- #

@block
def instMem(inst, address):
    memory = [intbv(0)[8:] for i in range(32*4)]
    # index = 0
    # with open('InstructionCode.txt', 'r') as f:
    #     for line in f:
    #         data_in = intbv(line)
    #         memory[index+3].next = data_in[32:24]
    #         memory[index+3]._update() 
    #         memory[index+2].next = data_in[24:16]
    #         memory[index+2]._update()
    #         memory[index+1].next = data_in[16:8]
    #         memory[index+1]._update()
    #         memory[index].next = data_in[8:0]
    #         memory[index]._update()
    #         index += 4 
    @always(address)
    def fetch():
           inst.next[32:24] = Signal(memory[address+3])
           inst.next[24:16] = Signal(memory[address+3])
           inst.next[16:8] = Signal(memory[address+3])
           inst.next[8:0] = Signal(memory[address+3])
    return instances()


inst = Signal(intbv(0)[32:])
address = Signal(intbv(0)[32:])
# memory = [Signal(intbv(0)[8:]) for i in range(32*4)]
# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #
# @block
# def test_instMem():
    
#     tstInstMem = instMem(inst, address)
    
#     @instance
#     def test():
#         print("Reg  | Address |           Instruction")
#         print("---------------------------------------------------")
#         for i in range (32):
#             address.next = i*4
#             yield delay(20)

#             print("x%02d  |   %03d   |  %s" % (i,address,bin(inst, 32)))
    
#     return instances()

# test = test_instMem()
# test.run_sim(5000)

# ---------------------------------------------------------------------------- #
#                              Verilog conversion                              #
# ---------------------------------------------------------------------------- #

def convert():
    con = instMem(inst, address)
    con.convert(hdl='Verilog')

# convert()
