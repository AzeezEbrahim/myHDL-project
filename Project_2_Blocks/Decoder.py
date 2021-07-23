from myhdl import *
#------------------------------------------------------------------------------------------------#
#                                         Main Block                                             #
#------------------------------------------------------------------------------------------------#

@block
def decoder32(instruction ,opcode ,rs1, rs2, rd , imm, funct3, funct7):

    @always(instruction)
    def decode32():
        opcode.next = instruction[7:]
        rs1.next=instruction[20:15]
        rs2.next=instruction[25:20]
        rd.next=instruction[12:7]
        funct3.next =instruction[15:12]
        funct7.next = instruction[32:25]
        
    @always_comb
    def immediate():
        opcode_in = instruction[7:]

        if opcode_in == 0b0110011:
            imm.next = 0
           # R Type instructions
        elif opcode_in == 0b0101111:
            imm.next = 0
         #   R Type - Atomic Extension - instructions

        elif opcode_in == 0b0000011:
            imm.next = intbv(instruction[32:20].signed(),min=-2**31, max=2**31)
        elif opcode_in == 0b0010011:
            function3 = instruction[15:12]
            imm.next = intbv(instruction[32:20].signed(),min=-2**31, max=2**31)
            if function3==0b001 or function3==0b101: 
                imm.next=intbv(instruction[25:20].signed(),min=-2**31, max=2**31)
            else:                           
                imm.next=intbv(instruction[32:20].signed(),min=-2**31, max=2**31)
           # I type - ALU - instructions



        elif opcode_in == 0b0100011:
            imm.next = intbv(concat(instruction[32:25],instruction[12:7]).signed(),min=-2**31, max=2**31)
           # S Type instructions


        elif opcode_in == 0b1100011:
            imm.next=intbv(concat(instruction[32:31],instruction[8:7],instruction[31:25],instruction[12:8]).signed(),min=-2**31, max=2**31)
           #SB type instructions
        elif opcode_in == 0b0010111 or opcode_in== 0b0110111:
            imm.next=intbv(instruction[32:12].signed(),min=-2**31, max=2**31)
        elif opcode_in == 0b1101111 or opcode_in == 0b1100111:
            imm.next = intbv(concat( instruction[31], instruction[20:12], instruction[20], instruction[31:21]).signed(),min=-2**31, max=2**31)
          #  UJ type instructions
        else:
            imm.next=0
           # print('bubble')

    return instances()

#------------------------------------------------------------------------------------------------#
#                                         Test Bench                                             #
#------------------------------------------------------------------------------------------------#

instruction=Signal(intbv(0,min=-2**32,max=2**32))
rs1,rs2,rd=[Signal(intbv(0)[5:])for i in range(3)]
imm=Signal(intbv(0,min=-2**32,max=(2**32)))
funct3 = Signal(intbv(0)[3:])
funct7 = Signal(intbv(0)[7:])
opcode = Signal(intbv(0)[7:])


@block
def test_decoder():
     
    
    Decoder_test = decoder32(instruction,opcode,rs1,rs2,rd,imm,funct3,funct7)

    @instance
    def test3():
        yield delay(5)
        # trial
        
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type: ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' trial ', bin(instruction,32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    
        

       # R type
        instruction.next = 0b00000001000001111000010100110011
        yield delay(10)
        
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type:  ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' R  ', bin(instruction,32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       
       
       
       # I type
        instruction.next = 0b00000000000000000000010110010011
        yield delay(10)
        
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type  ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' I  ', bin(instruction,32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       
        

       # S type
        instruction.next = 0b00000101001101001001001100100011
        yield delay(10)
    
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type  ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' S  ', bin(instruction,32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       
       

       # SB type
        instruction.next = 0b00000001101001101001010001100011
        yield delay(10)
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type: ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' SB  ', bin(instruction,32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       
       
        # U type
        instruction.next = 0b00000000000010011011100010110111
        yield delay(10)
        
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type:  ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' U  ', bin(instruction).zfill(32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       
        # UJ type
        instruction.next = 0b00000000000000001000000001100111
        yield delay(10)
        
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%('Type:  ','instruction','opcode','rs1','rs2','rd','imm','funct3','funct7'))
        print("| %-15s | %-35s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s |"%(' UJ  ', bin(instruction).zfill(32),bin(opcode,7),bin(rs1,5),bin(rs2,5),bin(rd,5),bin(imm,12) ,bin(funct3,3),bin(funct7,7)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
       

    return instances()


test = test_decoder()
test.run_sim(100)





#------------------------------------------------------------------------------------------------#
#                                         Verilog Convertion                                     #
#------------------------------------------------------------------------------------------------#


def convert(hdl):
    Decoder_test=decoder32(instruction ,opcode,rs1, rs2, rd , imm, funct3, funct7)
    Decoder_test.convert(hdl = hdl)


# convert(hdl='Verilog')

