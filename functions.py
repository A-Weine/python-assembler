def binary(number: int, length: int) -> str:
    # number(int): número na base decimal
    # length(int): quantidade de bits a ser utilizada para a representação binária
    
    if number < 0: # verifica se number é negativo
        number = (1 << length) + number # caso sim, desloca 1 em length bits para esquerda e soma com number
    return format(number, f'0{length}b') # o format retorna number como uma string em representação binária com length bits

def hexadecimal(number: str) -> str:
    # number(str): string que representa um número na forma binária
    
    number = int(number, 2) # converte a string hexadecimal number para um int em forma decimal
    return format(number, '08x') # o format retorna number como uma string em representação hexadecimal com 8 dígitos

def guardar_Instrucao(nome, dicionario):
    # nome(str): nome da instrução
    # dicionario(dict): dicionário que vai conter a instrução e quantidade de vezes que ela apareceu

    #condicional para verificar se a instrução já existe no dicionario
    if nome in dicionario:
        dicionario.update({nome: dicionario[nome] + 1}) #caso a instrução já exista, a quantidade de vezes que ela apareceu é atualizada em +1
    else:
        dicionario.update({nome: 1}) #caso a instrução seja nova no dicionario, então ela é armazenada o nome da instrução e a quantidade inicial: 1

def calcular_CPI(tipos_instrucoes, ciclos_instrucoes):
    #tipos_instrucoes(dict): dicionário que vai conter os nomes das instruções e a quantidade de vezes que elas aparecem
    #ciclos_instrucoes(dict): dicionário contendo o nome das instruções e seus respectivos clocks
    somatorio = 0 #variável que vai receber a soma do produto dos clocks das instruções pela quantidade de vezes que elas apareceram

    #laço que vai percorrer o dicionario possuindo a quantidade de aparições de cada instrução
    for instrucao in tipos_instrucoes:
        somatorio += ciclos_instrucoes[instrucao]*tipos_instrucoes[instrucao]
        #somatorio vai receber o produto do clock da instrução com a quantidade de vezes que ela apareceu
    CPI = somatorio/len(tipos_instrucoes)
    #É feito o calculo do CPI médio: somatorio/(quantidade de instruções)
    return CPI #O valor do CPI é retornado

def familyR_attribution(values: list[str], case: int, instruction: list, registers: dict):
    # values(list[str]): lista com o nome/número de cada registrador ou shift_amoount utilizado na instrução
    # case(int): número que representa o padrão de organização dos bits seguido pela instrução
    # instruction(list): lista que contém o molde dos grupos de bits da instrução
    # registers(dict): dicionário que associa cada nome de registrador ao seu respectivo número
    
    # Verifica qual dos padrões (case) é seguido pela instrução
    # positions determina a posição de cada um dos valores em values, respectivamente
    if case == 1:
        positions = [3, 4, 5]
    elif case == 2:
        positions = [2]
    elif case == 3:
        positions = [4]
    elif case == 4:
        positions = [2, 3]
    elif case == 5:
        positions = [2, 3, 4]

    #  Percorre values
    for position, value in enumerate(values):
        if value[0].isalpha(): # Caso o primeiro caractere do value (registrador) seja uma letra
            # Pega o valor int do registrador no dicionário registers e o coloca
            # na sua respectiva posição em instruction
            instruction[positions[position]] = registers[value]
        else: # Caso o primeiro caractere não seja uma letra
            # Converte a string para inteiro, conseguindo o valor numérico do registrador ou shift_amount diretamente
            # e o coloca na sua respectiva posiçao em instruction
            instruction[positions[position]] = int(value)

def familyI_attribution(values: list[str], case: int, instruction: list, registers: dict, pc: int, labels: dict):
    # values(list[str]): lista com o nome/número de cada registrador, imediato ou label utilizado na instrução
    # case(int): número que representa o padrão de organização dos bits seguido pela instrução
    # instruction(list): lista que contém o molde dos grupos de bits da instrução
    # registers(dict): dicionário que associa cada nome de registrador ao seu respectivo número
    # pc(int): número da linha da próxima instrução a ser lida
    # labels(dict): dicionário que associa cada label ao número de sua linha

    # Verifica qual dos padrões (case) é seguido pela instrução
    # positions determina a posição de cada um dos valores em values, respectivamente
    if case == 1:
        positions = [3, 4]
    elif case == 2:
        positions = [2, 3, 4]

    values_length = len(values) # representa a quantidade de elementos em values

    # Percorre cada elemento em values
    for position, value in enumerate(values):
        if value[0].isalpha(): # Caso o primeiro caractere do value seja uma letra
            if position != values_length - 1: # Caso o value não seja o último elemento em values, value é um registrador
                # Então pega o valor int do registrador no dicionário registers
                # e o coloca na sua respectiva posição em instruction
                instruction[positions[position]] = registers[value]
            else: # Caso value seja o último elemento de values, value é um label para salto condicional
                # Então calcula o valor realizando a subtração do número da linha da label (labels[value]) pelo número em pc
                # e coloca esse resultado na sua respectiva posição em instruction
                instruction[positions[position]] = labels[value] - pc
        else: # Caso o primeiro caractere do value não seja uma letra
            # Converte a string para inteiro, conseguindo o valor numérico do registrador ou imediato diretamente
            # e o coloca na sua respectiva posição em instruction
            instruction[positions[position]] = int(value)


def familyJ_attribution(value: str, instruction: list, labels: dict, base_address: int):
    # value(str): string que representa o imediato ou label utilizado na instrução 
    # instruction(list): lista que contém o molde dos grupos de bits da instrução
    # labels(dict): dicionário que associa cada label ao número de sua linha
    # base_address(int): endereço da primeira linha
    
    if value[0].isalpha(): # Caso o primeiro caractere do value seja uma letra, value é um label
        # Então resgata o número da linha do label no dicionário labels e a utiliza juntamente
        # com o base_address para calcular o endereço da linha do label e divide esse valor por 4.
        # O resulato é colocado na sua respectiva posição em instruction
        instruction[2] = int((((labels[value]-1)*4) + base_address) / 4)
    else: # Caso o primeiro caractere do value não seja uma letra, value é um imeditato
        # Converte a string para inteiro, conseguindo o valor numérico do imediato diretamente
        # e o coloca na sua respectiva posição em instruction
        instruction[2] = int(value)