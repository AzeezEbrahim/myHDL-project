from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #

@block
def BranchAdder(int_1,int_2,out):

    @always(int_1,int_2)
    def adder():

        out.next = int_1 + (int_2 << 1)

    return adder