from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  main block                                  #
# ---------------------------------------------------------------------------- #

@block
def instMem(inst, address, data_in, write_enable):
    memory = [Signal(intbv(0)[8:]) for i in range(83*4)]
    AssemblyCode = []
    with open('D:\ProgramsFile\VS code\EE361\Project_2_CPU_only\Sort_AssemblyCode.txt', 'r') as f:
            for line in f:
                AssemblyCode.append(line)
    @always(address)
    def fetch():
        if write_enable:
            memory[address+3].next = data_in[32:24]
            memory[address+2].next = data_in[24:16]
            memory[address+1].next = data_in[16:8]
            memory[address].next = data_in[8:0]
            inst.next = 0
        else:
            inst.next[32:24] = memory[address+3]
            inst.next[24:16] = memory[address+2]
            inst.next[16:8] = memory[address+1]
            inst.next[8:0] = memory[address]
            print("Instruction", bin(inst.next,32))
            print("address: ", int(address))
            print("Assembly", AssemblyCode[address//4][:-1])
    return instances()