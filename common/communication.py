import csv
import datetime
import json
import multiprocessing


def parse_communication_protocol(communication_string):
    # Trova le posizioni di inizio e fine dell'header (intestazione)
    header_start = communication_string.find("--Header:") + len("--Header:")
    header_end = communication_string.find("--EndH")

    # Estrai l'header (intestazione) 
    header = communication_string[header_start:header_end].strip()

    # Trova le posizioni di inizio e fine del payload
    payload_start = communication_string.find("--Payload:") + len("--Payload:")
    payload_end = communication_string.find("--EndP", payload_start)

    # Estrai il payload 
    payload = communication_string[payload_start:payload_end].strip()

    # Analizza l'intestazione e convertila in un array associativo
    header_array = {}
    header_segments = header.split(';')

    payload_array = {}
    payload_segments = payload.split(';')

    return {"Header": header_array, "Payload": payload}


def customHash(text: str):
    hash = 0
    for ch in text:
     hash = (hash * 33 ^ ord(ch) * 5381) & 0xFFFFFFFF
    return hash


def find_row(csv_file, search_criteria):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Considerando la prima riga come intestazione

        for row in reader:
            # Ipotizziamo che search_criteria sia un dizionario in cui le chiavi
            # sono i nomi delle colonne e i valori sono quelli da cercare
            if all(row[header.index(column)] == str(value) for column, value in search_criteria.items()):
                return row

    return None  # Restituisce None se la riga non viene trovata


def find_rows(csv_file, search_criteria=None):
    matching_rows = []

    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Considerando la prima riga come intestazione

        for row in reader:
            # Ipotizziamo che search_criteria sia un dizionario in cui le chiavi
            # sono i nomi delle colonne e i valori sono quelli da cercare

            if search_criteria is None:  # Voglio solo tutte le tuple
                matching_rows.append(row)
            else:
                if all(row[header.index(column)] == str(value) for column, value in search_criteria.items()):
                    matching_rows.append(row)

    return matching_rows


def find_rows_v2(csv_file, search_criteria_list=None):
    matching_rows = []

    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Considerando la prima riga come header

        for row in reader:
            # Se non vengono forniti criteri di ricerca, restituisce tutte le righe
            if search_criteria_list is None:
                matching_rows.append(row)
            else:
                # Controlla se la riga corrisponde ad almeno un criterio della lista
                row_matches = False
                for search_criteria in search_criteria_list:
                    # Verifica se tutti i criteri nel dizionario corrispondono
                    matches = all(row[header.index(column)] == str(value) for column, value in search_criteria.items())
                    if matches:
                        row_matches = True
                        break
                if row_matches:
                    matching_rows.append(row)

    return matching_rows


def insert_row(csv_file, data_row, custom_id=None):

    if custom_id is not None:
        new_id = custom_id
    else:
        # Determina l'ultimo ID nel file CSV e incrementalo Inizio Sezione Critica
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            last_row = None
            for row in reader:
                last_row = row
            if last_row is None or is_number(last_row[0]) == False:
                new_id = 1
            else:
                new_id = int(last_row[0]) + 1
    Lock = multiprocessing.Lock()
    # Aggiungi la nuova riga al file CSV
    Lock.acquire() # Sezione critica per le operazioni di scrittura su file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_id] + data_row)
    Lock.release()  # Fine Sezione Critica

    return new_id


def update_row(csv_file: str, row_id: str, column_name: str, new_value: str):
    # Leggi il file CSV e salva il suo contenuto in una lista di dizionari
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

    # Individua la riga corrispondente all'ID fornito
    for row in rows:
        if row['ID'] == row_id:
            # Modifica il valore della colonna indicata
            row[column_name] = new_value
            break
    else:
        print(f"Row with ID {row_id} not found.")
        return

    Lock = multiprocessing.Lock()
    # Salva i dati aggiornati sul file CSV
    Lock.acquire()  # Sezione critica per le operazioni di scrittura su file
    with open(csv_file, 'w', newline='') as file:
        fieldnames = csv_reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    Lock.release()

    print(f"Value in row {row_id}, column {column_name} updated to {new_value}.")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def request_constructor_obj(input_object, header):
    return {
        "header": header,
        "payload": input_object
    }


def request_constructor_str(input_object, header):
    return json.dumps(request_constructor_obj(input_object, header))


def formato_data():
    # Definisci i nomi dei giorni della settimana e dei mesi
    nomi_giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    nomi_mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre",
                 "Ottobre", "Novembre", "Dicembre"]

    # Ottieni la data e l'ora attuali
    oggi = datetime.datetime.now()

    # Ottieni il giorno della settimana, il giorno del mese e il mese attuali
    giorno_settimana = nomi_giorni[oggi.weekday()]
    giorno_mese = oggi.day
    mese = nomi_mesi[oggi.month - 1]
    anno = oggi.year

    # Costruisci la stringa con il formato richiesto
    data_formattata = f"{giorno_settimana} {giorno_mese} {mese} {anno}"
    return data_formattata


def get_current_date():
    current_date = datetime.datetime.now()
    return current_date.strftime("%d-%m-%Y")


def filter_dates_after_current(dates):
    current_date = datetime.datetime.now()
    matching_rows = []

    for row in dates:
        row_date = datetime.datetime.strptime(row[1], "%d-%m-%Y %H:%M:%S")
        if row_date > current_date:
            matching_rows.append(row)

    return matching_rows


def loadJSONFromFile(json_file):
    f = open(json_file)
    data = json.load(f)
    f.close()
    return data
