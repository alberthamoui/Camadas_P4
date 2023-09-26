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

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # TA COM PROBLEMA DE ZERAR OS TIMERS SEM PRECISAR ACHO
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        rodar = True
        while rodar:
            ocioso = True
            if ocioso:
                head, nRx = com1.getData(10)
                tipo = int(head[0])
                if tipo == 1:
                    tamanho = int(head[3])
                    numPckg = tamanho
                    t1 = True
                    ocioso = False
                    time.sleep(1)
                com1.rx.clearBuffer()
                time.sleep(.1)

            else:
                # Envia msg t2
                print("Enviando msg t2")
                com1.sendData(tipo2())
                cont = 1
                while cont <= numPckg:
                    # Set timer 1
                    timer1 = time.time()
                    # Set timer 2
                    timer2 = time.time()
                    # Recebeu msg t3?

                    head, nRx = com1.getData(10)
                    tipo = int(head[0])
                    tamanho = int(head[3])
                    countT3 = int(head[4])
                    com1.rx.clearBuffer()
                    time.sleep(.1)

                    if tipo == 3:
                        t3 = True
                        # O payload ta certo e em um pacote esperado correto?
                        if cont == countT3:
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
                        if timer2 > 20:
                            ocioso = True
                            # Envia msg t5
                            print("Enviando msg t5")
                            com1.sendData(tipo5())
                            print("ENCERRANDO")
                            print(":-(")
                            com1.disable()
                            exit()

                        else:
                            if timer1 > 2:
                                print("Enviando msg t4")
                                # Envia msg t4
                                # Reset timer1
                                timer1 = None
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