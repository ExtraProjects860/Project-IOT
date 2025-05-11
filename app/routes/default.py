from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response
from app.services.example_service import do_something

router = APIRouter(
    tags=["default"]
)

@router.get("/")
async def default_route():
    return JSONResponse(content={ "message": "Hello World!" }, status_code=status.HTTP_200_OK)

@router.get("/test")
async def test_route():
    result = do_something()
    if result.is_success:
        return Response(content=result.unwrap(), status_code=status.HTTP_200_OK)
    else:
        return Response(content=f"Erro: {str(result.failure())}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)