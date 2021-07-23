from myhdl import *
from instMem_v2 import instMem
from DecoderSec import decoder
from RegisterFile import RegisterFile
from control import control
from ALU import ALU
from mux import mux2_1
from Adder import adder
from BranchAdder import BranchAdder
from DataMemory import DataMemory

# ---------------------------------------------------------------------------- #
#                                  main Block                                  #
# ---------------------------------------------------------------------------- #



@block
def CPU(data, data_in, write_enable, clock, reset):
        
     
    dataMem,  ALUinput1, ALUinput2, ALU_result, rs1_Out, rs2_Out, jumpInstruction, imm = [Signal(intbv(0, min=-2**31, max=2**31)) for i in range(8)]
    instruction, nextInstruction, nextPCInput, resetPC, currentAddress = [Signal(intbv(0)[32:]) for i in range(5)]
    pcInput, address = [Signal(modbv(1, min=0, max=83*4)[32:]) for i in range(2)]
    rs1_In,rs2_In,rd=[Signal(intbv(0)[5:])for i in range(3)]
    funct3,memRead = [Signal(intbv(0)[3:]) for i in range(2)]
    funct7 = Signal(intbv(0)[7:])
    opCode = Signal(intbv(0)[7:])
    ALUOp = Signal(intbv(0)[5:])
    branch, memWrite, memToReg, immToALU, regWrite, reg1ToPC, pcToALU, enableReset = [Signal(bool(0)) for i in range(8)]
    Zero_Flag, Selector_Branch = [Signal(bool(0)) for i in range(2)]
    
    Decoder = decoder(instruction ,opCode ,rs1_In, rs2_In, rd , imm, funct3, funct7, clock)
    Instruction_Memory = instMem(instruction, address, data_in, write_enable)
    Control_Unit = control(branch, memWrite, memRead, memToReg, ALUOp, immToALU, regWrite, reg1ToPC, pcToALU, opCode, funct3, funct7)
    Adder4 = adder(address,nextInstruction)
    Register_File = RegisterFile( regWrite, rs1_Out, rs2_Out, rs1_In, rs2_In, rd, data)##
    ALU_Unit = ALU(ALUinput1,ALUinput2,ALUOp,ALU_result,Zero_Flag)
    Data_Memory = DataMemory(ALU_result, rs2_Out, memRead, memWrite, dataMem)
    Branch_Adder = BranchAdder(currentAddress,imm,jumpInstruction)
    Address_Mux = mux2_1(nextPCInput, nextInstruction, jumpInstruction, Selector_Branch)
    ALU_Mux1 = mux2_1(ALUinput1, rs1_Out, address, pcToALU)
    ALU_Mux2 = mux2_1(ALUinput2, rs2_Out, imm, immToALU)
    Feedback_Mux = mux2_1(data, ALU_result, dataMem, memToReg)
    Reg1PC_Mux = mux2_1(currentAddress, address, rs1_Out, reg1ToPC)
    Reset_Mux = mux2_1(pcInput, nextPCInput, resetPC, enableReset)

    @always(clock.posedge)
    def Program_Counter():
        if reset:
            resetPC.next = 0
            enableReset.next = 1
            reset.next = 0
        else:
            enableReset.next = 0
            address.next = pcInput

    @always(branch,Zero_Flag)
    def SelectorBranch():
        Selector_Branch.next = branch and Zero_Flag

    return instances()

data = Signal(intbv(0, min=-2**31, max=2**31))
data_in = Signal(intbv(0)[32:])
clock, write_enable, reset = [Signal(bool(0)) for i in range(3)]

@block
def test_CPU():
    
    testCPU = CPU(data, data_in, write_enable, clock, reset)

    @always(delay(5))
    def gen_clk():
        clock.next = not clock

    @instance
    def simulate():

        write_enable.next = 1
        reset.next = 1
        yield delay(10)
        with open('D:\ProgramsFile\VS code\EE361\Project_2_CPU_only\Sort_textCode.txt', 'r') as f:  
                for line in f:
                    data_in.next = Signal(intbv(line)[32:])
                    yield delay(10)
        write_enable.next = 0
        reset.next = 1
        yield delay(10)

        for i in range(500):
            yield delay(10)
            print("data", int(data))
            print("")
    
    return instances()

simulate_CPU = test_CPU()
simulate_CPU.run_sim(1700)

# def convert():
#     con = CPU(data, data_in, write_enable, clock, reset)
#     con.convert(hdl='Verilog')

# convert()