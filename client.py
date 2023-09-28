from comands import *
from enlace import *
import time
import numpy as np
import random
import binascii
from crc import Calculator, Crc8, Configuration



# A SER FEITO

# EXTRA


serialName = "COM4"
# serialName = "COM7"
#serialName = "COM6"


comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        t4 = ''
        contador = 0
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")

        imagem = "inicial.jpeg"
        txBuffer = open(imagem, 'rb').read()
        numPack = len(txBuffer)

        # Tamanho de cada payload (114 bytes)
        tam_pacote = 114

        #pacote total 128 bytes

        # calculadora de crc 
        calculator = Calculator(Crc8.CCITT) 
        config = Configuration(
        width=8,
        polynomial=0x07,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False,)

        pacotes = []
        lista_crc = []
        # Dividir os bytes da imagem em pacotes de 50 bytes
        for i in range(0, len(txBuffer), tam_pacote):
            pacote = txBuffer[i:i + tam_pacote]
            pacotes.append(pacote)
            crc = calculator.checksum(pacote)
            crc = crc.to_bytes(2, byteorder='little')[0]+ crc.to_bytes(2, byteorder='little')[1]
            lista_crc.append(crc)
        
        print(len(pacotes[-1]))

        print(lista_crc)
        
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
                # resposta = input(str("Deseja continuar? [s/n]: "))
                resposta = 's'
                if resposta == 's':
                    print("Comecando")
                    # enviar msg t1 com ident
                    com1.sendData(tipo1(tamanho_pacotes))
                    print(tipo1(tamanho_pacotes))
                    print('enviou t1')
                    time.sleep(5)
                    # Recebeu msg t2 com ident?
                    head, nRx = com1.getData(10)
                    tipo = int(head[0])
                    com1.rx.clearBuffer()
                    print('recebeu t2')
                    print(head)
                    print('\n')
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

        # Enviando Dados
        cont = 1
        
        while cont <= numPack:
            # Envia pacote cont - msg t3
            try:
                print('tentou')
                com1.sendData(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1]))
                print(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1]))
                print('------------------------------------------------------------------------------------')
            except:
                print('fudeu')
                print(com1.sendData(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1])))
                print(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1]))
                print('brecouuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
                break

            
            print('enviou tipo 3')
            print(tipo3(pacotes[cont-1], tamanho_pacotes, cont))
            print('\n')
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            #time.sleep(5)

            # Set timer 1
            timer1 = time.time()
            # Set timer 2
            timer2 = time.time()
            timer3 = 0

            #trava antes desse get
            rxlen = 0
            while rxlen == 0:
                rxlen = com1.rx.getBufferLen()
                time.sleep(.5)
                print("Esperando receber")
                print(rxlen)
                if time.time() - timer3 > 5:
                    print("brecou")
                    print(time.time()-timer3)
                    t4 =False
                    break
            

            head, nRx = com1.getData(10)
            print(f'head: {head}')
            tipo = int(head[0])
            print('tipo:  {}'.format(tipo))
            print('bbbbbbbbbbbbbbb')
            ultimo_pacote = int(head[7])
            com1.rx.clearBuffer()
            time.sleep(.1)

            if tipo == 4:
                print('recebeu tipo 4')
                t4 = True
            else:
                print('n recebeu tipo 4')
                t4 = False



            while not t4:
                # Recebeu msg t4?

                print("Erro no pacote")
                timeout1 = timer1 + 5
                timeout2 = timer2 + 20
                timer1 = time.time()
                if timer1 > timeout1:
                    com1.sendData(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1])) 
                    time.sleep(.1)
                    print('enviou tipo 3 de novo')
                    # Envia pacote cont - msg t3
                    # Reset timer1
                    timer1 = time.time()
                timer2= time.time()
                if timer2 > timeout2:
                    # Envia msg t5
                    com1.sendData(tipo5()) 
                    print("ENCERRANDO")
                    print(":-(")
                    com1.disable()
                    exit()
                else:
                    # Recebeu msg t6?
                    head, nRx = com1.getData(10)
                    tipo = int(head[0])
                    posicao = int(head[6])
                    com1.rx.clearBuffer()
                    time.sleep(.1)

                    if tipo == 6:
                        print('recebeu t6')
                        t6 = True
                        # Corrige cont
                        cont = posicao
                        # Envia pacote cont - msg t3
                        com1.sendData(tipo3(pacotes[cont-1], tamanho_pacotes, cont, lista_crc[cont-1]))
                        # Reset timer1 e timer2
                        timer1 = time.time()
                        timer2 = time.time()
                        # VOLTAR PRA RECEBEU MSG T4
                    else:
                        print('n recebeu t6')
                        t6 = False

            if t4:
                cont += 1
                print("Pacote 4 enviado com sucesso")



        print("SUCESSO")
        print(pacotes)


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
if __name__ == "__main__":
    main()