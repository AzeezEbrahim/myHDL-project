from myhdl import *
import random
randomrange = random.randrange

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #

@block
def BranchAdder(int_1,int_2,out):

    @always_comb
    def adder():

        out.next = int_1 + (int_2 << 1)

    return adder

# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #
@block
def test():

    int_1, int_2, out = [Signal(intbv(0)[32:]) for i in range(3)]
    Branch_Adder = BranchAdder(int_1,int_2,out)

    @instance
    def test():
        print()
        print("intput_1 + (input_2 shifted to left) =  result")
        for i in range(5):
            int_1.next = 1
            int_2.next = randomrange(10)
            yield delay(5)
            print("     %-3d +     %-21d =  %-10s" % (int(int_1), int(int_2), bin(out, 32)))


    return instances()

tb = test()
tb.run_sim(100)

# ----------------------------------------------------------------------- #
#                        conversion                                       #
# ----------------------------------------------------------------------- #

def conversion():
    int_1, int_2, out = [Signal(intbv(0)[32:]) for i in range(3)]
    dataMemoryObject = BranchAdder(int_1,int_2,out)
    dataMemoryObject.convert(hdl ="verilog")
    
# conversion()

