from fastapi import APIRouter, HTTPException
from Model.Items import Item
from Services.data_service import ItemDataService
from Services.Exceptions import ValidationError, InvalidCodeFiscaleError, DuplicateIDError

def CreateRoutePost(service_istance: ItemDataService):
    router = APIRouter()

    @router.post("/items/")
    def post_new_item(item: Item):
        try:
            result = service_istance.add_item(item)
            return {"message": "Record aggiunto con successo", "record": result}
        except DuplicateIDError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except InvalidCodeFiscaleError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ValidationError as e:  # Catch-all per altre validazioni
            raise HTTPException(status_code=400, detail=str(e))
    return router

