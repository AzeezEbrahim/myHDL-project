from myhdl import block, instances, instance, Signal, intbv, delay, always, ResetSignal

# ---------------------------------------------------------------------------- #
#!                                  Main Block                                  #
# ---------------------------------------------------------------------------- #


@block
def RegisterFile(REGwrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data):

    registers = [Signal(intbv(0)[32:]) for i in range(32)]
    @always(rs1_In, rs2_In, rd)
    def registersFile():
        
        # First output value from register number [rs1_In]
        rs1_Out.next = registers[rs1_In]
        # Second output value from register number [rs2_In]
        rs2_Out.next = registers[rs2_In]

        if REGwrite:
            registers[rd].next = data

    return registersFile

# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #


# @block
# def TestBench():
    
#     rs1_In, rs2_In, rd = [Signal(intbv(0)[5:]) for i in range(3)]
#     rs1_Out, rs2_Out, data = [Signal(intbv(0)) for i in range(3)]
#     REGwrite = Signal(intbv(0)[2:])
#     reg1 = RegisterFile(REGwrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data )


#     @instance
#     def test():
#         yield delay(5)
#         for i in range(2):

#             REGwrite.next = i
#             rd.next = 0b100
#             data.next = 20
#             yield delay(10)
#             rs1_In.next = 0b110
#             rs2_In.next = 0b100
#             yield delay(10)

#             print(
#                 ' ------------------------------------------------------------------------------------------')
#             print("| %-10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-10s |" %('rs1_In', 'rs2_In', 'rd', 'data', 'REGwrite', 'rs1_Out', 'rs2_Out'))
#             print("| %-10d | %-10d | %-10d | %-10d | %-10d | %-10d | %-10d |" %(rs1_In, rs2_In, rd, data, REGwrite, rs1_Out, rs2_Out))
#             print(
#                 ' ------------------------------------------------------------------------------------------')

#             for i in range(16):
#                 rs1_In.next = i*2
#                 rs2_In.next = i*2+1
#                 yield delay(10)
#                 print('x%d , %d' % (rs1_In, rs1_Out))
#                 print('x%d , %d' % (rs2_In, rs2_Out))

#             print()

#     return  instances()


# test = TestBench()
# test.run_sim(2000)

# ---------------------------------------------------------------------------- #
#                              Verilog Conversion                              #
# ---------------------------------------------------------------------------- #


def convert(hdl):
    rs1_In, rs2_In, rd = [Signal(intbv(0)[5:]) for i in range(3)]
    rs1_Out, rs2_Out, data = [Signal(intbv(0, min=-2**31, max=2**31)) for i in range(3)]
    REGwrite = Signal(intbv(0)[2:])


    
    inst = RegisterFile(REGwrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data)
    inst.convert(hdl=hdl)


# convert(hdl='Verilog')
