from dataclasses import dataclass
from dotenv import dotenv_values

CONFIG_ENV = dotenv_values()


@dataclass
class EmailSettings:
    email: str = CONFIG_ENV.get("EMAIL_ENV")
    password: str = CONFIG_ENV.get("PASS_ENV")
    subject: str = CONFIG_ENV.get("SUBJECT_ENV")
    hostname: str = CONFIG_ENV.get("HOSTNAME_ENV")
    port: int = CONFIG_ENV.get("PORT_ENV")
    send_to: str = CONFIG_ENV.get("SEND_TO_ENV")
    template_name: str = CONFIG_ENV.get("TEMPLATE_NAME_ENV")


email_settings: EmailSettings = EmailSettings()
