from fastapi import APIRouter
from Services.data_service import ItemDataService

def CreateRouteGetitem(service_istance: ItemDataService):
    router = APIRouter()
    
    @router.get("/items/")
    def get_tutti_items():
        return service_istance.load_data().to_dict('records') 
    
    return router