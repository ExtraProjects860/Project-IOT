from app import core
from app import config
from app import logs


async def shutdown_event():
    await config.sessionmanager.close()
    core.scheduler.shutdown()
    logs.logger.info("Conexões e tarefas agendadas finalizadas")
