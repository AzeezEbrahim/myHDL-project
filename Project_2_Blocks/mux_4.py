from myhdl import block, always, Signal, instance, intbv, delay
from random import randrange

# ---------------------------------------------------------------------------- #
#                                  Main Block                                  #
# ---------------------------------------------------------------------------- #
@block
def mux4(Output, a, b, selector):

    @always(a, b, selector)
    def comb():
        if selector == 0:
            Output.next = a
        else:
            Output.next = b

    return comb

# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #
# @block
# def test_mux_2_1():

#     Output, a, b = [Signal(intbv(0)[32:]) for i in range(3)]
#     selector = Signal(intbv(0)[1:])
#     mux_1 = mux4(Output, a, b, selector)

#     @instance
#     def stimulus():
#         print()
#         print("selector   a b   Output")
#         print("_______________________")
#         for i in range(12):
#             a.next, b.next, selector.next = randrange(
#                 8), randrange(8), randrange(2)
#             yield delay(10)
#             print("  %s     |  %s %s  |   %s" % (int(selector), int(a), int(b), int(Output)))

#     return mux_1, stimulus

# test = test_mux_2_1()
# test.run_sim(100)
# # ---------------------------------------------------------------------------- #
# #                                 Mux_2X1_conversion                           #
# # ---------------------------------------------------------------------------- #

# def convert(hdl):
#     Output = Signal(intbv(0)[32:])
#     a = Signal(intbv(0)[32:])
#     b = Signal(intbv(0)[32:])
#     selector = Signal(intbv(0)[2:])

#     inst = mux4(Output, a, b, selector)
#     inst.convert(hdl=hdl)

# convert(hdl='Verilog')