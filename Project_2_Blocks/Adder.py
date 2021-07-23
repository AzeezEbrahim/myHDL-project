from myhdl import always_comb,block,Signal,intbv,instance,delay,instances, bin

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #
@block
def adder(PC,nextInstruction):

    @always_comb
    def add():
        increament=intbv(4)[32:]
        nextInstruction.next = PC + increament 

    return add
# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #
@block
def test():

    pc, nextInstruction = [Signal(intbv(0)[32:]) for i in range(2)]

    ProgCounter = adder(pc,nextInstruction)

    @instance
    def test():
        
        print(hex(nextInstruction))
        for i in range(0,40,4):
            pc.next = i

            yield delay(5)
            print(hex(nextInstruction))


    return instances()

tb = test()
tb.run_sim(100)

# ---------------------------------------------------------------------------- #
#                              Verilog Conversion                              #
# ---------------------------------------------------------------------------- #

def convert(hdl):
    pc, nextInstruction = [Signal(intbv(0)[32:]) for i in range(2)]

    inst = adder(pc, nextInstruction)
    inst.convert(hdl=hdl)


# convert(hdl='Verilog')