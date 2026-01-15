import socket
import socketserver
import selectors
import json
import threading
import time

from common.bcolors import bcolors
from common.full_write import full_write
from common.communication import loadJSONFromFile
from server_side import method_switch

MAXLINE = 256

class MyHandler(socketserver.StreamRequestHandler):
    def handle(self):

        host, port = self.client_address
        print(f"[SERVER] Richiesta ricevuta da {host}:{port}")

        while True:
            try:
                data = self.rfile.readline(MAXLINE)
                if not data:
                    print(f"[SERVER] Connessione chiusa dal client {self.client_address}")
                    break

                print(f"[SERVER] Dati ricevuti da {self.client_address}: {data}")
                data_decoded = data.decode().replace('\n', '')
                data_decoded = json.loads(data_decoded)

                print(f"[SERVER] Dati elaborati: {data_decoded}")

                result = method_switch(data_decoded["header"], data_decoded["payload"])
                response = f"{json.dumps(result)}".encode("utf-8")
                print(f"[SERVER] Risposta da inviare: {response}")

                # Assicuriamoci che la risposta sia inviata del tutto prima di chiudere
                sent = full_write(self.request, response)
                print(f"[SERVER] Byte inviati: {sent}")

            except socket.error as e:
                if e.errno == 10054:
                    print(f"[SERVER] Connessione chiusa forzatamente dall'host remoto {self.client_address}")
                else:
                    print(f"{bcolors.FAIL} Errore Socket: {e}{bcolors.ENDC}")
                break
            except Exception as e:
                print(f"{bcolors.FAIL} Errore Generico: {e}{bcolors.ENDC}")
                break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def server_main(server_address, server_port):
    server = ThreadedTCPServer((server_address, server_port), MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print(f"[SERVER] In ascolto sulla porta {server_port}...")

    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("[SERVER] Server terminato dall'utente")


if __name__ == "__main__":
    server_coords = loadJSONFromFile("server_address.json")
    server_main(server_coords['address'], server_coords['port'])
