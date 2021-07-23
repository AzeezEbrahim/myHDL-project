from myhdl import *
from PC import pc
from instMem_v2 import instMem
from Decoder import decoder32
from RegisterFile import RegisterFile
from control import control
from ALU import ALU
from mux import mux
from mux_2 import mux2
from mux_3 import mux3
from mux_4 import mux4
from mux_5 import mux5
from Adder import adder
from BranchAdder import BranchAdder
from DataMemory import DataMemory

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #


@block
def PC_reg(PCOutput,PCInput,clock, enable):
    @always(clock.posedge)
    def passIt():
        if enable:
            PCOutput.next = PCInput
        else:
            PCOutput.next = 0
    return passIt



@block
def CPU(data, data_in, write_enable, clock, enable):
        
     
    dataMem,  ALUinput1, ALUinput2, ALU_result, rs1_Out, rs2_Out, jumpInstruction, imm = [Signal(intbv(0).signed()) for i in range(8)]
    instruction, nextInstruction, currentAddress = [Signal(intbv(0)[32:]) for i in range(3)]
    pcInput, address = [Signal(modbv(1, min=0, max=33)) for i in range(2)]
    rs1_In,rs2_In,rd=[Signal(intbv(0)[5:])for i in range(3)]
    funct3,memRead = [Signal(intbv(0)[3:]) for i in range(2)]
    funct7 = Signal(intbv(0)[7:])
    opCode = Signal(intbv(0)[7:])
    ALUOp = Signal(intbv(0)[5:])
    branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, pcToALU = [Signal(bool(0)) for i in range(7)]
    Zero_Flag, Selector_Branch = [Signal(intbv(0)[1:]) for i in range(2)]
    
    Selector_Branch.next = branch and Zero_Flag
    Instruction_Memory = instMem(instruction, address, data_in, write_enable)
    Adder4 = adder(address,nextInstruction)
    Decoder = decoder32(instruction ,opCode ,rs1_In, rs2_In, rd , imm, funct3, funct7)
    Register_File = RegisterFile( regWrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data)##
    ALU_Unit = ALU(ALUinput1,ALUinput2,ALUOp,ALU_result,Zero_Flag)
    Data_Memory = DataMemory(ALU_result, rs2_Out, memRead, memWrite, dataMem)
    Branch_Adder = BranchAdder(currentAddress,imm,jumpInstruction)
    Control_Unit = control(branch, memWrite, memRead, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, pcToALU, opCode, funct3, funct7)
    Address_Mux = mux5(pcInput, nextInstruction, jumpInstruction, Selector_Branch)
    ALU_Mux1 = mux(ALUinput1, rs1_Out, address, pcToALU)
    ALU_Mux2 = mux2(ALUinput2, rs2_Out, imm, immToALU)
    Feedback_Mux = mux3(data, ALU_result, dataMem, memToReg)
    Reg1PC_Mux = mux4(currentAddress, address, rs1_Out, reg1ToPC)
    PC_REG = PC_reg(address,pcInput,clock, enable)


    # @always(clock.posedge)
    # def Program_Counter():
    #     if enable:
    #         pcInput.next = 0
    #     else:
    #         address.next = pcInput

    return instances()

data = Signal(intbv(0, min=-2**31, max=2**31))
data_in = Signal(intbv(0)[32:])
clock, write_enable, enable = [Signal(bool(0)) for i in range(3)]

# ---------------------------------------------------------------------------- #
#                                   TestBench                                  #
# ---------------------------------------------------------------------------- #
@block
def test_CPU():
    
    testCPU = CPU(data, data_in, write_enable, clock, enable)

    @always(delay(5))
    def gen_clk():
        clock.next = not clock

    @instance
    def simulate():
        AssemblyCode = []
        with open('AssemblyCode.txt', 'r') as f:                  
                for line in f:
                    AssemblyCode.append(line)
        
        write_enable.next = 1
        yield delay(10)
        InstructionCode = []
        with open('InstructionCode.txt', 'r') as f:
                for line in f:
                    InstructionCode.append(intbv(line)[32:])
                    data_in.next = intbv(line)[32:]
                    yield delay(10)
        write_enable.next = 0
        enable.next = 1
        yield delay(10)
        enable.next = 0

        for i in range(33):
            yield delay(10)
            print("Assembly", AssemblyCode[i][:-1])
            print("Instruction", bin(InstructionCode[i],32))
            print("data", int(data))
            print("")
    
    return instances()

simulate_CPU = test_CPU()
simulate_CPU.run_sim(1000)
