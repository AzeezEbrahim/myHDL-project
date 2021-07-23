from myhdl import block, instances, instance, Signal, intbv, delay, always, ResetSignal

# ---------------------------------------------------------------------------- #
#!                                  Main Block                                  #
# ---------------------------------------------------------------------------- #


@block
def RegisterFile(REGwrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data):

    registers = [Signal(intbv(0,min=-2**31,max=2**31)) for i in range(32)]
    @always(rs1_In, rs2_In)
    def registersFetch():
        
        # First output value from register number [rs1_In]
        rs1_Out.next = registers[rs1_In]
        # Second output value from register number [rs2_In]
        rs2_Out.next = registers[rs2_In]
    @always(data,rd)
    def registersWrite():
        if REGwrite:
            registers[rd].next = data

    return instances()