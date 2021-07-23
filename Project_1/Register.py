from myhdl import block, always, intbv, Signal, instances, instance, delay, bin, now, concat, ConcatSignal, posedge, always_comb, modbv
from myhdl._block import _Block as Module
from random import randrange


# ---------------------------------------------------------------------------- #
#                                32-bit register                               #
# ---------------------------------------------------------------------------- #
@block
def Register_32Bit(inputs, clk, enable, outputs):

    @always(clk.posedge)
    def register():
       # if reset == 0:
            if enable:
                outputs.next = inputs
            else:
                outputs.next = outputs

    return instances()  # Or -->> register

# ---------------------------------------------------------------------------- #
#                                TestBench of 32-bit register                  #
# ---------------------------------------------------------------------------- #


@block
def TestBenchregister():
    inputs = Signal(intbv(0)[32:0])
    enable = Signal(bool(0))
    clk = Signal(bool(0))
    #reset = Signal(bool(0))
    outputs = Signal(intbv(0)[32:0])

    Register_32 = Register_32Bit(inputs, clk, enable, outputs)

    @always(delay(5))
    def clk_driver():
        clk.next = not clk

    @instance
    def TestBench():
        while True:
            print("input = %d   CurrentTime = %s" % (inputs, now()))
            enable.next = 1
            # reset.next = 0
            clk.next = not clk
            inputs.next = randrange(2)
            print("output = %s" % bin(outputs))
            print()
            yield (clk.negedge)

    return instances()  # Or -->> clk_driver, TestBench,  Register_32


tb = TestBenchregister()
tb.run_sim(30)


# if __name__ == '__main__':
#     inputs = Signal(intbv(0)[32:0])
#     enable = Signal(bool(0))
#     clk = Signal(bool(0))
#     reset = Signal(bool(0))
#     outputs = Signal(intbv(0)[32:0])

#     inst=Register_32Bit(inputs,clk,enable,reset,outputs)
#     inst.run_sim(100)
#     inst.convert('Verilog')
