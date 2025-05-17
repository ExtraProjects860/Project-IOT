from app import core
from app import services


async def startup_event():
    result = await services.api_service_arduino.get_token()
    if result.is_failure:
        print("Erro ao obter token na inicialização:", result.failure())
        return

    print("Conexão com api realizada e token bearer adquirido")

    core.scheduler.add_job(core.send_data_job, "interval", seconds=15)
    core.scheduler.start()
