#ALUNOS:
#LUCAS ALEXANDRE ALVES DE OLIVEIRA
#ANTONIO WEINE DE SOUSA SILVA

#IMPORTAÇÃO DE BIBLIOTECAS DO PYTHON
import sys
from csv import DictReader

#IMPORTAÇÃO DAS BIBLIOTECAS LOCAIS
from dicts import instructions, registers
from functions import (
    binary,
    calcular_CPI,
    familyI_attribution,
    familyJ_attribution,
    familyR_attribution,
    guardar_Instrucao,
    hexadecimal,
)

#OBS: CONSIDERA-SE QUE O CÓDIGO ASSEMBLY NÃO TEM ERROS

tipo_saida = "-b" #variável que vai receber o tipo de saída do programa
nome_arquivo = "" #variavel que vai receber o nome do arquivo

#RECEBIMENTO DOS ARGUMENTOS
if len(sys.argv) > 2: #verifica se o usuário passou mais de um argumento (nome do arquivo e tipo de saida)
    nome_arquivo = sys.argv[1] #caso sim, recebe o nome do arquivo em uma variável
    tipo_saida = sys.argv[2] #e recebe o tipo de saída (binário ou hexadecimal) em uma variável

#ABERTURA DO ARQUIVO PARA LEITURA
with open(nome_arquivo, 'r') as arquivo_leitura: #faz abertura do arquivo passado em modo de leitura
    lines = arquivo_leitura.readlines() #salva todas as linhas do arquivo em uma lista

nome_arquivo = nome_arquivo.split(".")[0].strip() #remove a extensão do nome do arquivo. Ex.: "mips1.asm" -> "mips1"

binary_lines = [] #lista que vai receber o resultado final em binario
hex_lines = ["v2.0 raw\n"] #lista que vai receber o resultado final em hexadecimal
#lista hexadecimal já inicializada com linha padrão "v2.0 raw"

base_address = 0x00400000 #define uma variável com o endereço base.
pc = 1 #inicializa o valor do program counter pra 1.
#No caso 1 corresponde à primeira linha de programa (0x00400000 no Mars)
#aqui essa variável não recebe o endereço em si, pois posteriormente esse endereço é calculado utlizando a quantidade de linhas.

label = "" #variavel que vai receber o nome da label.
labels = {} #dicionario que vai receber os labels junto de seus endereços(número de linha).
labels_solo = {} #dicionario que recebe labels sem endereço definido.
line_counter = 0 #variavel para contar as linhas do programa.

#LEITURA DAS LINHAS DO ARQUIVO Nº1
#é feita um laço para primeira passada no conteúdo do arquivo que foram salvas em uma lista,
#na qual vai ser feita somente a verificação das labels e seus endereços.
for linha in lines:
    
    if '.' not in linha: #verifica se a linha possui alguma diretiva, caso sim, a linha é ignorada.
        linha = (linha.split("#")[0].strip()).split() #remove os comentários da linha e divide ela em uma lista.
        
        if len(linha) > 0 and ':' in linha[0]: #verifica se a linha pós limpeza possui conteúdo e se possui uma label.
            label = linha[0].split(":")[0] #caso sim, a variavel recebe o primeiro elemento da linha, que vai ser o label.

        #verifica pelo tamanho da lista se a linha possui alguma instrução (visto que em linha, após a remoção de diretivas e comentários,
        #se a linha possuir mais de um elemento, então com certeza possui uma instrução).
        if len(linha) > 1:
            line_counter += 1 #caso sim, a variavel de contagem de linhas é incrementada em 1.

            #Todas as labels que estavam sem endereço no dicionario labels_solo são atualizadas e adicionadas ao dicionario geral de labels.
            for itens in labels_solo: #o dicionario labels_solo (labels sem endereço) é percorrido.
                labels_solo.update({itens:line_counter}) #todas as labels previamente sem endereço recebem o endereço da linha atual.
                labels.update({itens:labels_solo[itens]}) #o dicionario geral de labels recebe o dicionario labels_solo.
            labels_solo.clear() #é feita limpeza do dicionario de labels sem endereço, visto que foram atualizados.
            
            if ':' in linha[0]: #verifica se a linha da instrução possui uma label.
                #caso a linha possua uma label, esse label é adicionado no dicionario de labels com seu respectivo endereço (linha atual)
                labels.update({label:line_counter})
                
        elif len(linha) > 0: #verifica se a linha possui somente o label.
            labels_solo.update({label:None}) #se sim, o label é adicionado ao dicionario de labels sem endereço definido.

