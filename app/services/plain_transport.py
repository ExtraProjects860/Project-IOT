import aiosmtplib
from email.mime.multipart import MIMEMultipart
from app import modules

class PlainTransport(modules.EmailTransport):
    def __init__(self, hostname: str, port: int):
        super().__init__(hostname, port)

    async def send(self, message: MIMEMultipart, username: str, password: str) -> None:
        await aiosmtplib.send(
            message,
            hostname=self.get_hostname(),
            port=self.get_port(),
            username=username,
            password=password
        )
