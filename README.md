# UniWorld - Sistema di Gestione Esami Universitari

Applicazione Client-Server parallela per la gestione delle prenotazioni esami e della segreteria universitaria.

## Architettura
Il progetto implementa un'architettura **Client-Server** basata su socket TCP:
* **Server:** Gestisce la concorrenza tramite `ThreadedTCPServer` e l'accesso esclusivo ai dati (file CSV) utilizzando meccanismi di Lock per garantire la consistenza (Thread Safe).
* **Client:** Interfaccia grafica realizzata in **PyQt5**, comunica con il server tramite un protocollo personalizzato basato su JSON.

## Funzionalità
### Studente
* Login sicuro.
* Visualizzazione date esami disponibili.
* Prenotazione agli appelli.
* Visualizzazione storico prenotazioni (Accettate/Rifiutate/In attesa).

### Segreteria
* Login amministratore.
* Inserimento nuovi Corsi, Lauree e Appelli.
* Gestione richieste studenti (Accettazione/Rifiuto prenotazioni).
* Visualizzazione panoramica richieste.

## Installazione e Avvio

1. Assicurarsi di aver installato le dipendenze:
   ```bash
   pip install -r requirements.txt