from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app import routes
from app import config
from app import events


class App:
    def __init__(self):
        self.app: FastAPI = FastAPI()
        self.startup_events()
        self.routes()
        self.create_tables()

    def routes(self):
        self.app.include_router(routes.default_routes)
        self.app.include_router(routes.ws_route_climate_record)

    def middlewares(self):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def startup_events(self):
        self.app.add_event_handler("startup", events.startup_event)

    def create_tables(self):
        config.Base.metadata.create_all(bind=config.engine)


app_instance = App()
app = app_instance.app
