from app import services
from app import utils
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Registros de Clima"]
)

class ClimateRecordController:
    @staticmethod
    @router.get("/climate-records")
    async def index(request: Request, page: int = Query(1, ge=1), quantity_records: int = Query(10, ge=1)):
        try:
            result: utils.Result = await services.climate_record_service.get_records(page, quantity_records)
            if result.is_success:
                return JSONResponse(status_code=200, content=result.unwrap())
            else:
                return JSONResponse(status_code=500, content={"error": str(result.error)})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})