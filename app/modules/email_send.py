import aiofiles
from jinja2 import Template
from abc import ABC, abstractmethod
from .email_transport import EmailTransport
from app import config

class EmailConfiguration(ABC):
    def __init__(self, email: str, password: str, subject: str, transport: EmailTransport):
        self.__email: str = email
        self.__password: str = password
        self.__subject: str = subject
        self.__transport: EmailTransport = transport

    @abstractmethod
    async def send_email(self, send_to: str, template_name: str, vars_to_override: dict, attachments: list = None) -> None:
        pass
    
    def variables_html_override(self, html: str, vars_to_override: dict) -> str:
        template: Template = Template(html)
        return template.render(**vars_to_override)

    async def load_html_template(self, template_name: str) -> str:
        async with aiofiles.open(f"{config.TEMPLATES_PATH}/{template_name}.html", mode="r", encoding="utf-8") as file:
            return await file.read()
    
    async def load_attachments(self) -> None:
        # Se necessário implementar posteriormente
        pass
    
    def get_email(self) -> str:
        return self.__email
    
    def get_password(self) -> str:
        return self.__password
    
    def get_subject(self) -> str:
        return self.__subject
    
    def get_transport(self) -> EmailTransport:
        return self.__transport
    
    def __str__(self) -> str:
        return f"email: {self.__email}, password: {self.__password}, subject: {self.__subject}, transport: {self.__transport}"