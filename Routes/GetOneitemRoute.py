from fastapi import APIRouter, HTTPException
from Services.data_service import ItemDataService

def CreateRouteGetOneitem(service_istance: ItemDataService):
    router = APIRouter()
    
    @router.get("/items/{item_id}")
    def get_one_item(item_id: int):   
        result = service_istance.getOneItem(item_id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail="L'item non è presente nel csv")
    
    
    return router