from myhdl import * #block, always_comb, instance, Signal, intbv, delay

@block
def control(branch, memWrite, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, PCToALU, OPcode, func3, func7):

    @always_comb
    def controller():
        if OPcode == 0b0110011:  # for R-type
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 0
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 0
           
        elif OPcode == 0b0010011 : # for I-type without load
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 1
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 0

        elif OPcode == 0b0000011 : # for I-type with load
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 1
            immToALU.next = 1
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 0

        elif OPcode == 0b0100011 : # for S-type 
            branch.next = 0
            memWrite.next = 1
            memToReg.next = 0
            immToALU.next = 1
            regWrite.next = 0
            reg1ToPC.next = 0
            PCToALU.next = 0

        elif OPcode == 0b1100011 : # for B-type
            branch.next = 1
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 0
            regWrite.next = 0
            reg1ToPC.next = 0
            PCToALU.next = 0
       
        elif OPcode == 0b1101111 : # for J-type
            branch.next = 1
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 0
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 1

        elif OPcode == 0b1100111 : # for jalr
            branch.next = 1
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 0
            regWrite.next = 1
            reg1ToPC.next = 1
            PCToALU.next = 1
        
        elif OPcode == 0b0110111 : # for lui
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 1
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 0
 
        elif OPcode == 0b0010111 : # for auipc
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 1
            regWrite.next = 1
            reg1ToPC.next = 0
            PCToALU.next = 1
        else:
            branch.next = 0
            memWrite.next = 0
            memToReg.next = 0
            immToALU.next = 0
            regWrite.next = 0
            reg1ToPC.next = 0
            PCToALU.next = 0
    
    @always_comb
    def ALUControl():
        if OPcode == 0b0110011:  # for R-type
            if func7 == 0x00: 
                if func3 == 0x0: 
                    ALUOp.next = 1 # add
                elif func3 == 0x4: 
                    ALUOp.next = 3 # xor
                elif func3 == 0x6: 
                    ALUOp.next = 4 # or
                elif func3 == 0x7: 
                    ALUOp.next = 5 # and
                elif func3 == 0x1: 
                    ALUOp.next = 6 # shift left logical
                elif func3 == 0x5: 
                    ALUOp.next = 7 # shift right logical
                elif func3 == 0x2 or func3 == 0x3: 
                    ALUOp.next = 9 # set less than
                else: ALUOp.next = 0


            elif func7 == 0x20: 
                if func3 == 0x0: 
                    ALUOp.next = 2 # sub
                elif func3 == 0x5: 
                    ALUOp.next = 8 # shift right arith
                else: ALUOp.next = 0
            
            else: ALUOp.next = 0
        
        elif OPcode == 0b0010011 : # for I-type without load
            if func3 == 0x0: 
                ALUOp.next = 1 # add
            elif func3 == 0x4: 
                ALUOp.next = 3 # xor
            elif func3 == 0x6: 
                ALUOp.next = 4 # or
            elif func3 == 0x7: 
                ALUOp.next = 5 # and
            elif func3 == 0x1: 
                ALUOp.next = 6 # shift left logical
            elif func3 == 0x5: 
                ALUOp.next = 7 # shift right logical
            elif func3 == 0x2 or func3 == 0x3: 
                ALUOp.next = 9 # set less than
            else: ALUOp.next = 0

        
        elif OPcode == 0b0000011 or OPcode == 0b0100011:
            ALUOp.next = 1 # add

        elif OPcode == 0b1100011: # for B-type
            if func3 == 0x0: 
                ALUOp.next = 10 # rs1 == rs2
            elif func3 == 0x1: 
                ALUOp.next = 11 # rs1 != rs2
            elif func3 == 0x4 or func3 == 0x6: 
                ALUOp.next = 12 # rs1 < rs2
            elif func3 == 0x5 or func3 == 0x7: 
                ALUOp.next = 13 # rs1 >= rs2
            else: ALUOp.next = 0
        
        elif OPcode == 0b1101111 or OPcode == 0b1100111 : # for jar & jarl
            ALUOp.next = 14 # PC + 4 
        
        elif OPcode == 0b0110111 : # for lui
            ALUOp.next = 15 # imm << 12
        
        elif OPcode == 0b0010111 : # for auipc
            ALUOp.next = 16 # PC + (imm << 12)
        else: ALUOp.next = 0
            
    
    return controller ,ALUControl

branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU = [Signal(bool(0)) for i in range(7)]
ALUOp = Signal(intbv(0)[5:])
func3 = Signal(intbv(0)[3:])
func7 = Signal(intbv(0)[7:])
OPcode = Signal(intbv(0)[7:])



 

@block
def test_control():
    inst = Signal(intbv(0)[32:])
    OPcode = inst(7,0)
    func3 = inst(15,12)
    func7 = inst(32,25)
    tstControl = control(branch, memWrite, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, PCToALU, OPcode, func3, func7)
    @instance
    def simulate():
        print("Instruction       | branch | memWrite | memToReg | immToALU | regWrite | reg1ToPC | PCToALU | ALUOp")
        print("_______________________________________________________________________________________________")
        
        inst.next = 0b00000000001100010000000010110011
        yield delay(10)
        print("add x1, x2, x3    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00101000011000101000001000110011
        yield delay(10)
        print("sub x4, x5, x6    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))
        
        inst.next = 0b00000000100101000100001110110011
        yield delay(10)
        print("xor x7, x8, x9    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000110001011110010100110011
        yield delay(10)
        print("or x10, x11, x12  |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000111101110111011010110011
        yield delay(10)
        print("and x13, x14, x15 |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000001000011001000100010011
        yield delay(10)
        print("slli x2, x3, 2    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000101000101101001000010011
        yield delay(10)
        print("srli x4, x5, 10   |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00010100011100111101001100010011
        yield delay(10)
        print("srai x6, x7, 7    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000001101001010010000010011
        yield delay(10)
        print("slti x8, x9, 3    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000010001011011010100010011
        yield delay(10)
        print("sltiu x10, x11, 4 |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000100101101000011000000011
        yield delay(10)
        print("lb x12, x13, 9    |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000011011110110010000110100011
        yield delay(10)
        print("sw 35, x22, x23   |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000001100111000000011001100011
        yield delay(10)
        print("beq 24, x24, x25  |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000001101111010001001001100011
        yield delay(10)
        print("bne 8, x26, x27   |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000001110111100100100101100011
        yield delay(10)
        print("blt 36, x28, x29  |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000001111111110101101001100011
        yield delay(10)
        print("bge 40, x30, x31  |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000000000000000001011101111
        yield delay(10)
        print("jal 80, x5        |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000010100000111000001101100111
        yield delay(10)
        print("jalr x6, x7, 40   |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000000000000000010000110111
        yield delay(10)
        print("lui x8, 9         |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

        inst.next = 0b00000000000000000010010010010111
        yield delay(10)
        print("auipc x9, 17      |    %d   |     %d    |    %d     |   %d    |    %d     |     %d    |    %d    | %s  " 
        % (branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, PCToALU, bin(ALUOp,5)))

    return instances()

def convert():
    con = control(branch, memWrite, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, PCToALU, OPcode, func3, func7)
    con.convert(hdl='Verilog')

# convert()
test = test_control()
test.run_sim(200)

