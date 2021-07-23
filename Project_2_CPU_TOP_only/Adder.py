from myhdl import always,block,Signal,intbv,instance,delay,instances, bin

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #
@block
def adder(PC,nextInstruction):

    @always(PC)
    def add():
        increament=intbv(4)[32:]
        nextInstruction.next = PC + increament 

    return add