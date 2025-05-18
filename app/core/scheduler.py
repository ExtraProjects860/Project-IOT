from app import core
from app import services
from app import logs
from app import utils
from app import schemas
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def websocket_send_clients(data: dict) -> None:
    logs.logger.info("Enviando dados para clientes conectados")
    disconnected = set()

    for ws in list(core.connected_clients):
        try:
            await ws.send_json(data)
        except:
            disconnected.add(ws)

    core.connected_clients -= disconnected


async def verify_register_record(data: dict) -> utils.Result:
    temperature, humidity = data.get("temperature"), data.get("humidity")

    logs.logger.info("Validando temperatura e umidade para armazenar...")  
    return await services.climate_record_service.register_record({
        "temperature": temperature,
        "humidity": humidity
    })


def parsed_for_dataclasses(raw_list: list) -> dict:
    parsed_data = [schemas.ArduinoDataResponseSchema(**item) for item in raw_list]
    return schemas.extract_temperature_and_humidity(parsed_data)


async def send_data_job() -> None:
    logs.logger.info("Coletando dados da Arduino API...")
    result: utils.Result = await services.api_service_arduino.iot_properties()
    if result.is_failure:
        logs.logger.warning(f"Erro ao armazenar dados: {result.failure()}")
        return

    raw_list: list = result.unwrap()
    
    await websocket_send_clients(raw_list)

    result = await verify_register_record(parsed_for_dataclasses(raw_list))
    if result.is_failure:
        logs.logger.warning(f"Erro ao armazenar dados: {result.failure()}")
        return
    
