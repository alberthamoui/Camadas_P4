from enlace import *
from comands import *
import time
import numpy as np
from PIL import Image
import io

# serialName = "COM3"
# serialName = "COM7"
# serialName = "COM6"
serialName = "COM6"


recebidos = []
comeco = b'\x0a'
final = b'\x0f'


def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        # Recebendo o Byte de inicio
        print("esperando 1 byte de inicio")


        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # MAIN

        rodar = True
        ocioso = True
        pckg = False
        while rodar:
            print("rodou")
            if ocioso:
                print("ocioso = true")
                head, nRx = com1.getData(10)
                try:
                    print(head)
                except:
                    print("nn recebeu head")


                print(list(head))
                print(f'head0: {head[0]}')
                tipo = int(head[0])
                print(f"tipo:{tipo}")


                if tipo == 1 or head[0] == b'x01':
                    print("tipo 1")
                    tamanho = int(head[3])
                    numPckg = tamanho
                    t1 = True
                    ocioso = False
                    print('ocioso = false')
                    time.sleep(1)
                com1.rx.clearBuffer()
                time.sleep(.1)
                print('volta pro while')

            else:
                # Envia msg t2
                print("Enviando msg t2")
                com1.sendData(tipo2())
                cont = 1
                print('cont = 1')






                while cont <= numPckg:
                    print("cont <= numPckg")
                    # Set timer 1
                    timer1 = time.time()
                    # Set timer 2
                    timer2 = time.time()
                    # Recebeu msg t3?

                    head, nRx = com1.getData(10)
                    print(f'head: {head}\n\n')
                    print(list(head)[11:15])
                    tipo = int(head[0])
                    tamanho = int(head[3])
                    countT3 = int(head)[4]
                    # countT3 = sum(list(head)[11:15])
                    print(f'tipo: {tipo}' + '\n' + f'tamanho: {tamanho}' + '\n' + f'countT3: {countT3}')
                    com1.rx.clearBuffer()
                    time.sleep(.1)

                    if tipo == 3:
                        print("tipo 3")
                        t3 = True
                        # O payload ta certo e em um pacote esperado correto?
                        if cont == countT3:
                            print("cont == countT3")
                            pckg = True
                        if pckg:
                            print("Enviando msg t4")
                            # Envia msg t4
                            com1.sendData(tipo4(cont))
                            cont += 1
                        else:
                            print("Enviando msg t6")
                            # Envia msg t6
                            com1.sendData(tipo6(countT3))
                    else:
                        t3 = False

                    while not t3:
                        time.sleep(1)
                        print("not t3")
                        print(f'timer2: {timer2}')
                        timeout2 = timer2 + 20 
                        if timer2 > timeout2:
                            ocioso = True
                            # Envia msg t5
                            print("Enviando msg t5")
                            com1.sendData(tipo5())
                            print("ENCERRANDO")
                            print(":-(")
                            com1.disable()
                            exit()

                        else:
                            print(f'timer1: {timer1}')
                            timeout1 = timer1 + 2
                            if timer1 > timeout1:
                                print("Enviando msg t4")
                                # Envia msg t4
                                com1.sendData(tipo4(cont))
                                # Reset timer1
                                timer1 = time.time()
                                # VOLTA PRA RECEBEU T3
                                break

                print("SUCESSO")




        
        
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    print(recebidos)
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()