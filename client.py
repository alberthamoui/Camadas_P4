from comands import *
from enlace import *
import time
import numpy as np
import random
import binascii



# A SER FEITO

# EXTRA


serialName = "COM4"
# serialName = "COM7"
#serialName = "COM6"


comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        contador = 0
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")

        imagem = "inicial.jpeg"
        txBuffer = open(imagem, 'rb').read()
        numPack = len(txBuffer)

        teste = "client\inicial.jpeg"
        # txBuffer = open(teste, 'rb').read()
        # pacotes = None # O QUE EH ISSO??
        # tamPacotes = len(txBuffer)
        # tamPacotesBytes = (tamPacotes).to_bytes(1, byteorder='big')
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        txBuffer = open(teste, 'rb').read()

        tamPacotes = len(txBuffer)

        # Tamanho de cada payload (114 bytes)
        tam_pacote = 114

        pacotes = []
        # Dividir os bytes da imagem em pacotes de 50 bytes
        for i in range(0, len(txBuffer), tam_pacote):
            pacote = txBuffer[i:i + tam_pacote]
            pacotes.append(pacote)
        
        print('\n\n')
        print(pacotes)
        print('\n\n')

        tamanho_pacotes = len(pacotes)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # HandShake
        comeca = False
        validado = False

        while not comeca:
            if validado == False:
                resposta = input(str("Deseja continuar? [s/n]: "))
                if resposta == 's':
                    print("Comecando")
                    # enviar msg t1 com ident
                    com1.sendData(tipo1(tamanho_pacotes))

                    time.sleep(5)
                    # Recebeu msg t2 com ident?
                    head, nRx = com1.getData(10)
                    tipo = int(head[0])
                    if tipo == 2:
                        validado = True
                        print("Validado")

                elif resposta == 'n':
                    print("Encerrando")
                    com1.disable()
                    exit()

            else:
                print("Comecando")
                comeca = True

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Enviando Dados
        cont = 1
        
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # TA COM PROBLEMA DE ZERAR OS TIMERS SEM PRECISAR ACHO
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        while cont <= numPack:
            # Envia pacote cont - msg t3
            com1.sendData(tipo3(pacotes[cont-1], tamanho_pacotes, cont))    

            # Set timer 1
            timer1 = time.time()
            # Set timer 2
            timer2 = time.time()

            head, nRx = com1.getData(10)
            tipo = int(head[0])
            ultimo_pacote = int(head[7])

            if tipo == 4:
                t4 = True
            else:
                t4 = False
            while not t4:
                # Recebeu msg t4?

                print("Erro no pacote")
                if timer1 > 5:
                    # Envia pacote cont - msg t3
                    # Reset timer1
                    timer1 = time.time()
                if timer2 > 20:
                    # Envia msg t5
                    print("ENCERRANDO")
                    print(":-(")
                    com1.disable()
                    exit()
                else:
                    # Recebeu msg t6?
                    head, nRx = com1.getData(10)
                    tipo = int(head[0])
                    posicao = int(head[6])

                    if tipo == 6:
                        t6 = True
                        # Corrige cont
                        cont = posicao
                        # Envia pacote cont - msg t3
                        # Reset timer1 e timer2
                        timer1 = time.time()
                        timer2 = time.time()
                        # VOLTAR PRA RECEBEU MSG T4
                    else:
                        t6 = False

            if t4:
                cont += 1
                print("Pacote enviado com sucesso")




        print("SUCESSO")































        # head = [
        #     'tipo', # 0 
        #     "1 ou qualquer", # 1
        #     "livre", # 2
        #     "qnt pacotes", # 3
        #     "num pacote atual", # 4
        #     "se for handshake -> id, se for dados -> tam", # 5
        #     "pacote do erro", # 6
        #     "ultimo pacote recebido com sucesso", # 7
        #     "em  branco", # 8
        #     "em  branco", # 9
        #     ]
        
        # Payload -> 0-114 bytes 

        # eop -> 4 bytes 0xAA 0xBB 0xCC 0xDD    

        # head = b'\x00\x00\x00\x00' + b'\x00\x00\xBB\x00' + b'\xBB\x00\x00\x00'
        
        # eop = b'\xAA\xBB\xCC\xDD'

        # handshake = head + eop

        # Byte de inicio
        # time.sleep(0.2)
        # com1.sendData(handshake)
        # time.sleep(2)

        # # Recebendo o Byte de inicio
        # print("esperando 1 byte de resposta")
        # tamanho, nRx = com1.getData(1)

        # com1.rx.clearBuffer()
        # time.sleep(.1)



        # teste = "inicial.jpeg"
        # # txBuffer = open(teste, 'rb').read()
        # # pacotes = None # O QUE EH ISSO??
        # # tamPacotes = len(txBuffer)
        # # tamPacotesBytes = (tamPacotes).to_bytes(1, byteorder='big')
        # # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # txBuffer = open(teste, 'rb').read()

        # tamPacotes = len(txBuffer)
        # tamPacotesBytes = tamPacotes.to_bytes(4, byteorder='big')  # Use 4 bytes para representar o tamanho total

        # # Tamanho de cada pacote (50 bytes)
        # tam_pacote = 50

        # pacotes = []
        # # Dividir os bytes da imagem em pacotes de 50 bytes
        # for i in range(0, len(txBuffer), tam_pacote):
        #     pacote = txBuffer[i:i + tam_pacote]
        #     pacotes.append(pacote)
        
        # print('\n\n')
        # print(pacotes)
        # print('\n\n')


        # hs = 0
        # envio = 1
        # ESTADO = hs
        
        # timeout = time.time() + 5
        # if len(tamanho) == 0 or time.time()>timeout:
        #     quest = input(str("Servidor inativo. Tentar novamente? s/n : "))
        
        # tamanho_pacotes = len(pacotes)
        # tamanho_pacotes_bytes = tamanho_pacotes.to_bytes(1, byteorder='big')  # Use 4 bytes para representar o tamanho
        # #print(tamPacotesBytes)



        # print('\n\n\n')
        # ki = 0
        # for pacote in range(len(pacotes)-1):
        #     #envio = tamPacotesBytes + b'\x00\x00\xBB\x00' + b'\xBB\x00\x00\x00' + pacotes[pacote] + eop
        #     envio = pacotes[pacote] 
        #     print(envio)
        #     com1.sendData(envio)
        #     time.sleep(3)
        #     ki +=1
        #     print(ki)
        
        # time.sleep(3)
        # envio = tamPacotesBytes + b'\xAA\xAA\xAA\xAA' + b'\xBB\x00\x00\x00' + pacotes[-1] + eop
        # print('\n\n\n\n\n')
        # print(envio)
        # print(ki+1)
        # time.sleep(3)
        # com1.sendData(envio)
        # time.sleep(2)

        # time.sleep(3)
        # com1.sendData(final)
        # time.sleep(2)
        
        # # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # # Recebendo confirmacao do server
        # print("esperando confirmacao")
        # confirmacao, nRx = com1.getData(1)
        # com1.rx.clearBuffer()
        # time.sleep(.1)
        # print("confirmacao recebida")
        # if confirmacao == b'\x0c':
        #     print("TUDO CERTO")
        #     # Encerra comunicação
        #     time.sleep(1)
        #     print("-------------------------")
        #     print("Comunicação encerrada")
        #     print("-------------------------")
        #     com1.disable()

        # else:
        #     print("ERRO")
        #     print("TENTAR NOVAMENTE")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()