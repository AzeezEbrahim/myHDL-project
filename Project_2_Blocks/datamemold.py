'''
@auther: tamam alahdal
'''

from myhdl import block,bin,Signal,intbv,delay,instance,always,instances
import random
#-----------------------------------------------------------------------
#                       main Block                                     -              
#-----------------------------------------------------------------------
@block
def DataMemory (address,dataIn,dataSize,memoryWrite,dataOut):
    memory = [Signal(intbv(0)[8:]) for i in range(4096)]     #memory size is 4k byte
    @always(address,dataIn)
    def Access():
        #read or write for 1 byte
        if dataSize == 1:
            if(memoryWrite):
               memory[address].next = dataIn[8:0]

               dataOut.next = 0
            else:
                dataOut.next[8:0] = memory[address]
                dataOut.next[16:8] = 0
                dataOut.next[24:16] = 0
                dataOut.next[32:24] = 0
        #read or write for 2 byte
        elif dataSize == 2:
            if(memoryWrite):
               memory[address].next = dataIn[8:0]
               memory[address+1].next = dataIn[16:8]
               dataOut.next = 0
            else:
                dataOut.next[8:0] = memory[address]
                dataOut.next[16:8] = memory[address+1]
                dataOut.next[24:16] = 0
                dataOut.next[32:24] = 0
        # read or write for 4 bytes
        elif dataSize == 4:
            if(memoryWrite):
               memory[address].next = dataIn[8:0]
               memory[address+1].next = dataIn[16:8]
               memory[address+2].next = dataIn[24:16]
               memory[address+3].next = dataIn[32:24]
               dataOut.next = 0
            else:

                dataOut.next[8:0] = memory[address]
                dataOut.next[16:8] = memory[address+1]
                dataOut.next[24:16] = memory[address+2]
                dataOut.next[32:24] = memory[address+3]
        else:
            dataOut.next = 0
    return Access
#----------------------------------------------------------------------- #
#                       Test Bench                                       #
#----------------------------------------------------------------------- #

# @block
# def DataMemoryTestBench():
#     #initializeation
#     address = Signal(intbv(0)[12:])     #4k-Bytes
#     memoryWrite = Signal(bool(0))
#     dataSize = Signal(intbv(0)[3:])   #size of data be read or weriten
#     dataIn = Signal(intbv(0)[32:])
#     dataOut = Signal(intbv(0)[32:])
#     #  ------ object --------
#     dataMemoryObject = DataMemory(address,dataIn,dataSize,memoryWrite,dataOut)

#     @instance
#     def monitor():
#         dataSizeList = []
#         addressList  = []
#         memoryWrite.next = 1
#         print("address          dataSize        dataIn          dataOut             MW")
#         for i in range(10):
#             dataSize.next = random.choice([1,2,4])
#             dataSizeList.append(int(dataSize.next))
#             delay(3)
#             if(dataSize.next == 0):
#                 dataIn.next = 0
#             elif (dataSize.next == 1): #1-byte
#                 dataIn.next = random.randrange(0, 2 ** 8)

#             elif (dataSize.next == 2): #2-bytes
#                 dataIn.next = random.randrange(0, 2 ** 16)

#             elif (dataSize.next == 4): #4-bytes
#                 dataIn.next = random.randrange(0, 2 ** 32)

#             address.next = address+dataSize
#             addressList.append(int(address.next))
#             yield delay(10)
#             print("%s                 %s             %s          %s            %s"%(int(address),dataSize,dataIn,dataOut,memoryWrite))
#         print("------------------------------------\n----------------------------\n--------------")
#         dataIn.next = 0  # random.randrange(0, 2 ** 8)
#         memoryWrite.next = 0
#         for i in range(10):
#             dataSize.next = dataSizeList[i]
#             address.next = addressList[i]
#             yield delay(10)
#             print("%s                 %s             %s          %s            %s"%(int(addressList[i]),dataSize,dataIn,dataOut,memoryWrite))
#     return instances()

# TestBench = DataMemoryTestBench()
# TestBench.run_sim(1000)

# # ----------------------------------------------------------------------- #
# #                        conversion                                       #
# # ----------------------------------------------------------------------- #

# def conversion():
#     # initializeation
#     address = Signal(intbv(0)[12:])     #4k-Bytes
#     memoryWrite = Signal(bool(0))
#     dataSize = Signal(intbv(0)[3:])   #size of data be read or weriten
#     dataIn = Signal(intbv(0)[32:])
#     dataOut = Signal(intbv(0)[32:])
#     #  ------ object --------
#     dataMemoryObject = DataMemory(address,dataIn,dataSize,memoryWrite,dataOut)
#     dataMemoryObject.convert(hdl ="verilog")
# conversion()