from myhdl import block, always, Signal, instance, intbv, delay

# ---------------------------------------------------------------------------- #
#                                  Main Block                                  #
# ---------------------------------------------------------------------------- #
@block
def mux2_1(Output, a, b, selector):

    @always(a, b, selector)
    def comb():
        if selector == 0:
            Output.next = a
        else:
            Output.next = b

    return comb

# @block
# def mux_1(Output, a, b, selector):

#     @always(a, b, selector)
#     def comb():
#         if selector == 0:
#             Output.next = a
#         else:
#             Output.next = b

#     return comb

# @block
# def mux_2(Output, a, b, selector):

#     @always(a, b, selector)
#     def comb():
#         if selector == 0:
#             Output.next = a
#         else:
#             Output.next = b

#     return comb

# @block
# def mux_3(Output, a, b, selector):

#     @always(a, b, selector)
#     def comb():
#         if selector == 0:
#             Output.next = a
#         else:
#             Output.next = b

#     return comb

# @block
# def mux_4(Output, a, b, selector):

#     @always(a, b, selector)
#     def comb():
#         if selector == 0:
#             Output.next = a
#         else:
#             Output.next = b

#     return comb

# @block
# def mux_5(Output, a, b, selector):

#     @always(a, b, selector)
#     def comb():
#         if selector == 0:
#             Output.next = a
#         else:
#             Output.next = b

#     return comb