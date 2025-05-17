from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, List
from app import utils


@dataclass
class ApiResponseSchema:
    status_code: int
    data: dict | None
    ok: bool


@dataclass
class ArduinoDataResponseSchema:
    id: str
    variable_name: str
    last_value: Any
    value_updated_at: datetime


def transform_dataclass_arduino(data: dict) -> List:
    properties_dto: List[ArduinoDataResponseSchema] = [
        ArduinoDataResponseSchema(
            id=item.get("id"),
            variable_name=item.get("variable_name"),
            last_value=item.get("last_value"),
            value_updated_at=datetime.fromisoformat(
                item.get("value_updated_at").replace("Z", "+00:00"))
        )
        for item in data
    ]

    # Transforma para dict para enviar ao front (ex: websocket ou json)
    raw_data = [asdict(prop) for prop in properties_dto]
    return utils.serialize_datetimes(raw_data)
