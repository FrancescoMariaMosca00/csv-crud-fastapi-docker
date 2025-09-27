from pydantic import BaseModel

class Item(BaseModel):
    ID: int
    Nome: str
    Cognome: str
    Codice_Fiscale: str