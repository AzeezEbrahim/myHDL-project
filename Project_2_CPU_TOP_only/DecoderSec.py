from myhdl import block, always_comb, instances, instance, Signal, intbv, delay,bin,concat , always
#------------------------------------------------------------------------------------------------#
#                                         Main Block                                             #
#------------------------------------------------------------------------------------------------#

@block
def decoder(instruction ,opcode ,rs1, rs2, rd , imm, funct3, funct7 , clock):

    @always(instruction)
    def controlDecode():
        opcode.next = instruction[7:]
        funct3.next =instruction[15:12]
        funct7.next = instruction[32:25]

    @always(clock.negedge)
    def decode32():
        rs1.next=instruction[20:15]
        rs2.next=instruction[25:20]
        rd.next=instruction[12:7]
        
    @always(clock.posedge)
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
        elif opcode_in == 0b1101111:
            imm.next = intbv(concat( instruction[32], instruction[20:12], instruction[20], instruction[31:25]).signed(),min=-2**31, max=2**31)
        elif opcode_in == 0b1100111:
            imm.next = intbv(instruction[32:21].signed(),min=-2**31, max=2**31)
          #  UJ type instructions
        else:
            imm.next=0
           # print('bubble')

    return instances()