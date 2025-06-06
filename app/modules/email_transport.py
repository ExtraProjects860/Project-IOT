from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart

class EmailTransport(ABC):
    def __init__(self, hostname: str, port: int):
        self.__hostname: str = hostname
        self.__port: int = port
    
    @abstractmethod
    async def send(self, message: MIMEMultipart, username: str, password: str) -> None:
        pass
    
    def get_hostname(self) -> str:
        return self.__hostname

    def get_port(self) -> int:
        return self.__port
    
    def __str__(self) -> str:
        return f"hostname: {self.__hostname}, port: {self.__port}"
