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


data_service_istance = ItemDataService(FILE_PATH, columns)
app = FastAPI()


#Router to count all items
count_router = CreateRouteCounter(data_service_istance)
app.include_router(count_router)

#Router to get all items
getItem = CreateRouteGetitem(data_service_istance)
app.include_router(getItem)

#Router to post one item
postItem = CreateRoutePost(data_service_istance)
app.include_router(postItem)

#Router to get one item
getOneItem = CreateRouteGetOneitem(data_service_istance)
app.include_router(getOneItem)

#Router to delete one item
deleteOneItem = DeleteRouteItem(data_service_istance)
app.include_router(deleteOneItem)

#Router to update one item
updateOneItem = UpdateRoutePost(data_service_istance)
app.include_router(updateOneItem)

