from enlace import *
import time
import numpy as np
from PIL import Image
import io

# serialName = "COM3"
# serialName = "COM7"
# serialName = "COM6"
serialName = "COM9"


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
        tamanho, nRx = com1.getData(1)

        com1.rx.clearBuffer()
        time.sleep(.1)
        numPckg = None

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # MAIN

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # TA COM PROBLEMA DE ZERAR OS TIMERS SEM PRECISAR ACHO
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        ocioso = True
        if ocioso:
            t1 = True
            if t1:
                # Eh pra mim?
                endereco = True
                if endereco:
                    ocioso = False
            time.sleep(1)
        else:
            # Envia msg t2
            print("Enviando msg t2")
            cont = 1
            while cont <= numPckg:
                # Set timer 1
                timer1 = None
                # Set timer 2
                timer2 = None
                # Recebeu msg t3?
                t3 = True

                while not t3:
                    time.sleep(1)
                    if timer2 > 20:
                        ocioso = True
                        # Envia msg t5
                        print("Enviando msg t5")
                        print("ENCERRANDO")
                        print(":-(")
                        com1.disable()
                        exit()
                        break

                    else:
                        if timer1 > 2:
                            print("Enviando msg t4")
                            # Envia msg t4
                            # Reset timer1
                            timer1 = None
                            # VOLTA PRA RECEBEU T3
                            break
                if t3:
                    # O payload ta certo e em um pacote esperado correto?
                    pckg = True
                    if pckg:
                        print("Enviando msg t4")
                        # Envia msg t4
                        cont += 1
                    else:
                        print("Enviando msg t6")
                        # Envia msg t6



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