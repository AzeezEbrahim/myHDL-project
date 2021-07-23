from myhdl import *

# ---------------------------------------------------------------------------- #
#                                  Main Block                                  #
# ---------------------------------------------------------------------------- #

@block
def ALU(input_1,input_2,ALU_Control,ALU_result,Zero_Flag):
    @always_comb
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
            ALU_result.next = modbv((input_1 >> input_2) | (input_1 << (len(input_1) - input_2))).signed()
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



# ---------------------------------------------------------------------------- #
#                                  Test-Bench                                  #
# ---------------------------------------------------------------------------- #



@block
def test_ALU():
    
    input_1, input_2, ALU_result = [Signal(intbv(0)[32:].signed()) for i in range(3)]
    ALU_Control = Signal(intbv(0)[5:])
    Zero_Flag = Signal(intbv(0)[1:])

    ALU_1 = ALU(input_1,input_2,ALU_Control,ALU_result,Zero_Flag)

    @instance
    def test():
        Operation = ["ADD ", "SUB ", "XOR ", "OR ", "AND ", "SLL ", "SRL ", "SRA ", "SLT ",
                     "BEQ ", "BNE ", "BLT ", "BGE ", "jal & jalr ","LUI ","AUIPC ",
                     "ELSE"]

        for i in range(1, 18):
            input_1.next, input_2.next, ALU_Control.next =  9, 11, i  # Testing ALU_Control
             
            yield delay(1)
            print('-------------------------------------------------------------------------------------------------------------')
            print("| %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('input_1','input_2','ALU_Control','ALU_result','Zero_Flag', 'Operation'))
            print("| %-15d | %-15d | %-15d | %-15d | %-15d | %-15s |"%(input_1, input_2, ALU_Control, ALU_result, Zero_Flag, Operation[i-1]))
            print('-------------------------------------------------------------------------------------------------------------')

    return test, ALU_1


tb = test_ALU()
tb.run_sim()

# ---------------------------------------------------------------------------- #
#                              Verilog conversion                              #
# ---------------------------------------------------------------------------- #

def convert(hdl):
    
    input_1, input_2, ALU_result = [Signal(intbv(0)[32:].signed()) for i in range(3)]
    ALU_Control = Signal(intbv(0)[5:])
    Zero_Flag = Signal(intbv(0)[2:])
    inst = ALU(input_1,input_2,ALU_Control,ALU_result,Zero_Flag)
    inst.convert(hdl=hdl)



# convert(hdl='Verilog')