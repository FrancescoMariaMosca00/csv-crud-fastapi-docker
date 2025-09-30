# csv-crud-fastapi-docker

Progetto per Social Thingum.

Questa applicazione, sviluppata in Python con il framework FastAPI, espone un set di routes che consentono di eseguire operazioni CRUD (Create, Read, Update, Delete) su un db basato su file CSV.  

---

## Funzionalità principali
- Gestione di record utente composti da `ID`, `Nome`, `Cognome`, `Codice Fiscale`.
- Controllo di vincoli:
  - **unicità** dell’ID,
  - **unicità e correttezza** del Codice Fiscale (16 caratteri, non duplicato),
  - **formato valido** di Nome e Cognome (solo lettere e spazi).

## Struttura Progetto

L’applicazione è organizzata in più directory:

- **`Data/`**  
  Contiene il file `items.csv`, che funge da database persistente.  

- **`Model/`**  
  Qui si trova la definizione del modello **Item**.  
  Viene implementato con **Pydantic** e rappresenta lo schema dei dati accettati e restituiti dalle API.

- **`Routes/`**  
  Ogni file corrisponde a un router separato, che si occupa di:
  - Ricevere la chiamata HTTP,
  - Interagire con il service,
  - Gestire eventuali errori restituendo risposte coerenti.  
  Questa separazione aumenta la manutenibilità e rende più chiaro il flusso delle operazioni.

- **`Services/`**  
  È il cuore logico dell’applicazione.  
  Qui sono presenti:
  - La classe `ItemDataService`, che funge da ponte tra le route e il “database” (il file CSV). Si occupa del caricamento e salvataggio dei dati, oltre che di tutte le validazioni.
  - Le eccezioni personalizzate (`DuplicateIDError`, `InvalidCodeFiscaleError`, `InvalidNameError`), definite in un modulo dedicato per avere una gestione pulita e centralizzata degli errori.

- **`main.py`**  
  Punto di ingresso dell’applicazione.  
  Qui vengono istanziati i vari router e avviato il server FastAPI.  

## 🛠️ Validazioni e Gestione Errori

La logica di validazione dei dati è un aspetto centrale del progetto.  
Sono previsti diversi controlli:
- **ID univoco:** garantisce che non esistano duplicati.
- **Codice Fiscale:** deve essere lungo esattamente 16 caratteri ed essere univoco.
- **Nome e Cognome:** possono contenere solo lettere (inclusi caratteri accentati) e spazi.

Se uno di questi vincoli viene violato, viene sollevata un’eccezione dedicata.  
Questo approccio rende gli errori **espliciti e leggibili** sia lato codice che lato API, evitando risposte generiche.

---

## API Endpoints

L’applicazione espone un set standard di endpoint REST:

- **POST /items/** : Inserisce un nuovo record.  
- **GET /items/{id}** : Recupera un record esistente a partire dall’ID.
- **GET /items/** : Restituisce tutti gli items
- **PUT /items/{id}** : Aggiorna un record esistente.  
- **DELETE /items/{id}** : Elimina un record dal CSV.
- **GET /items/count** : Restituisce il count delle istanze nel file csv.


---

##Avvio dell’applicazione

Per eseguire l’applicazione è sufficiente:

1. Clonare la repository
   Installare le dipendenze principali (FastAPI, Uvicorn, Pandas).
   pip install --no-cache-dir -r requirements.txt
   Runnare il main ed avviare il server con il comando:  
   uvicorn main:app --reload
2. Oppure scaricare la docker image da qui: https://drive.google.com/file/d/15CGeTnX0rGW5NIRuRf8wCFFaG0NHaR1B/view?usp=drive_link
   In seguito runnare i seguenti comandi da powershell nella cartella in cui la dockerimage è stata scaricata
   docker load -i csv-crud-api-projectimage.tar

   e poi eseguire uno dei seguenti comandi:
   docker run -it --rm -p 8000:8000 csv-crud-api-test

   oppure, nel caso in cui si desiderino i changes sul csv permanenti:
   docker run -p 8000:8000 -v ${PWD}/data:/app/Data csv-crud-api-projectimage
   
4. Accedere agli endpoint:
   - Applicazione: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
   - Documentazione interattiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs#/)  


CURL PER POST:
C:\Users\PC\OneDrive\Documenti\GitHub\csv-crud-fastapi-docker>curl -X POST "http://localhost:8000/items/" -H "Content-Type: application/json" -d "{\"ID\":98, \"Nome\": \"Mario\", \"Cognome\": \"Rossi\", \"Codice_Fiscale\": \"RSSMRA01A01H501A\"}"
