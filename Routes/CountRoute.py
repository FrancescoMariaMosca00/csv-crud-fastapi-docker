from fastapi import APIRouter
from Services.data_service import ItemDataService


def CreateRouteCounter(service_istance: ItemDataService):
    router = APIRouter()
    
    @router.get("/items/count")
    def count_items_endpoint():
        count = len(service_istance.load_data())
        return {"count": int(count)}
    
    return router