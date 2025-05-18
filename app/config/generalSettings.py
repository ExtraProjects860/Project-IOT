from dataclasses import dataclass
from dotenv import dotenv_values

CONFIG_ENV = dotenv_values()


@dataclass
class Settings:
    project_name: str = "Project-IOT"
    database_url: str = CONFIG_ENV.get("DB_URL")
    echo_sql: bool = True
    debug_logs: bool = True
    email_env: str = CONFIG_ENV.get("EMAIL_ENV")
    client_id_arduino: str = CONFIG_ENV.get("CLIENT_ID_ARDUINO")
    client_secret_arduino: str = CONFIG_ENV.get("CLIENT_SECRET_ARDUINO")
    thing_id_arduino: str = CONFIG_ENV.get("THING_ID_ARDUINO")


settings: Settings = Settings()
