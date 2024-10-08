# Dicionário que estabelece um molde para os bits de cada instrução
instructions = {
    "sll" : ['R', 0, 0, None, None, None, 0],
    "srl" : ['R', 0, 0, None, None, None, 2],
    "jr" : ['R', 0, None, 0, 0, 0, 8],
    "mfhi" : ['R', 0, 0, 0, None, 0, 16],
    "mflo" : ['R', 0, 0, 0, None, 0, 18],
    "mult" : ['R', 0, None, None, 0, 0, 24],
    "multu" : ['R', 0, None, None, 0, 0, 25],
    "div" : ['R', 0, None, None, 0, 0, 26],
    "divu" : ['R', 0, None, None, 0, 0, 27],
    "add" : ['R', 0, None, None, None, 0, 32],
    "addu" : ['R', 0, None, None, None, 0, 33],
    "sub" : ['R', 0, None, None, None, 0, 34],
    "subu" : ['R', 0, None, None, None, 0, 35],
    "and" : ['R', 0, None, None, None, 0, 36],
    "or" : ['R', 0, None, None, None, 0, 37],
    "slt" : ['R', 0, None, None, None, 0, 42],
    "sltu" : ['R', 0, None, None, None, 0, 43],
    "mul" : ['R', 28, None, None, None, 0, 2],
    "beq" : ['I', 4, None, None, None],
    "bne" : ['I', 5, None, None, None],
    "addi" : ['I', 8, None, None, None],
    "addiu" : ['I', 9, None, None, None],
    "slti" : ['I', 10, None, None, None],
    "sltiu" : ['I', 11, None, None, None],
    "andi" : ['I', 12, None, None, None],
    "ori" : ['I', 13, None, None, None],
    "lui" : ['I', 15, 0, None, None],
    "lw" : ['I', 35, None, None, None],
    "sw" : ['I', 43, None, None, None],
    "j" : ['J', 2, None],
    "jal" : ['J', 3, None]
}

# Dicionário que associa cada nome de registrador ao seu respectivo número
registers = {
    "zero": 0,
    "at": 1,
    "v0": 2,
    "v1": 3,
    "a0": 4,
    "a1": 5,
    "a2": 6,
    "a3": 7,
    "t0": 8,
    "t1": 9,
    "t2": 10,
    "t3": 11,
    "t4": 12,
    "t5": 13,
    "t6": 14,
    "t7": 15,
    "s0": 16,
    "s1": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "t8": 24,
    "t9": 25,
    "k0": 26,
    "k1": 27,
    "gp": 28,
    "sp": 29,
    "fp": 30,
    "ra": 31
}
