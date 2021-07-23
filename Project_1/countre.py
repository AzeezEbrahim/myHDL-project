from myhdl import block, always, modbv, Signal, delay, \
    always_seq, ResetSignal, instance, bin
from random import randrange

# ---------------------------------------------------------------------------- #
#                                    counter                                   #
# ---------------------------------------------------------------------------- #


@block
def countre(count, enable, clock, reset):

    @always_seq(clock.posedge, reset=reset)
    def seq():
        if enable:
            count.next = count + 1
    return seq


count = Signal(modbv(0)[12:])
enable, clk = [Signal(bool(0)) for i in range(2)]
reset = ResetSignal(0, active=1, isasync=False)

# ---------------------------------------------------------------------------- #
#                                   TestBench                                  #
# ---------------------------------------------------------------------------- #


@block
def testbench():
    counter_test = countre(count, enable, clk, reset)

    @always(delay(5))
    def clock():
        clk.next = not clk
        if clk:
            print(" %s  |    %s  | %s" %
                  (bin(enable), bin(count, 12), bin(reset)))

    @instance
    def reset_gen():
        while True:
            yield delay(randrange(100, 1200))
            reset.next = 1
            yield delay(randrange(20))
            reset.next = 0

    @instance
    def enable_gen():
        while True:
            enable.next = 1
            yield delay(randrange(80, 150))
            enable.next = 0
            yield delay(randrange(30))

    return clock, counter_test, reset_gen, enable_gen


def simulate():
    print("enable  |  count  |  reset")
    print("__________________________")
    tb = testbench()
    tb.run_sim(1000)

# ---------------------------------------------------------------------------- #
#                                  conversion                                  #
# ---------------------------------------------------------------------------- #


def convert():
    tst = countre(count, enable, clk, reset)
    tst.convert(hdl='Verilog')


simulate()
# convert()
