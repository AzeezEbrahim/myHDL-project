from myhdl import always, block, always_seq, Signal, modbv, ResetSignal, \
    delay, instance, intbv, instances
import random
randomrange = random.randrange

# ---------------------------------------------------------------------------- #
#                                   register                                   #
# ---------------------------------------------------------------------------- #
@block
def ParallelReg(out, inp, clock, enable, reset):
    @always_seq(clock.posedge, reset=reset)
    def passIt():
        if(enable):
            out.next = inp
    return passIt

# ---------------------------------------------------------------------------- #
#                                   Test-becnh                                  #
# ---------------------------------------------------------------------------- #


@block
def RegTestBench():
    randomrange = random.randrange
    out = Signal(intbv(0)[32:])
    inp = Signal(intbv(0)[32:])
    clock = Signal(bool(0))
    enable = Signal(bool(0))
    reset = ResetSignal(0, active=0, isasync=False)
    RegObject = ParallelReg(out, inp, clock, enable, reset)

    @always(delay(10))
    def clkUp():
        clock.next = not clock

    @instance
    def stimulus():
        # ---reset----
        reset.next = 1
        # ---enable---
        for i in range(10):
            enable.next = randomrange(2)
            # at the negEdge come to this line at continoue exe down (loop)
            yield clock.negedge
        # ---end---

    @instance
    def monitor():
        # ---header out---
        print("enable         inp                        out                  rest")
        while True:
            inp.next = randomrange((2**32)-1)
            yield clock.posedge  # at the PosEdge come to this line ate continoue exe down
            yield delay(1)  # after delay by '1' go through print
            print("%s           %s                   %s               %s"
                  % (int(enable), hex(inp), hex(out), int(reset)))
    return monitor, stimulus, clkUp, RegObject

# -------------------end test bench--------------------------------------------


def runtestBench():
    testbench = RegTestBench()
    testbench.run_sim(3000)


runtestBench()

# ---------------------------------------------------------------------------- #
#                                  conversion                                  #
# ---------------------------------------------------------------------------- #


def conversion():
    # --------------initilaization ---------------
    out = Signal(intbv(0)[32:])
    inp = Signal(intbv(0)[32:])
    clock = Signal(bool(0))
    enable = Signal(bool(0))
    reset = ResetSignal(0, active=0, isasync=False)

    RegObject = ParallelReg(out, inp, clock, enable, reset)
    RegObject.convert(hdl="verilog")


# conversion()

