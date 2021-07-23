from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  Main Block                                  #
# ---------------------------------------------------------------------------- #

@block
def ALU(input_1,input_2,ALU_Control,ALU_result,Zero_Flag):
    @always(input_1,input_2,ALU_Control)
    def Operand():
        
        if ALU_Control == 1:                 #! ADD operation
            ALU_result.next = input_1 + input_2
            Zero_Flag.next = 0
            
        elif ALU_Control == 2:               #! SUB operation
            ALU_result.next = input_1 - input_2
            Zero_Flag.next = 0
        
        elif ALU_Control == 3:               #! XOR operation 
            ALU_result.next = input_1 ^ input_2
            Zero_Flag.next = 0
                
        elif ALU_Control == 4:               #! OR operation
            ALU_result.next = input_1 | input_2
            Zero_Flag.next = 0
            
        elif ALU_Control == 5:               #! AND operation
            ALU_result.next = input_1 & input_2
            Zero_Flag.next = 0

        elif ALU_Control == 6:               #! SLL operation
            ALU_result.next = input_1 << input_2
            Zero_Flag.next = 0
            
        elif ALU_Control == 7:               #! SRL operation
            ALU_result.next = input_1 >> input_2
            Zero_Flag.next = 0

        elif ALU_Control == 8:               #! SRA operation
            ALU_result.next = modbv((input_1 >> input_2) | (input_1 >> (len(input_1) - input_2))).signed()
            Zero_Flag.next = 0 

        elif ALU_Control == 9:               #! SLT & SLTU operation
            if(input_1 < input_2):
                ALU_result.next = 1
                Zero_Flag.next = 0
            else:
                ALU_result.next = 0
                Zero_Flag.next = 0

        elif ALU_Control == 10:              #! BEQ operation
            if input_1 == input_2:
                Zero_Flag.next = 1
                ALU_result.next = 0
            else:
                Zero_Flag.next = 0
                ALU_result.next = 0

        elif ALU_Control == 11:             #! BNE operation 
            if input_1 != input_2:
                Zero_Flag.next = 1
                ALU_result.next = 0
            else:
                Zero_Flag.next = 0
                ALU_result.next = 0

        elif ALU_Control == 12:              #! BLT & BLTU operation 
            if input_1 < input_2:
                Zero_Flag.next = 1
                ALU_result.next = 0
            else:
                Zero_Flag.next = 0
                ALU_result.next = 0

        elif ALU_Control == 13:              #! BGE & BGEU operation
            if input_1 >= input_2:
                Zero_Flag.next = 1
                ALU_result.next = 0
            else:
                Zero_Flag.next = 0
                ALU_result.next = 0

        elif ALU_Control == 14:              #! jal & jalr operation 
            ALU_result.next = input_1 + 4
            Zero_Flag.next = 1

        elif ALU_Control == 15:              #! LUI operation 
            ALU_result.next = input_2 << 12
            Zero_Flag.next = 0

        elif ALU_Control == 16:              #! AUIPC operation 
            ALU_result.next = input_1 + (input_2 << 12)
            Zero_Flag.next = 0
            

        else:
            Zero_Flag.next = 0               #!  ELSE  
            ALU_result.next = 0


    return Operand