#Após percorrer todas as linhas do programa, é verificado se ainda há algum label sem endereço definido no dicionario.
if len(labels_solo) > 0:
#Caso sim, é feito um laço percorrendo esse dicionario e os endereços das labels restantes são atualizados para uma linha após a ultima instrução.
#Isso é feito para que, caso haja algum label após a última instrução, sejam considerados corretamente (de acordo com o Mars).
    for itens in labels_solo: #laço percorrendo o dicionario
        labels_solo.update({itens:line_counter+1}) #labels sem endereço recebem o devido endereço
        labels.update({itens:labels_solo[itens]}) #dicionario geral de labels recebe os labels restantes.
    labels_solo.clear() #é feita limpeza do dicionario de labels sem endereço, visto que foram atualizados.

tipos_instrucoes = {} #é criado o dicionario que vai receber a quantidade de instruções de cada tipo.

#LEITURA DAS LINHAS DO ARQUIVO Nº2
#é feita outro laço para segunda passada no conteúdo do arquivo que foram salvas em uma lista,
#na qual será realizada a verificação das instruções completas.
for linha in lines:
    
    if '.' not in linha: #Linhas com diretivas são ignoradas completamente
        linha = (linha.split("#")[0].strip()).split(":") #ignora todos os comentários e divide a linha em uma lista em que o primeiro elemento é um possível label.
        instrucao = "" #inicializa variável que vai receber o nome da instrução.

        #Verifica se o primeiro elemento não é vazio (pode ser um label ou já o inicio da instrução).
        if len(linha[0]) > 0: 

            #verifica se a lista possui apenas um elemento, caso sim, esse elemento é a instrução,
            #visto que a linha foi repartida utilizando : como separador (simbolo de label).
            if len(linha) == 1:
                pc += 1 #caso sim, valor de pc é incrementado para próxima instrução.
                lista = linha[0].replace(",", "").replace("$", "").strip().split() 
                #a linha salva na lista é repartida em palavras,
                #removendo completamente caracteres de registradores ($), virgulas e espaços em branco no inicio e fim.
                instrucao = instructions[lista[0]] #variável recebe o primeiro elemento da linha, que vai ser obrigatoriamente o nome da instrução dada as verificações até o momento.
                guardar_Instrucao(lista[0], tipos_instrucoes) #a instrução é salva no dicionario de tipos de instruções no código.

            #como foi feita divisão da linha com o separador de labels, caso a lista possua dois elementos então contém um label nela, 
            #dada a separação, caso a linha contenha apenas o label, a lista terá primeiro elemento como o label e o segundo vazio
            #é feita a verificação dessas condições:
            elif len(linha) == 2 and not (linha[1]):
                continue #Em caso positivo, então a linha contém apenas o label e é ignorada.
                
            else: #Por fim, em caso negativo paras condições anteriores, então a linha possui um label e a instrução.
                pc += 1 #é feito incremento de pc para próxima instrução
                lista = linha[1].replace(",", "").replace("$", "").strip().split()
                #a linha salva na segunda posição da lista (posição pertencente à instrução) é repartida em palavras,
                #removendo completamente caracteres de registradores ($), virgulas e espaços em branco no inicio e fim.

                #é utilizado o nome da instrução (primeiro elemento da nova lista)
                #no dicionario "instructions" que possui o molde de cada instrução guardado
                instrucao = instructions[lista[0]] #a variável "instrucao" recebe o molde da instrucao atual (uma lista)
                guardar_Instrucao(lista[0], tipos_instrucoes) #função guardar_Instrucao é chamada, com as informações da instrução atual como parametro
                #Essa função guarda em um dicionario o tipo da instrução junto da quantidade de vezes que ela aparece.

            family_instruction = instrucao[0] #variável recebe a familia da instrucao atual de dentro do molde.
            opcode_instruction = instrucao[1] #variável recebe o opcode da instrucao atual.

            #É feita verificação da famila da instrução atual, para saber se é uma instrução de familia I, J ou R.
            if family_instruction == 'R': #verifica se é da familia R
                function_instruction = instrucao[6] #variável recebe o número de função da instrução atual.
                #especifico da familia R
                
                bits = [6, 5, 5, 5, 5, 6] #variável recebe forma de organização de bits da familia R
                #variáveis correspondentes aos registradores utilizados e shift_amount da familia R são inicializadas.
                rs = "" #registrador de origem
                rt = "" #registrador alvo
                rd = "" #registrador de destino
                sa = "" #shift amount

                #Verifica-se o opcode da instrução para saber qual metodo de organização de registradores utilizar
                if opcode_instruction == 0:

                    #São feitas verificações do número de função,
                    #para que os registradores sejam organizados no formato correto da instrução (de acordo com a tabela da familia R)
                    if function_instruction == 0 or function_instruction == 2: #instruções sll e srl
                        case = 1 #variável que representa o padrão de organização dos bits seguido pela instrução
                        #Se refere ao modo que os registradores são organizados para o molde
                        
                        #É feita atribuição dos registradores que foram lidos na linha seguindo o formato da instrução
                        rd = lista[1]
                        rt = lista[2]
                        sa = lista[3]

                        values = [rt, rd, sa] #lista que recebe os registradores e shiftamount em ordem

                        #função familyR_attribution é chamada, recebendo como parametro a lista de registradores, o caso
                        #a instrução e o dicionario de registradores.
                        familyR_attribution(values, case, instrucao, registers)
                        #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

                    elif function_instruction == 8: #instrução jr
                        case = 2 #variável que representa o padrão de organização dos bits seguido pela instrução
                        #Se refere ao modo que os registradores são organizados para o molde
                        
                        rs = lista[1] #atribuição do registrador que está na linha lida para variável

                        values = [rs] #lista recebendo o registrador

                        #feita chamada da função familyR_attribution
                        familyR_attribution(values, case, instrucao, registers)
                        #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

                    elif 16 == function_instruction or function_instruction == 18: #instruções mfhi e mflo
                        case = 3 #variável que representa o padrão de organização dos bits seguido pela instrução
                        #Se refere ao modo que os registradores são organizados para o molde
                        
                        rd = lista[1] #atribuição do registrador que está na linha lida para variável

                        values = [rd] #lista recebe o registrador
                        
                        #feita chamada da função familyR_attribution
                        familyR_attribution(values, case, instrucao, registers)
                        #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

                    elif 24 <= function_instruction <= 27: #instruções mult, multu, div e divu
                        case = 4 #variável que representa o padrão de organização dos bits seguido pela instrução
                        #Se refere ao modo que os registradores são organizados para o molde

                        #É feita atribuição dos registradores que foram lidos na linha seguindo o formato da instrução
                        rs = lista[1]
                        rt = lista[2]

                        values = [rs, rt] #lista recebe os registradores em ordem
                        
                        familyR_attribution(values, case, instrucao, registers)
                        #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

                    elif 32 <= function_instruction <= 37 or 42 <= function_instruction <= 43: #instruções add, addu, sub, subu, and, or, slt, sltu
                        case = 5 #variável que representa o padrão de organização dos bits seguido pela instrução
                        #Se refere ao modo que os registradores são organizados para o molde

                        #É feita atribuição dos registradores que foram lidos na linha seguindo o formato da instrução
                        rd = lista[1]
                        rs = lista[2]
                        rt = lista[3]

                        values = [rs, rt, rd] #lista recebe os registradores em ordem

                        #feita chamada da função familyR_attribution
                        familyR_attribution(values, case, instrucao, registers)
                        #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

                elif opcode_instruction == 28 and function_instruction == 2: #instrução mul
                    case = 5 #variável que representa o padrão de organização dos bits seguido pela instrução
                    #Se refere ao modo que os registradores são organizados para o molde

                    #É feita atribuição dos registradores que foram lidos na linha seguindo o formato da instrução
                    rd = lista[1]
                    rs = lista[2]
                    rt = lista[3]

                    values = [rs, rt, rd] #lista recebe os registradores em ordem

                    #feita chamada da função familyR_attribution
                    familyR_attribution(values, case, instrucao, registers)
                    #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

            elif family_instruction == "I": #verifica se é da familia I
                bits = [6, 5, 5, 16] #variável recebe o formato de organização dos bits da família I

                #é feita inicialização das variáveis correnspondentes aos registradores e a constante.
                rs = "" #registrador de origem
                rt = "" #registrador alvo
                immediate = "" #constante

                if 4 <= opcode_instruction <= 5: #instruções beq e bne
                    case = 2 #variável que representa o padrão de organização dos bits seguido pela instrução
                    #Se refere ao modo que os registradores são organizados para o molde

                    #É feita atribuição dos registradores e constante que foram lidos na linha seguindo o formato da instrução
                    rs = lista[1]
                    rt = lista[2]
                    immediate = lista[3]

                    values = [rs, rt, immediate] #lista recebe os registradores e constante em ordem

                    #feita chamada da função familyI_attribution, que tem mesmo objetivo da função familyR_attribution
                    familyI_attribution(values, case, instrucao, registers, pc, labels)
                    #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"
                
                elif 8 <= opcode_instruction <= 13: #instruções addi, addiu, slti, sltiu, andi, ori
                    case = 2 #variável que representa o padrão de organização dos bits seguido pela instrução
                    #Se refere ao modo que os registradores são organizados para o molde

                    #É feita atribuição dos registradores e constante que foram lidos na linha seguindo o formato da instrução
                    rt = lista[1]
                    rs = lista[2]
                    immediate = lista[3]

                    values = [rs, rt, immediate] #lista recebe os registradores e constante em ordem

                    #feita chamada da função familyI_attribution
                    familyI_attribution(values, case, instrucao, registers, pc, labels)
                    #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"
                    
                elif opcode_instruction == 15: #instrução lui
                    case = 1 #variável que representa o padrão de organização dos bits seguido pela instrução
                    #Se refere ao modo que os registradores são organizados para o molde

                    #É feita atribuição dos registradores e constante que foram lidos na linha seguindo o formato da instrução
                    rt = lista[1]
                    immediate = lista[2]

                    values = [rt, immediate] #lista recebe os registradores e constante em ordem

                    #feita chamada da função familyI_attribution
                    familyI_attribution(values, case, instrucao, registers, pc, labels)
                    #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"
                
                elif opcode_instruction == 35 or opcode_instruction == 43: #instruções lw e sw
                    case = 2 #variável que representa o padrão de organização dos bits seguido pela instrução
                    #Se refere ao modo que os registradores são organizados para o molde

                    #É feita padronização dos registradores e contante lidos na linha
                    #Isso é feito, pois nessas 2 instruções eles são informados no formato:
                    #Ex.: 0 ($t0);
                    #A padronização é para remover quaisquer espaços que hajam entre os registradores e a constante
                    
                    reorganizar = "".join(lista[2::]) #registrador e constante são passados para uma string, removendo os espaços contidos.
                    separated_list = reorganizar.split("(") #a string é dividida utilizando o parenteses como separador.
                    #nesse caso a constante será o primeiro elemento da lista e o registrador o segundo
                        
                    rt = lista[1] #variável recebe registrador da linha, que é disposto de forma normal.
                    
                    rs = separated_list[1].replace(")", "") #variável recebe registrador da lista padronizada, que é disposto entre parenteses.
                    #os parenteses são removidos na passagem
                    
                    immediate = separated_list[0] #variável recebe constante da lista padronizada

                    values = [rs, rt, immediate] #lista recebe os registradores e constante em ordem

                    #feita chaada da função familyI_attribution
                    familyI_attribution(values, case, instrucao, registers, pc, labels)
                    #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

            elif family_instruction == "J": #instruções da familia J (j e jal)
                #Na familia J, como as duas instruções possuem o molde seguindo a mesma lógica, não é necessário
                #fazer verificações para alocação das informações
                bits = [6, 26] #bits recebe o formato dos bits da familia J
                address = lista[1] #variável recebe o endereço lido na linha 

                #função familyJ_attribution é chamada, tem mesmo objetivo que a função familyR_attribution e familyJ_attribution
                familyJ_attribution(address, instrucao, labels, base_address)
                #Essa função preenche os valores corretamente dentro do molde que está na lista "instrucao"

            bits32 = "" #é inicializada variável que vai receber a linha de 32 bits, mas em binário
            
            for position, number in enumerate(instrucao[1:]): #percorre a lista de instrução(que já está com seus valores corretamente preenchidos)
                bits32 += binary(number, bits[position]) 
                #é utilizada a função binary para converter os elementos da lista para um valor binário, já na posição correta
            bits32 += '\n'#é adicionada uma quebra da linha ao final
            binary_lines.append(bits32) #a lista binary_lines recebe a linha em binário.

