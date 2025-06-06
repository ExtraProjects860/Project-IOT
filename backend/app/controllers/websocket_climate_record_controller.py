from fastapi import APIRouter, WebSocket
from app import core

router = APIRouter()

class WebSocketClimateController:
    @staticmethod
    @router.websocket("/ws/climate-records")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        core.climate_mediator.get_connected_clients().add(websocket)

        try:
            while True:
                await websocket.receive_text()
        except:
            pass
        finally:
            core.climate_mediator.get_connected_clients().remove(websocket)
