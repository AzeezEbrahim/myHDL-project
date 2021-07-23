
from myhdl import always, block, always_seq, Signal, modbv, ResetSignal, \
    delay, instance, intbv, instances
import random
randomrange = random.randrange

# ---------------------------------------------------------------------------- #
#                                  main block                                  #
# ---------------------------------------------------------------------------- #

@block
def pc(PCOutput,PCInput,clock):
    @always(clock.posedge)
    def passIt():
        PCOutput.next = PCInput
    return passIt

# ---------------------------------------------------------------------------- #
#                                   TestBench                                  #
# ---------------------------------------------------------------------------- #

# @block
# def RegTestBench():
#     randomrange = random.randrange
#     PCOutput = Signal(intbv(0)[32:])
#     PCInput  = Signal(intbv(0)[32:])
#     clock  = Signal(bool(0))
#     RegObject = pc(PCOutput, PCInput, clock)

#     @always(delay(10))
#     def clkUp():
#         clock.next = not clock
#     @instance
#     def monitor():
#         #---header PCOutput---
#         print(" PCInput                   PCOutput         ")
#         while True:
#             PCInput.next = randomrange(2**32)
#             yield clock.posedge     #at the PosEdge come to this line ate continoue exe down
#             yield delay(10)           #after delay by '1' go through print
#             print(" %s               %s" %(hex(PCInput),hex(PCOutput)))
#     return monitor,clkUp,RegObject


# def runtestBench():
#     testbench = RegTestBench()
#     testbench.run_sim(1000)
# runtestBench()

# ---------------------------------------------------------------------------- #
#                             conversion to verilog                            #
# ---------------------------------------------------------------------------- #

def conversion():
    PCOutput     = Signal(intbv(0)[32:])
    PCInput  = Signal(intbv(0)[32:])
    clock        = Signal(bool(0))

    RegObject    = pc(PCOutput,PCInput,clock)
    RegObject.convert(hdl = "verilog")

# conversion()