saida = [] #lista contendo linhas de saida para escritura no arquivo (bin ou hex)

#É feito uma verificação de qual o tipo de saída escolhida pelo usuário
if tipo_saida == "-b": #caso seja binário:
    nome_arquivo = nome_arquivo + ".bin" #o nome do arquivo recebe extensão ".bin"
    saida = binary_lines #a lista de saída recebe as linhas em formato binário

elif tipo_saida == "-h": #caso seja hexadecimal:
    nome_arquivo = nome_arquivo + ".hex" #nome do arquivo recebe extensão ".hex"

    #é feito um laço para percorrer as linhas em formato binário
    #e essas linhas são convertidas para hexadecimal utilizando a função "hexadecimal"
    for line in binary_lines:
        hex_lines.append(hexadecimal(line) + "\n") #as linhas são adicionadas na lista "hex_lines"
    saida = hex_lines #a lista de saída recebe as linhas em formato hexadecimal

#ABERTURA DO ARQUIVO PARA ESCRITA
#caso o arquivo com o nome escolhido não exista, então é criado um novo arquivo
#e caso já exista um arquivo com o mesmo nome, então é sobrescrito
with open(nome_arquivo, "w") as file:
    
    for line in saida: #laço percorre todas as linhas da lista de saída
        file.write(line) #as linhas são escritas no arquivo

