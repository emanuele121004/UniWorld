import sys
import time
from PyQt5.QtWidgets import QApplication
from multiprocessing import Process

# Importiamo le interfacce grafiche (GUI)
from logic.students.login_logic import LoginLogic
from logic.students.students_home_logic import StudentsHomeLogic
from logic.segreteria.segreteria_home_logic import SegreteriaHomeLogic

# Importiamo il server
from combined_multiplex_concurrent_server import server_main

# --- CONFIGURAZIONE RETE ---
# Deve corrispondere a server_address.json
IP_SERVER = '127.0.0.1'
PORTA_SERVER = 9000 
# ---------------------------

def avvia_interfaccia_grafica():
    """
    Gestisce il flusso delle finestre PyQt5.
    """
    app = QApplication(sys.argv)

    # Inizializzazione Logiche
    interfaccia_login = LoginLogic()
    dashboard_studente = StudentsHomeLogic(interfaccia_login.user)
    dashboard_amministrazione = SegreteriaHomeLogic(interfaccia_login.user)

    # Collegamenti segnali (Switch tra finestre)
    interfaccia_login.show_students_home.connect(
        lambda: dashboard_studente.showWindow(interfaccia_login.user)
    )
    interfaccia_login.show_office_home.connect(
        lambda: dashboard_amministrazione.showWindow(interfaccia_login.user)
    )

    # Mostra Login
    interfaccia_login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print(f"--- Avvio Sistema UniWorld ---")
    
    # 1. Avvio il Server in un processo separato
    print(f"[SYSTEM] Avvio del Server su {IP_SERVER}:{PORTA_SERVER}...")
    processo_server = Process(target=server_main, args=(IP_SERVER, PORTA_SERVER))
    processo_server.start()
    
    # Aspettiamo un secondo che il server sia pronto
    time.sleep(1)

    try:
        # 2. Avvio il Client (Interfaccia Grafica)
        print("[SYSTEM] Avvio Interfaccia Grafica...")
        avvia_interfaccia_grafica()
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        # 3. Quando chiudo le finestre, spengo il server
        print("[SYSTEM] Chiusura applicazione e arresto server.")
        processo_server.kill()