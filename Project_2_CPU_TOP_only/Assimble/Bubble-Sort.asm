.text

main:
	#clear A2
	la	a0, A2
	addi	a1,x0, 8
	call clear

	#copy A1 to A2
	la	a0, A1
	la	a1, A2
	call copy
	
	#sort A2
	la	a0, A2
	addi	a1, zero, 8
	call sort
	
			
	la	a1, exitmsg
	addi	a2, zero, 31
	call print
	
# Setup the parameters to exit the program
# and then call Linux to do it.

        addi    a0, x0, 0   # Use 0 return code
        addi    a7, x0, 93  # Service command code 93 terminates
        ecall               # Call linux to terminate the program


print:   addi  a0, x0, 1      # 1 = StdOut
        #la    a1, exitmsg # load address of helloworld
        #addi  a2, x0, 13     # length of our string
        addi  a7, x0, 64     # linux write system call
        ecall                # Call linux to output the string
        ret
        


clear:	
	# a0 is the address of the array
	# a1 is the length of the array
	mv	t0, a1
	Loop:
	sw	zero,0(a0)
	addi	t0,t0,-1
	addi	a0,a0,4
	bne	t0, zero,Loop
	ret
	
copy:	
	# a0 is the address of the array A1
	# a1 is the address of the array A2
	mv	t0, a0
	mv	t1, a1
	CPLoop:
	lw	t2, 0(t0)
	sw	t2, 0(t1)
	addi	t0, t0, 4
	addi	t1, t1, 4
	bne	t2, zero,CPLoop
	ret


swap:
     lw  t0,0(a0)
     lw  t1,0(a1)
     sw  t1,0(a0)
     sw  t0,0(a1)
     ret
				
sort:
    addi  sp,sp,-32
    sw  ra,28(sp)
    sw  s0,24(sp)
    sw  s1,20(sp)
    sw  s2,16(sp)
    sw  s3,12(sp)
    sw  s4,8(sp)
    mv  s4,a0
    addi  s3,a1,-1
    bgtz  s3, L1
    j L2
    L4: mv  a0,s0
    addi  s0,s0,4
    lw  t1,0(a0)
    lw  t0,4(a0)
    ble t1,t0, L3
    mv  a1,s0
    call swap
    L3: addi  s1,s1,1
    blt s1,s2, L4
    L5: addi  s3,s3,-1
    beqz  s3, L2 
    L1: mv  s2,s3
    blez  s3, L5 
    mv  s0,s4
    li  s1,0
    j L4
    L2: lw  ra,28(sp)
    lw  s0,24(sp)
    lw  s1,20(sp)
    lw  s2,16(sp)
    lw  s3,12(sp)
    lw  s4,8(sp)
    addi  sp,sp,32
    ret
																																			
																																																																																																															
.data
A1:	.word 8, 5, 10, 9, 2, 6, 7, 0
A2: .word 0, 0, 0, 0, 0, 0, 0, 0
exitmsg: .ascii "The program is done, exiting..."