# CALCULO DE CPI

#é criado dicionário que irá receber a quantidade de clocks de cada instrução e o nome da instrução.
instrucao_clocks = {}

#ABERTURA DO ARQUIVO CSV PARA LEITURA
with open('arquivo.csv', 'r') as arquivo:
    #linhas do arquivo são lidas e armazenadas em um dicionário
    #é utilizada a função DictReader da biblioteca "csv".
    arquivo_leitura = DictReader(arquivo, delimiter=',')

    #laço percorre cada linha armazenada no dicionário
    for item in arquivo_leitura:
        instrucao = list(item.values())[0] #variável recebe o nome da instrução (de acordo com o padrão do arquivo)
        clocks = int(list(item.values())[1]) #variável recebe a quantidade de clocks da instrução (de acordo com o padrão do arquivo)
        instrucao_clocks.update({instrucao:clocks}) #o nome da instrução e seu clock são armazenados em um dicionario

#Obs.: não é necessário fechar o arquivo, pois o "with" já realiza isso automaticamente.

CPI = calcular_CPI(tipos_instrucoes, instrucao_clocks) #variável que vai receber o CPI médio do programa
#É utilizada função "calcular_CPI" que recebe os dicionarios referentes a instruções como parametro

#SAÍDA DO PROGRAMA:
print("Quantidade por tipos de instruções:")

for nome, quantidade in tipos_instrucoes.items(): #laço percorre o dicionario de tipos de instruções
    print(f"{nome}: {quantidade}") #imprime nome da instrução com a quantidade de vezes que ela apareceu

print("\nCPI médio: ", CPI) #imprime o CPI médio do programa
