from fastapi import APIRouter, WebSocket
from app.core.state import connected_clients

router = APIRouter()

# pegar e passar o controller


@router.websocket("/ws/climate-records")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        pass
    finally:
        connected_clients.remove(websocket)
