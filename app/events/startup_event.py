from app import config
from app import logs
from app import core
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class AppStartupCoordinator:
    def __init__(self, session_manager: config.DatabaseSessionManager, scheduler: AsyncIOScheduler, climate_job: core.ClimateDataMediator):
        self.__session_manager: config.DatabaseSessionManager = session_manager
        self.__scheduler: AsyncIOScheduler = scheduler
        self.__climate_job: core.ClimateDataMediator = climate_job

    async def __create_tables(self) -> None:
        async with self.__session_manager.connect() as conn:
            await conn.run_sync(config.Base.metadata.create_all)
            logs.logger.info(
                "Tabelas criadas no banco de dados (se necessário)")

    def __start_scheduler(self) -> None:
        self.__scheduler.add_job(
            self.__climate_job.handle_send_data_job, "interval", seconds=15)
        self.__scheduler.start()
        logs.logger.info("Scheduler iniciado com job a cada 15 segundos")

    async def run_startup(self) -> None:
        logs.logger.info("Iniciando eventos de startup")
        await self.__create_tables()

        logs.logger.info("Conexão com API realizada e token bearer adquirido")
        self.__start_scheduler()
        
    def get_scheduler(self) -> AsyncIOScheduler:
        return self.__scheduler


startup_coordinator: AppStartupCoordinator = AppStartupCoordinator(
    config.sessionmanager,
    AsyncIOScheduler(),
    core.climate_mediator
)
