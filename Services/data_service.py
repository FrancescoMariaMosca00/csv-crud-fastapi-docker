import os
import re
import pandas as pd
from Services.Exceptions import InvalidCodeFiscaleError, DuplicateIDError, InvalidNameError

class ItemDataService:
    def __init__(self, csv_path: str, columns: list):
        self.csv_path = csv_path
        self.columns = columns
        self.df = self.load_data()
        
    
    def load_data(self):
        # Creazione/lettura file CSV
        if os.path.exists(self.csv_path):
            print("Il file items.csv esiste")
            df = pd.read_csv(self.csv_path)
        else:
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.csv_path, index=False)
            print("Creato file items.csv con colonne:", self.columns)
        
        return df

    def save_data(self):
        return self.df.to_csv(self.csv_path, index=False)
    
    def delete_data(self, id:int):
        self.df = self.df.drop(self.df[self.df['ID'] == id].index)
        self.save_data()


    def update_data(self, item_id:int, item):
        if  self.validate_item_PUT(item, item_id):
            mask = self.df['ID'] == item.ID
            self.df.loc[mask, 'Nome'] = item.Nome
            self.df.loc[mask, 'Cognome'] = item.Cognome
            self.df.loc[mask, 'Codice Fiscale'] = item.Codice_Fiscale
            self.save_data()

            updaterow = {
                        'ID': item.ID,  
                        'Nome': item.Nome,
                        'Cognome': item.Cognome,
                        'Codice Fiscale': item.Codice_Fiscale
                    }
            return updaterow
        else:
            pass
            

            
    
    def validate_item_POST(self, item):
        if item.ID in self.df["ID"].values:
            raise DuplicateIDError("L'ID esiste già")
        # Validazione: unicità Codice Fiscale
        if item.Codice_Fiscale in self.df["Codice Fiscale"].values:
            raise InvalidCodeFiscaleError("Codice Fiscale già esistente")
        
        if len(item.Codice_Fiscale) != 16:
            raise InvalidCodeFiscaleError("Codice Fiscale non corrisponde al corretto numero di caratteri")
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Nome):
            raise InvalidNameError("Il Nome può contenere solo lettere e spazi")
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Cognome):
            raise InvalidNameError("Il Cognome può contenere solo lettere e spazi")

    
        return True
    
    def validate_item_PUT(self, item, id):
        if item.ID != id:
            raise DuplicateIDError("L'ID inserito è diverso rispetto a quello iniziale")
        
        if (item.Codice_Fiscale in self.df["Codice Fiscale"].values) and item.ID != id:
            raise InvalidCodeFiscaleError("Il nuovo codice Fiscale appartiene ad un altro utente")
                
        if len(item.Codice_Fiscale) != 16:
            raise InvalidCodeFiscaleError("Codice Fiscale non corrisponde al corretto numero di caratteri")
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Nome):
            raise NameError(detail="Il Nome può contenere solo lettere e spazi")
        
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", item.Cognome):
            raise NameError(detail="Il Cognome può contenere solo lettere e spazi")
        
        if item.Codice_Fiscale == self.df.loc[self.df["ID"] == id, "Codice Fiscale"].iloc[0]:
            pass
        elif (self.df[(self.df["Codice Fiscale"] == item.Codice_Fiscale) & (self.df["ID"] != id)].shape[0] > 0):
            raise InvalidCodeFiscaleError("Il nuovo codice fiscale appartiene già a un altro utente")
        
        return True



    def add_item(self, item):
        if self.validate_item_POST(item):
            new_row = {
                        'ID': item.ID,  
                        'Nome': item.Nome,
                        'Cognome': item.Cognome,
                        'Codice Fiscale': item.Codice_Fiscale
                    }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.save_data()
            return new_row
        
    def getOneItem(self, item_id: int):
        record = self.df.loc[self.df['ID'] == item_id]
        if not record.empty:
            return record.iloc[0].to_dict()
        else:
            pass

    def deleteOneItem(self, item_id:int):
        record = self.getOneItem(item_id)

        if record is not None:
            self.delete_data(item_id)
            return record
        else:
            pass

    def updateOneItem(self, item_id:int, item):
        result = self.update_data(item_id, item)

        if result is not None:
            return result
        else:
            pass




    