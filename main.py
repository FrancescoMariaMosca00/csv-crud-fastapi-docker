from fastapi import FastAPI
import os

from Services.data_service import ItemDataService

from Routes.CountRoute import  CreateRouteCounter
from Routes.GetItemRoute import CreateRouteGetitem
from Routes.PostRoute import CreateRoutePost
from Routes.GetOneitemRoute import CreateRouteGetOneitem
from Routes.DeleteRoute import DeleteRouteItem
from Routes.PutRoute import UpdateRoutePost

DATA_DIR = "Data"
FILE_PATH = os.path.join(DATA_DIR, "items.csv")

columns = ['ID', 'Nome', 'Cognome', 'Codice Fiscale']
#key_column = 'ID'
#unique_column = 'Codice Fiscale'

data_service_istance = ItemDataService(FILE_PATH, columns)
#df = data_service_istance.load_data()

app = FastAPI()
#ENDPOINTS

#Endpoint to count istances of the df
count_router = CreateRouteCounter(data_service_istance)  # Passa il df
app.include_router(count_router)

#Endpoint to get all the istances
getItem = CreateRouteGetitem(data_service_istance)
app.include_router(getItem)

postItem = CreateRoutePost(data_service_istance)
app.include_router(postItem)

getOneItem = CreateRouteGetOneitem(data_service_istance)
app.include_router(getOneItem)

deleteOneItem = DeleteRouteItem(data_service_istance)
app.include_router(deleteOneItem)

updateOneItem = UpdateRoutePost(data_service_istance)
app.include_router(updateOneItem)
#Endpoint per ottenere tutti i record

