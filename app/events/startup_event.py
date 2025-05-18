from app import core
from app import services
from app import config
from app import logs
from app import utils


async def create_tables() -> None:
    async with config.sessionmanager.connect() as conn:
        await conn.run_sync(config.Base.metadata.create_all)
        logs.logger.info("Tabelas criadas no banco de dados (se necessário)")


async def get_token_api() -> utils.Result:
    return await services.api_service_arduino.get_token()


def scheduler_start() -> None:
    core.scheduler.add_job(core.send_data_job, "interval", seconds=15)
    core.scheduler.start()
    logs.logger.info("Scheduler iniciado com job a cada 15 segundos")


async def startup_event() -> None:
    logs.logger.info("Iniciando eventos de startup")

    await create_tables()

    result = await get_token_api()
    if result.is_failure:
        logs.logger.error(
            f"Erro ao obter token na inicialização: {result.failure()}")
        return

    logs.logger.info("Conexão com API realizada e token bearer adquirido")
    scheduler_start()
