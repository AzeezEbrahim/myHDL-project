



'''
@auther: tamam alahdal
'''

from myhdl import block,bin,Signal,intbv,delay,instance,always,instances
import random
#-----------------------------------------------------------------------
#                       main Block                                     -              
#-----------------------------------------------------------------------
@block
def DataMemory (address,dataIn,memoryRred,memoryWrite,dataOut):
    memory = [Signal(intbv(0, min=-2**8, max=2**8)) for i in range(10240)]     #memory size is 10k byte
    # index = 0
    # with open('Sort_dataCode.txt', 'r') as f:
    #     for line in f:
    #         data_in = intbv(line)
    #         memory[index+3].next = data_in[32:24]
    #         memory[index+3]._update() 
    #         memory[index+2].next = data_in[24:16]
    #         memory[index+2]._update()
    #         memory[index+1].next = data_in[16:8]
    #         memory[index+1]._update()
    #         memory[index].next = data_in[8:0]
    #         memory[index]._update()
    #         index += 4 
    @always(address,dataIn)
    def Access():
        if memoryRred == 1:
            if(memoryWrite):
                memory[address].next = dataIn[8:0]
                dataOut.next = 0
            else:
                dataOut.next[8:0] = memory[address]
       
        if memoryRred == 2:
            if(memoryWrite):
                memory[address+1].next = dataIn[16:8]
                memory[address].next = dataIn[8:0]
                dataOut.next = 0
            else:
                dataOut.next[16:8] = memory[address+1]
                dataOut.next[8:0] = memory[address]
        if memoryRred == 3:
            if(memoryWrite):
                memory[address+3].next = dataIn[32:24]
                memory[address+2].next = dataIn[24:16]
                memory[address+1].next = dataIn[16:8]
                memory[address].next = dataIn[8:0]
                dataOut.next = 0
            else:
                dataOut.next[32:24] = memory[address+3]
                dataOut.next[24:16] = memory[address+2]
                dataOut.next[16:8] = memory[address+1]
                dataOut.next[8:0] = memory[address]
        else:
            dataOut.next = 0
    return Access
#----------------------------------------------------------------------- #
#                       Test Bench                                       #
#----------------------------------------------------------------------- #

# @block
# def DataMemoryTestBench():
#     #initializeation
#     address = Signal(intbv(0)[12:])
#     memoryWrite = Signal(bool(0))
#     dataIn = Signal(intbv(0)[8:])
#     dataOut = Signal(intbv(0)[8:])
#     #  ------ object --------
#     dataMemoryObject = DataMemory(address,dataIn,memoryWrite,dataOut)

#     @instance
#     def monitor():
#         print("address          dataIn          dataOut        MW")
#         for i in range(10):
#             dataIn.next = random.randrange(0,2**8)
#             memoryWrite.next = 1
#             address.next = i
#             yield delay(10)
#             print("%s                   %s          %s            %s"%(int(address),dataIn,dataOut,memoryWrite))
#         print("------------------------------------\n----------------------------\n--------------")
#         for i in range(10):
#             dataIn.next = 0 #random.randrange(0, 2 ** 8)
#             memoryWrite.next = 0
#             address.next = i
#             yield delay(10)
#             print("%s                    %s          %s            %s" % (int(address), dataIn, dataOut, bin(memoryWrite,1)))
#     return instances()

# TestBench = DataMemoryTestBench()
# TestBench.run_sim(1000)

# ----------------------------------------------------------------------- #
#                        conversion                                       #
# ----------------------------------------------------------------------- #

def conversion():
    # initializeation
    address = Signal(intbv(0)[12:])
    memoryWrite = Signal(bool(0))
    dataIn = Signal(intbv(0)[8:])
    dataOut = Signal(intbv(0)[8:])
    #  ------ object --------
    dataMemoryObject = DataMemory(address, dataIn, memoryWrite, dataOut)
    dataMemoryObject.convert(hdl ="verilog")
# conversion()