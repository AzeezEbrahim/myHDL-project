from myhdl import * #block, always_comb, instance, Signal, intbv, delay

@block
def control(branch, memWrite, memRead, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, PCToALU, OPcode, func3, func7):

    @always(OPcode)
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
    
    @always(OPcode,func7,func3)
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

    @always(OPcode,func3)
    def DataMemControler():
        if OPcode == 0b0000011 or OPcode == 0b0100011:
            if func3 == 0x0 or func3 == 0x4:
                memRead.next = 0
            elif func3 == 0x1 or func3 == 0x5:
                memRead.next = 1
            elif func3 == 0x2:
                memRead.next = 2
            else :
                memRead.next = 0
        else: memRead.next = 0


            
    
    return controller ,ALUControl ,DataMemControler