from myhdl import always, block, instance,  bin,\
     Signal, delay, intbv, modbv, always_comb
from random import randrange

# ---------------------------------------------------------------------------- #
#                                BARREL SHIFTER                                #
# ---------------------------------------------------------------------------- #
@block
def barrel_shifter(load_reg, load_in, shift):
    X = Signal(modbv(0)[12:])
    @always_comb
    def shift_3bit():
        load_reg.next = load_in >> shift

    return shift_3bit

load_reg = Signal(modbv(0)[12:])
load_in = Signal(modbv(0)[12:])
shift = Signal(intbv(0)[3:])

# ---------------------------------------------------------------------------- #
#                                  Test-bench                                  #
# ---------------------------------------------------------------------------- #

@block
def test():

    test_barrel_shifter = barrel_shifter(load_reg, load_in, shift)
    
    @always(delay(10))
    def shift_gen():
        shift.next = randrange(8)
        load_in.next = randrange(2**12)

    @always(delay(10))
    def stimulus():
        print("%s   |  %s  |  %s "%(bin(load_in,12), bin(shift,3), bin(load_reg,12)))

    return test_barrel_shifter, shift_gen, stimulus

def simulate():
    tb = test()
    print("     load_in      | shift | load_reg")
    print("______________________________")
    tb.run_sim(500)

# ---------------------------------------------------------------------------- #
#                                  conversion                                  #
# ---------------------------------------------------------------------------- #

def convert():
    conv = barrel_shifter(load_reg, load_in, shift)
    conv.convert(hdl='Verilog')

simulate()
# convert()
