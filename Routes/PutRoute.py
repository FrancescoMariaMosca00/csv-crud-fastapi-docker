from fastapi import APIRouter, HTTPException
from Model.Items import Item
from Services.data_service import ItemDataService
from Services.Exceptions import ValidationError, InvalidCodeFiscaleError, DuplicateIDError

def UpdateRoutePost(service_istance: ItemDataService):
    router = APIRouter()

    @router.put("/items/{item_id}")
    def put_new_item(item: Item, item_id: int):
        check = service_istance.getOneItem(item_id)
        if check is not None:
            try:
                result = service_istance.updateOneItem(item_id, item)
                print(result)
                return {"message": "Record aggiornato con successo", "record": result}
            except DuplicateIDError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except InvalidCodeFiscaleError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(status_code=404, detail="L'item non è presente nel csv")
    
    return router
