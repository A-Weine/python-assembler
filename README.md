Assembler MIPS básico para Mars 4.5 em Python.

Implementa um montador simples para a arquitetura MIPS, suportado pelo simulador Mars 4.5, e com foco em instruções básicas (sem pseudo-instruções).

**Colaboradores:**

* **Antonio Weine** (https://github.com/A-Weine)
* **Lucas Alexandre** (https://github.com/lucasalexandreao)

**Funcionalidades:**

* Suporte às seguintes instruções:
    * **R-Family:** sll, srl, jr, mfhi, mflo, mult, multu, div, divu, add, addu, sub, subu, and, or, slt, sltu, mul
    * **I-Family:** beq, bne, addi, addiu, slti, sltiu, andi, ori, lui, lw, sw
    * **J-Family:** j, jal

* Retorna tipos de instruções utilizadas e a quantidade de vezes que foram utilizadas.
* Retorna CPI Médio calculado baseado nos clocks das instruções contidas no "arquivo.csv"

* Tradução do código para formato binário ou hexadecimal.
    
**Uso:**
```
montador.py "seu_arquivo.asm" -b  # Gera código binário
montador.py "seu_arquivo.asm" -h  # Gera código hexadecimal
