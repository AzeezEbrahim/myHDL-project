from myhdl import block, always_comb, Signal, instance, intbv, delay
from random import randrange

# ---------------------------------------------------------------------------- #
#                                    Mux_2X1                                   #
# ---------------------------------------------------------------------------- #


@block
def mux2_1(Output, a, b, selector):

    @always_comb
    def comb():
        if selector == 0:
            Output.next = a
        elif selector == 1:
            Output.next = b
        else:
            Output.next = 0

    return comb

# ---------------------------------------------------------------------------- #
#                                    Mux_3X1                                    #
# ---------------------------------------------------------------------------- #


@block
def mux3_1(Output, a, b, c, selector):

    @always_comb
    def comb():
        if selector == 0:
            Output.next = a
        elif selector == 1:
            Output.next = b
        elif selector == 2:
            Output.next = c
        else:
            Output.next = 0

    return comb


# ---------------------------------------------------------------------------- #
#                                 Mux_2X1_TestBench                            #
# ---------------------------------------------------------------------------- #


@block
def test_mux_2_1():

    Output, a, b, selector = [Signal(intbv(0)) for i in range(4)]

    mux_1 = mux2_1(Output, a, b, selector)

    @instance
    def stimulus():
        print()
        print("selector   a b   Output")
        print("_______________________")
        for i in range(12):
            a.next, b.next, selector.next = randrange(
                8), randrange(8), randrange(2)
            yield delay(10)
            print("  %s     |  %s %s  |   %s" % (selector, a, b, Output))

    return mux_1, stimulus


# ---------------------------------------------------------------------------- #
#                                 Mux_3X1_TestBench                            #
# ---------------------------------------------------------------------------- #


@block
def test_mux_3_1():

    Output, a, b, c, selector = [Signal(intbv(0)) for i in range(5)]

    mux_1 = mux3_1(Output, a, b, c, selector)

    @instance
    def stimulus():
        print()
        print("selector     a b c     Output")
        print("______________________________")
        for i in range(12):
            a.next, b.next, c.next, selector.next = randrange(
                8), randrange(8), randrange(8), randrange(3)
            yield delay(10)
            print("   %s     |   %s %s %s   |   %s" %
                  (selector, a, b, c, Output))

    return mux_1, stimulus


tb = test_mux_2_1()
rb = test_mux_3_1()

tb.run_sim()
rb.run_sim()


# ---------------------------------------------------------------------------- #
#                                 Mux_2X1_conversion                           #
# ---------------------------------------------------------------------------- #

def convert(hdl):
    Output = Signal(intbv(0)[4:])
    a = Signal(intbv(0)[4:])
    b = Signal(intbv(0)[4:])
    selector = Signal(intbv(0)[2:])

    inst = mux2_1(Output, a, b, selector)
    inst.convert(hdl=hdl)


# convert(hdl='Verilog')
# ---------------------------------------------------------------------------- #
#                                 Mux_3X1_conversion                           #
# ---------------------------------------------------------------------------- #


def convert(hdl):
    Output = Signal(intbv(0)[4:])
    a = Signal(intbv(0)[4:])
    b = Signal(intbv(0)[4:])
    c = Signal(intbv(0)[4:])
    selector = Signal(intbv(0)[2:])

    inst = mux3_1(Output, a, b, c, selector)
    inst.convert(hdl=hdl)


# convert(hdl='Verilog')
