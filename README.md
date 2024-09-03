Assembler MIPS básico para Mars 4.5 em Python.

Implementa um montador simples para a arquitetura MIPS, suportado pelo simulador Mars 4.5, e com foco em instruções básicas (sem pseudo-instruções).

**Funcionalidades:**

* Suporte às seguintes instruções:
    * **R-type:** sll, srl, jr, mfhi, mflo, mult, multu, div, divu, add, addu, sub, subu, and, or, slt, sltu, mul
    * **I-type:** beq, bne, addi, addiu, slti, sltiu, andi, ori, lui, lw, sw
    * **J-type:** j, jal

* Geração de código em formato binário ou hexadecimal.
  
**Uso:**
```
montador.py "seu_arquivo.asm" -b  # Gera código binário
montador.py "seu_arquivo.asm" -h  # Gera código hexadecimal
