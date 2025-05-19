from app import models
from app import utils
from app import config
from app import modules
from .email_send_gmail import EmailSendGmail
from .tls_transport import TLSTransport
from sqlalchemy.ext.asyncio import AsyncSession


class ClimateRecordService:
    # lembrar de colocar o email_service_gmail como dependência externa
    def __init__(self, database: AsyncSession, email_sender: modules.EmailConfiguration):
        self.__database: AsyncSession = database
        self.__email_sender: modules.EmailConfiguration = email_sender
        self.__should_store_temperature: bool = True

    def __calculate_temperature_sensation(self, temperature: float, humidity: float) -> float:
        """
        Calcula a sensação térmica (heat index) baseada na temperatura (°C) e umidade relativa (%).
        Fórmula adaptada de Rothfusz/NWS.
        obs:
            Essa fórmula é confiável entre 27°C a 50°C e umidade acima de 40%. Fora desses limites, pode dar valores incorretos.
            Para temperaturas muito baixas, o ideal seria calcular sensação térmica por vento (Wind Chill).
        """
        t: float = temperature
        rh: float = humidity

        hi: float = (
            -8.784695 +
            1.61139411 * t +
            2.338549 * rh +
            -0.14611605 * t * rh +
            -0.012308094 * t**2 +
            -0.016424828 * rh**2 +
            0.002211732 * t**2 * rh +
            0.00072546 * t * rh**2 +
            -0.000003582 * t**2 * rh**2
        )

        return round(hi, 2)

    def __should_register(self, temperature: float, humidity: float) -> bool:
        if temperature is None or humidity is None:
            raise ValueError("Dados de temperatura ou umidade ausentes.")

        temperature_verify: float = 30.0
        if temperature > temperature_verify and self.__should_store_temperature:
            self.__should_store_temperature = False
            return True

        if temperature < temperature_verify - 1:
            self.__should_store_temperature = True

        return False

    async def register_record(self, data: dict) -> utils.Result:
        temperature, humidity = data.get("temperature"), data.get("humidity")

        try:
            if not self.__should_register(temperature, humidity):
                return utils.Success("Registro não necessário")

            thermal_sensation: float = self.__calculate_temperature_sensation(
                temperature, humidity)
            record = models.TemperatureIncident(
                temperature=temperature, humidity=humidity, thermal_sensation=thermal_sensation)

            self.__database.add(record)
            await self.__database.commit()
            await self.__database.refresh(record)

            await self.__email_sender.send_email(
                "oversouls11@gmail.com", "email_test", record.to_dict())

            return utils.Success(record)
        except Exception as e:
            return utils.Failure(e)

    async def get_records(self, page: int, quantity_records: int) -> utils.Result:
        try:
            return utils.Success(await utils.paginationData(self.__database, models.TemperatureIncident, page, quantity_records))
        except Exception as e:
            return utils.Failure(e)

    def get_should_store_temperature(self) -> bool:
        return self.__should_store_temperature

    def __str__(self) -> str:
        return f"database: {self.__database} should_store_temperature: {self.__should_store_temperature}"


transport: TLSTransport = TLSTransport(
    config.email_settings.hostname,
    config.email_settings.port,
)

email_sender: EmailSendGmail = EmailSendGmail(
    config.email_settings.email,
    config.email_settings.password,
    config.email_settings.subject,
    transport
)

climate_record_service: ClimateRecordService = ClimateRecordService(
    config.sessionmanager.sessionmaker(),
    email_sender,
)
