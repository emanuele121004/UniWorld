import asyncio
import socket
import sys
import json

from common.full_write import full_write
from common.bcolors import bcolors

MAXLINE = 4096

async def read_socket(sock):
    received_data = ""
    while True:
        # Legge i dati dal socket in modo asincrono
        recvbuff = await asyncio.to_thread(sock.recv, MAXLINE)
        
        if not recvbuff:
            print("[CLIENT] Nessun dato ricevuto (EOF)")
            break
            
        if not recvbuff.strip():
            print("[CLIENT] Dati vuoti. Chiusura connessione.")
            break
            
        received_data += recvbuff.decode()
        
    return received_data


async def client_echo(data, sock):
    # Scrive i dati usando la funzione full_write
    await asyncio.to_thread(full_write, sock, data.encode())
    
    # Aspetta che il socket abbia finito di inviare 
    await asyncio.to_thread(sock.shutdown, socket.SHUT_WR)
    
    # Legge la risposta
    return await read_socket(sock)


def launchMethod(input_str: str, server_address: str, server_port: int):
    """
    Funzione principale per lanciare una richiesta al server
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_add = (server_address, server_port)

    try:
        sock.connect(serv_add)
        print(f"[CLIENT] Connesso con successo a {serv_add}")
    except Exception as e:
        print(f"{bcolors.FAIL}[CLIENT] Errore di connessione: {e}{bcolors.ENDC}")
        # In caso di errore critico, usciamo o gestiamo l'eccezione
        return None

    try:
        # Esegue la comunicazione asincrona
        result = asyncio.run(client_echo(input_str, sock))
    except Exception as e:
         print(f"{bcolors.FAIL}[CLIENT] Errore durante lo scambio dati: {e}{bcolors.ENDC}")
         result = None
    finally:
        # Chiude il socket alla fine dello stream
        sock.close()

    return result
