from fastapi import FastAPI
from app import models
from app import routes
from app.config.configureDB import Base, engine

class App:
    def __init__(self):
        self.app = FastAPI()
        self.routes()
        self.middlewares()
        self.create_tables()

    def routes(self):
        self.app.include_router(routes.default_routes)
    
    def middlewares(self):
        pass
    
    def create_tables(self):
        Base.metadata.create_all(bind=engine)
        
app_instance = App()
app = app_instance.app