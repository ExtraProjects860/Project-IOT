from sqlalchemy import Column, Float
from app import models


class TemperatureIncident(models.BaseModel):
    __tablename__ = "temperature_incident"

    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    thermal_sensation = Column(Float, nullable=False)
