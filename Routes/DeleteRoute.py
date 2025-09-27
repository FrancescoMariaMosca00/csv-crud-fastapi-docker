#Endpoint per eliminare un record esistente:
from fastapi import APIRouter, HTTPException
from Services.data_service import ItemDataService

def DeleteRouteItem(service_istance: ItemDataService):
    router = APIRouter()

    @router.delete("/items/{item_id}")
    def delete_one_item(item_id: int):
        result = service_istance.deleteOneItem(item_id)

        if result is not None:
            return {"message": "Record eliminato con successo", "record": result}
        else:
            raise HTTPException(status_code=404, detail="ID utente non valido")
    
    return router