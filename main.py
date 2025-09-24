from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import pandas as pd
from pydantic import BaseModel
import os
#Cancello l'import di uuid perché risulta più complesso nella fase di Update and Delete.
#Utilizzo come chiave un semplice numero che cresce
#import uuid
import re

DATA_DIR = "Data"
FILE_PATH = os.path.join(DATA_DIR, "items.csv")

columns = ['ID', 'Nome', 'Cognome', 'Codice Fiscale']
key_column = 'ID'
unique_column = 'Codice Fiscale'

# Creazione/lettura file CSV
if os.path.exists(FILE_PATH):
    print("Il file items.csv esiste")
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=columns)
    df.to_csv(FILE_PATH, index=False)
    print("Creato file items.csv con colonne:", columns)
    


app = FastAPI()

# Modello di input per POST
class Item(BaseModel):
    ID: int
    Nome: str
    Cognome: str
    Codice_Fiscale: str


#ENDPOINTS

#Endpoint per ottenere tutti i record
@app.get("/items/")
def get_tutti_items():
    return df.to_dict('records') 

#Endpoint per la creazione di nuovi record
@app.post("/items/")
def post_new_item(item: Item):
    global df

    # Ricarico dataset aggiornato
    df = pd.read_csv(FILE_PATH)
    
    if item.ID in df["ID"].values:
        raise HTTPException(status_code=400, detail="L'ID esiste già")

    # Validazione: unicità Codice Fiscale
    if item.Codice_Fiscale in df[unique_column].values:
        raise HTTPException(status_code=400, detail="Codice Fiscale già esistente")
    
    if len(item.Codice_Fiscale) != 16:
        raise HTTPException(status_code=400, detail="Codice Fiscale non corrisponde al corretto numero di caratteri")
    
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Nome):
        raise HTTPException(
            status_code=400, 
            detail="Il Nome può contenere solo lettere e spazi"
        )
    
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Cognome):
        raise HTTPException(
            status_code=400, 
            detail="Il Nome può contenere solo lettere e spazi"
        )
    
    # Genero nuovo record
    new_row = {
        'ID': item.ID,  # ID univoco
        'Nome': item.Nome,
        'Cognome': item.Cognome,
        'Codice Fiscale': item.Codice_Fiscale
    }

    # Aggiungo a DataFrame
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Salvo su file
    df.to_csv(FILE_PATH, index=False)

    return {"message": "Record creato con successo", "record": new_row}

#Endpoint per ottenere un singolo record basato sull'ID
@app.get("/items/{item_id}")
#castato ad intero altrimenti lo vede come stringa
def get_one_item(item_id: int):
    global df   

    record = df.loc[df['ID'] == item_id]
    if not record.empty:
        return record.iloc[0].to_dict()
    else:
        raise HTTPException(status_code=404, detail="ID utente non valido")
    
#Endpoint per aggiornare un record esistente:
@app.put("/items/{item_id}", response_model=Item)
def update_one_item(item_id:int, item: Item):
    record = get_one_item(item_id)

    if not record.empty:
        if item.ID in df["ID"].values:
            raise HTTPException(status_code=400, detail="L'ID esiste già")

        # Validazione: unicità Codice Fiscale
        if item.Codice_Fiscale in df[unique_column].values:
            raise HTTPException(status_code=400, detail="Codice Fiscale già esistente")
        
        if len(item.Codice_Fiscale) != 16:
            raise HTTPException(status_code=400, detail="Codice Fiscale non corrisponde al corretto numero di caratteri")
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Nome):
            raise HTTPException(
                status_code=400, 
                detail="Il Nome può contenere solo lettere e spazi"
            )
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Cognome):
            raise HTTPException(
                status_code=400, 
                detail="Il Nome può contenere solo lettere e spazi"
            )
        
        # Genero nuovo record
        update_row = {
            'ID': item.ID,  # ID univoco
            'Nome': item.Nome,
            'Cognome': item.Cognome,
            'Codice Fiscale': item.Codice_Fiscale
        }

        # Aggiungo a DataFrame
        df = df.loc[df['ID']== item_id, ['Nome', 'Cognome', 'Codice Fiscale']] = [update_row['Nome'], update_row['Cognome'], update_row['Codice Fiscale']]

        # Salvo su file
        df.to_csv(FILE_PATH, index=False)

        return {"message": "Record creato con successo", "record": update_row}
            
        
    else:
        raise HTTPException(status_code=404, detail="ID utente non valido")


#Endpoint per eliminare un record esistente:
@app.delete("/items/{item_id}")
def delete_one_item(item_id: int):
    global df
    record = df.loc[df['ID'] == item_id]

    if not record.empty:
        df = df.drop(df[df['ID'] == item_id].index)
        df.to_csv(FILE_PATH, index=False)
        return {"message": "Record eliminato con successo", "record": record.iloc[0].to_dict()}
    else:
        raise HTTPException(status_code=404, detail="ID utente non valido")
    