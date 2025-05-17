from app import core
from app import services
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def send_data_job() -> None:
    print("Coletando dados da Arduino API...")
    result = await services.api_service_arduino.iot_properties()
    if result.is_failure:
        print("Erro ao coletar dados:", result.failure())
        return

    data = result.unwrap()

    print("Enviando dados para clientes conectados")
    for ws in list(core.connected_clients):
        try:
            await ws.send_json(data)
        except:
            core.connected_clients.remove(ws)
