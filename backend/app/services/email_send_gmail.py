from app import modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSendGmail(modules.EmailConfiguration):
    def __init__(self, email: str, password: str, subject: str, transport: modules.EmailTransport):
        super().__init__(email, password, subject, transport)
        
    async def send_email(self, send_to: str, template_name: str, vars_to_override: dict, attachments: list = None) -> None:
        if attachments:
            await self.load_attachments()
        
        html = await self.load_html_template(template_name)
        html = self.variables_html_override(html, vars_to_override)
        
        message: MIMEMultipart = MIMEMultipart("alternative")
        message["From"] = self.get_email()
        message["To"] = send_to
        message["Subject"] = self.get_subject()
        message.attach(MIMEText(html, "html", "utf-8"))
        
        await self.get_transport().send(
            message, 
            username=self.get_email(),
            password=self.get_password()
        )
