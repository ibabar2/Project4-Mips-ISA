import time

print("Authors: Vraj Patel, Imran Babar")
print("Simulator Using Mips ISA")
print("Operations Supported: add, sub, xor, addi, beq, bne, slt, lw, sw")





def FileToArray(arrayfile):
    ReturnFIleArray = []
    for line in arrayfile:
        ReturnFIleArray.append(line[0:10].rstrip())
    return ReturnFIleArray


def PrintingTheOutput(registerArray, pc):
    print("pc): ", pc)
    for i in range(1, 8):
        print("$" + str(i) + ": ", registerArray[i])


def EachInstruction(MachineCodeInHex):
    BinStr = str(bin(int(MachineCodeInHex, 16))[2:].zfill(32))
    rd = 0
    rt = 0
    rs = 0
    DestinationReg = 0
    SourceReg = []
    if BinStr[0:6] == "000000":
        rd = int(BinStr[16:21], 2)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        DestinationReg = rd
        SourceReg = [rt, rs]
        print(" $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
    # BRANCH
    elif BinStr[0:6] == "000100" or BinStr[0:6] == "000101":
        # B** $rs, $rt, imm
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        SourceReg = [rt, rs]
        # ADDI
    elif BinStr[0:6] == "001000":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        SourceReg = [rs]
        DestinationReg = rt
    # LW
    elif BinStr[0:6] == "100011":
        # LW $rt, imm($rs)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        SourceReg = [rs]
        DestinationReg = rt
    # SW
    elif BinStr[0:6] == "101011":
        # SW $rt, imm($rs)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        SourceReg = [rt, rs]
    return [SourceReg, DestinationReg]


def execute_operation(MachineCodeInHex,data_mem, registerArray, pc, MulticycleInstrucCount, pipe_delays, MachineCode_Old, MachineCode_New):
    BinStr = str(bin(int(MachineCodeInHex, 16))[2:].zfill(32))
    # SUB
    if BinStr[0:6] == "000000" and BinStr[21:32] == "00000100010":
        rd = int(BinStr[16:21], 2)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        print("SUB $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        registerArray[rd] = registerArray[rs] - registerArray[rt]
        MulticycleInstrucCount[1] += 1
        print("The Number of Multicycles are 4 Cycles")
        # ADDI
    elif BinStr[0:6] == "001000":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        imm_bin = BinStr[16:32]
        if imm_bin[0] == "1":
            PositionNum = int(imm_bin, 2)
            EverythingOne = 0b1111111111111111
            num = EverythingOne - PositionNum + 1
            imm= 0 - num
        else:
            num = int(imm_bin, 2)
            imm = num
        #imm = ConvBinToDec(imm_bin)
        print("ADDI $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        registerArray[rt] = registerArray[rs] + imm
        MulticycleInstrucCount[1] += 1
        print("The Number of Multicycles are 4 Cycles")
    # ADD
    elif BinStr[0:6] == "000000" and BinStr[21:32] == "00000100000":
        rd = int(BinStr[16:21], 2)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        print("ADD $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        registerArray[rd] = registerArray[rs] + registerArray[rt]
        MulticycleInstrucCount[1] += 1
        print("The Number of Multicycles are 4 Cycles")


    # BEQ
    elif BinStr[0:6] == "000100":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        imm_bin = BinStr[16:32]
        if imm_bin[0] == "1":
            PositionNum = int(imm_bin, 2)
            EverythingOne = 0b1111111111111111
            num = EverythingOne - PositionNum + 1
            imm= 0 - num
        else:
            num = int(imm_bin, 2)
            imm = num
        #imm =ConvBinToDec(imm_bin)
        print("BEQ $" + str(rs) + ", $" + str(rt) + ", " + str(imm))
        if registerArray[rt] == registerArray[rs]:
            pc= pc + (imm * 4)
            print("STALL")
            pipe_delays[1]= pipe_delays[1]+ 1
        MulticycleInstrucCount[0]= MulticycleInstrucCount[0]+ 1
        print("The Number of Multicycles are 3 Cycles")
        data_registers = EachInstruction(MachineCode_Old)
        DestinationReg = data_registers[1]
        if DestinationReg == rt or DestinationReg == rs:
            print("STALL")
            pipe_delays[0]= pipe_delays[0]+ 1
    # BNE
    elif BinStr[0:6] == "000101":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        imm_bin = BinStr[16:32]
        if imm_bin[0] == "1":
            PositionNum = int(imm_bin, 2)
            EverythingOne = 0b1111111111111111
            num = EverythingOne - PositionNum + 1
            imm= 0 - num
        else:
            num = int(imm_bin, 2)
            imm = num
        #imm =ConvBinToDec(imm_bin)
        print("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        if registerArray[rt] != registerArray[rs]:
            pc= pc + (imm * 4)
            print("STALL")
            pipe_delays[1]= pipe_delays[1]+1
        MulticycleInstrucCount[0]= MulticycleInstrucCount[0]+ 1
        print("The Number of Multicycles are 3 Cycles")
        data_registers = EachInstruction(MachineCode_Old)
        DestinationReg = data_registers[1]
        if DestinationReg == rt or DestinationReg == rs:
            print("STALL")
            pipe_delays[0]=  pipe_delays[0]+ 1
    # SLT
    elif BinStr[0:6] == "000000" and BinStr[21:32] == "00000101010":
        rd = int(BinStr[16:21], 2)
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        print("SLT $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        if registerArray[rs] < registerArray[rt]:
            registerArray[rd] = 1
        else:
            registerArray[rd] = 0
        MulticycleInstrucCount[1]= MulticycleInstrucCount[1]+ 1
        print("The Number of Multicycles are 4 Cycles")
    # LW
    elif BinStr[0:6] == "100011":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        imm_bin = BinStr[16:32]
        if imm_bin[0] == "1":
            PositionNum = int(imm_bin, 2)
            EverythingOne = 0b1111111111111111
            num = EverythingOne - PositionNum + 1
            imm= 0 - num
        else:
            num = int(imm_bin, 2)
            imm = num
        #imm =ConvBinToDec(imm_bin)
        print("LW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        d_mem_index = int((registerArray[rs] - 0x2000 + imm) / 4)
        d_mem_value = data_mem[d_mem_index]
        print("MEMORY INDEX FOR LW", d_mem_index)
        registerArray[rt] = d_mem_value
        MulticycleInstrucCount[2] =  MulticycleInstrucCount[2]+ 1
        print("The Number of Multicycles are 5 Cycles")
        data_registers = EachInstruction(MachineCode_New)
        SourceReg = data_registers[0]
        for i in range(0, len(SourceReg)):
            cur_src_reg =SourceReg[i]
            print("SOURCE REG: ",SourceReg[i])
            if cur_src_reg == rt:
                print("DELAY FOR LW")
                pipe_delays[0]= pipe_delays[0]+ 1

    # SW
    elif BinStr[0:6] == "101011":
        rt = int(BinStr[11:16], 2)
        rs = int(BinStr[6:11], 2)
        imm_bin = BinStr[16:32]
        if imm_bin[0] == "1":
            PositionNum = int(imm_bin, 2)
            EverythingOne = 0b1111111111111111
            num = EverythingOne - PositionNum + 1
            imm= 0 - num
        else:
            num = int(imm_bin, 2)
            imm = num
        #imm =ConvBinToDec(imm_bin)
        print("SW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        d_mem_index = int((registerArray[rs] - 0x2000 + imm) / 4)
        data_mem[d_mem_index] = registerArray[rt]
        MulticycleInstrucCount[1]= MulticycleInstrucCount[1]+1
        print("The Number of Multicycles are 4 Cycles")
    pc= pc + 4
    return [data_mem, registerArray, pc, MulticycleInstrucCount, pipe_delays]
def simulator(ImemArray):
    ImemFile = open(ImemArray, "r")
    instr_mem = FileToArray(ImemFile)
    registerArray = [0, 0, 0, 0, 0, 0, 0, 0]  
    data_mem = [0] * 1023  
    pc = 0
    index = 0
    MachineCodeInHex = instr_mem[pc]
    MachineCodeInHex_old = "0xffffffff"
    MachineCodeInHex_new = "0xffffffff"
    MulticycleInstrucCount = [0, 0, 0]    
    dic = 0     
    pipe_delays = [0, 0]   
    while MachineCodeInHex != "0x1000FFFF" or MachineCodeInHex != "0x1000ffff":
        if MachineCodeInHex == "0x1000ffff":
            dic = dic + 1
            MulticycleInstrucCount[0]= MulticycleInstrucCount[0] + 1
            break

        if index == 0:
            MachineCodeInHex_old = "0xffffffff"
            MachineCodeInHex_new = instr_mem[index + 1]
        elif index == (len(instr_mem) - 2):
            MachineCodeInHex_old = instr_mem[index - 1]
            MachineCodeInHex_new = "0xffffffff"
        else:
            MachineCodeInHex_old = instr_mem[index - 1]
            MachineCodeInHex_new = instr_mem[index + 1]
        data_set = execute_operation(MachineCodeInHex, data_mem, registerArray, pc, MulticycleInstrucCount, pipe_delays, MachineCodeInHex_old, MachineCodeInHex_new)
        data_mem = data_set[0]
        registerArray = data_set[1]
        pc = data_set[2]
        MulticycleInstrucCount = data_set[3]
        pipe_delays = data_set[4]

        print("The INDEX is now at :          ", index)
        print("The New INSTRUCTION will be:", MachineCodeInHex_new)

        PrintingTheOutput(registerArray, pc)
        print("The things stored in Data Memory are the following:", data_mem[0:10], "\n")
        index = int(pc / 4)
        MachineCodeInHex = instr_mem[index]
        dic += 1

    three_cycles = MulticycleInstrucCount[0]
    four_cycles = MulticycleInstrucCount[1]
    five_cycles = MulticycleInstrucCount[2]
    multi_cyclesCounter = (3 * three_cycles) + (4 * four_cycles) + (5 * five_cycles)
    print("DIC Count for Single Cycle is:", dic)
    print("\n")

    print("MultiCycle Details are as follows:")
    print("3 cycle instructions=", three_cycles, "4 cycle instructions=", four_cycles)
    print("5 cycle instructions=", five_cycles, " Total number of cycles=",multi_cyclesCounter)
    print("\n")

    delay_hazards = pipe_delays[0]
    ctrl_hazards = pipe_delays[1]
    p_cycles = dic + 4 + delay_hazards + ctrl_hazards
    print("PIPELINING DETAILS:")
    print("Amount of Control Hazard Delays:", ctrl_hazards, ",Amount of Data Hazard Delays:", delay_hazards)
    print("Total Number of Cycles for pipelining:    ", p_cycles)
print("\n************A1*********\n**********************\n")
simulator("A1.txt")
print("\n\n************A2*********\n*********************\n")
simulator("A2.txt")
print("\n\n************B1*********\n*********************\n")
simulator("B1.txt")
print("\n\n************B2*********\n*********************\n")
simulator("B2.txt")
#simulator("i_mem.txt")
