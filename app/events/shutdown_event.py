from app import config
from app import logs
from .startup_event import startup_coordinator

# criar uma classe de coordinator aqui dps


async def shutdown_event():
    await config.sessionmanager.close()
    startup_coordinator.get_scheduler().shutdown()
    logs.logger.info("Conexões e tarefas agendadas finalizadas")
