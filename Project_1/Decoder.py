
from myhdl import block, always_comb, Signal, intbv, instance, delay, instances, bin

# ---------------------------------------------------------------------------- #
#                                    Decoder                                   #
# ---------------------------------------------------------------------------- #


@block
def Decoder(out, inp):

    @always_comb
    def decoder():
        out.next = 0
        out.next[inp] = 1

    return decoder


# ---------------------------------------------------------------------------- #
#                                  test bench                                  #
# ---------------------------------------------------------------------------- #


@block
def DecoderTestBench():
    # --------------initilaization ---------------
    out = Signal(intbv(0)[16:])
    inp = Signal(intbv(0)[4:])

    # --------------create an object -------------
    decoderObject = Decoder(out, inp)

    @instance
    def stimulus():

        for i in range(16):
            inp.next = i
            yield delay(10)
            print("   %s     %s " % (bin(inp, 4), bin(out, 16)))
    return instances()
# -------------------end-----------------------


def runtestBench():
    a = DecoderTestBench()
    a.run_sim(1000)


runtestBench()

# ---------------------------------------------------------------------------- #
#                                  conversion                                  #
# ---------------------------------------------------------------------------- #


def conversion():
    # --------------initilaization ---------------
    out = Signal(intbv(0)[16:])
    inp = Signal(intbv(0)[4:])
    decoderObject = Decoder(out, inp)  # ---create object------
    decoderObject.convert(hdl="verilog")  # ---------convert------


#conversion()
