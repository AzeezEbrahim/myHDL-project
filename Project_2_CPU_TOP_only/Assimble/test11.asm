.text 
main:                                   # @main
        lui     a6, %hi(data_in1)
        lw      a1, %lo(data_in1)(a6)
        lui     a2, %hi(data_in2)
        lw      t1, %lo(data_in2)(a2)
        add     a1, a1, t1
        lui     a7, %hi(data_out)
        addi    a5, a6, %lo(data_in1)
        lw      t0, 4(a5)
        addi    a2, a2, %lo(data_in2)
        lw      a4, 4(a2)
        sw      a1, %lo(data_out)(a7)
        lw      t2, 8(a5)
        lw      a0, 8(a2)
        sub     a3, t0, a4
        addi    a1, a7, %lo(data_out)
        sw      a3, 4(a1)
        or      a7, a0, t2
        lw      t0, 12(a5)
        lw      a0, 12(a2)
        lw      a3, 16(a5)
        lw      a2, 16(a2)
        sw      a7, 8(a1)
        and     a0, a0, t0
        sw      a0, 12(a1)
        sll     a0, a3, a2
        sw      a0, 16(a1)
        sw      t1, %lo(data_in1)(a6)
        sw      a4, 4(a5)
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
        j       .LBB0_1
.data 
data_in1:
        .word   9                       # 0x9
        .word   3                       # 0x3
        .word   7                       # 0x7
        .word   4                       # 0x4
        .word   1                       # 0x1

data_in2:
        .word   9                       # 0x9
        .word   5                       # 0x5
        .word   7                       # 0x7
        .word   4294967289              # 0xfffffff9
        .word   1                       # 0x1

data_out:
	.word  0
	.word  0
	.word  0
	.word  0
	.word  0