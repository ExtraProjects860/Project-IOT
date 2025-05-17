from datetime import datetime
from typing import Any, Union, List, Dict


def serialize_datetimes(data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
    def convert(obj: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in obj.items()
        }

    if isinstance(data, list):
        return [convert(item) for item in data]
    elif isinstance(data, dict):
        return convert(data)
    return data
