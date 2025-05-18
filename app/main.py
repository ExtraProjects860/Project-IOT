from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import controllers
from app import config
from app import events
from app import logs


class App:
    def __init__(self):
        logs.logger.info("Inicializando a aplicação FastAPI")
        self.__app: FastAPI = FastAPI(
            title=config.settings.project_name, docs_url="/docs")
        self.__middlewares()
        self.__startup_events()
        self.__routes()
        logs.logger.info("Aplicação FastAPI inicializada com sucesso")

    def __routes(self):
        self.__app.include_router(controllers.default_router)
        self.__app.include_router(controllers.climate_record_router)
        self.__app.include_router(controllers.ws_climate_record_router)
        logs.logger.debug("Rotas registradas")

    def __middlewares(self):
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logs.logger.debug("CORS Middleware aplicado")

    def __startup_events(self):
        self.__app.add_event_handler("startup", events.startup_event)
        self.__app.add_event_handler("shutdown", events.shutdown_event)
        logs.logger.debug("Evento de startup registrado")
    
    def get_app(self):
        return self.__app


app_instance = App()
app = app_instance.get_app()
