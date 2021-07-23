.text
addi x1,x0,50		
addi x2,x0,60
addi x3,x0,7		
addi x4,x0,80		
addi x5,x0,90	
addi x6,x0,-210
addi x7,x0,-47
addi x8,x0,-4
add x9,x1,x6	
sub x10,x2,x4
slli x11,x4,2
sra x12, x8, x3 
xor x13, x11, x12
sltiu x14, x6, 4

sw x2,32(x0)

sh x3,1024(x0)
sh x4,1040(x0)

sb x4,400(x0)
sb x5,440(x0)


lw x12,0(x0)
lw x13,32(x0)

lh x14,1024(x0)		#x3
lh x15,1040(x0)		#x4

lb x16,400(x0)		#x4
lb x17,440(x0)		#x5


beq x1,x12,yes
beq x2,x13,yes
beq x3,x14,yes
beq x4,x15,yes
beq x4,x16,yes
beq x5,x16,yes



yes:
Exit:...


no:

addi x20,x0,1
j yes