from random import *
from comands import *
from enlace import *
import time
import numpy as np
import binascii

# h0 – Tipo de mensagem.
# h1 – Se tipo for 1: número do servidor. Qualquer outro tipo: livre
# h2 – Livre.
# h3 – Número total de pacotes do arquivo.
# h4 – Número do pacote sendo enviado.
# h5 – Se tipo for handshake: id do arquivo (crie um para cada arquivo). Se tipo for dados: tamanho do payload.
# h6 – Pacote solicitado para recomeço quando a erro no envio.
# h7 – Ùltimo pacote recebido com sucesso.
# h8 – h9 – CRC (Por ora deixe em branco. Fará parte do projeto 5).
# PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
# EOP – 4 bytes: 0xAA 0xBB 0xCC 0xDD
eop = b'\xAA' + b'\xBB' + b'\xCC' + b'\xDD'
def tipo1(tamanho,esperado):
    global eop
    head = b'\x01' + esperado.to_bytes(1, byteorder='big') + b'\xAA' + tamanho.to_bytes(1, byteorder='big') + b'\xAA' + b'\xAA' + b'\xAA' + b'\xAA' + b'\xAA' + b'\xAA'
    
    return head + b'' + eop

def tipo2():
    head = b'\x02' + b'\x01' + b'\x02' + b'\x03' + b'\x04' + b'\x05' + b'\x06' + b'\x07' + b'\x08' + b'\x09'
    global eop
    return head + b'' + eop

def tipo3(payload, tamanho, count, crc):
    head = b'\x03' + b'\x01' + b'\x02' + tamanho.to_bytes(1, byteorder='big') + count.to_bytes(1, byteorder='little') + b'\x05' + b'\x06' + b'\x07' + crc.to_bytes(1, byteorder='little') + b'\x09'
    print(f'tamanho: {tamanho.to_bytes(1, byteorder="big")}' + 
        '\n'
        + f'count: {count.to_bytes(1, byteorder="big")}')
    global eop
    return head + payload + eop

def tipo4(ultimo):
    head = b'\x04' + b'\x01' + b'\x02' + b'\x03' + b'\x04' + b'\x05' + b'\x06' + ultimo.to_bytes(1, byteorder='little') + b'x08' + b'x09'
    global eop
    return head + b'' + eop

def tipo5():
    head = b'\x05' + b'\x01' + b'\x02' + b'\x03' + b'\x04' + b'\x05' + b'\x06' + b'\x07' + b'\x08' + b'\x09'
    global eop
    return head + b'' + eop
    
def tipo6(posicaoErro):
    head = b'\x06' + b'\x01' + b'\x02' + b'\x03' + b'\x04' + b'\x05' + posicaoErro.to_bytes(1, byteorder='little') + b'\x07' + b'\x08' + b'\x09'
    global eop
    return head + b'' + eop