from myhdl import block, always_comb, instance, Signal, intbv, delay, modbv, bin
from random import randrange

# ---------------------------------------------------------------------------- #
#                                      ALU                                     #
# ---------------------------------------------------------------------------- #

@block
def ALU(result, input_1, input_2, sel):

    @always_comb
    def ALU_Mux():
        if sel == 1:
            result.next = input_1 + input_2
        elif sel == 2:
            result.next = input_2 - input_1
        elif sel == 3:
            result.next = input_1 & input_2
        elif sel == 4:
            result.next = input_1 | input_2
        elif sel == 5:
            result.next = input_1 ^ input_2
        else:
            result.next = 0

    return ALU_Mux

# ---------------------------------------------------------------------------- #
#                                 ALU_TestBench                                #
# ---------------------------------------------------------------------------- #


@block
def test_ALU():
    result = Signal(intbv(0)[9:].signed())
    input_1 = Signal(intbv(0)[8:].signed())
    input_2 = Signal(intbv(0)[8:].signed())
    sel = Signal(intbv(0)[3:])
    ALU_1 = ALU(result, input_1, input_2, sel)

    @instance
    def test():
        yield delay(1)
        print("input_1  input_2  result")
        for i in range(1, 3):

            sel.next = i
            input_1.next = randrange(0, 2**3)
            input_2.next = randrange(0, 2**3)
            yield delay(1)
            print(bin(input_1, 8), bin(input_2, 8), bin(result, 9))

        for i in range(3, 6):

            sel.next = i
            input_1.next = randrange(0, 2**3)
            input_2.next = randrange(0, 2**3)
            yield delay(1)
            print(bin(input_1, 8), bin(input_2, 8), bin(result, 9))

    return test, ALU_1


tb = test_ALU()
tb.run_sim()


# ---------------------------------------------------------------------------- #
#                                ALU_conversion                                #
# ---------------------------------------------------------------------------- #

def convert(hdl):
    sel = Signal(intbv(0)[3:])
    input_1 = Signal(intbv(0)[8:].signed())
    input_2 = Signal(intbv(0)[8:].signed())
    result = Signal(intbv(0)[9:].signed())

    inst = ALU(result, input_1, input_2, sel)
    inst.convert(hdl=hdl)


convert(hdl='Verilog')
