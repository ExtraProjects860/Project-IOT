from app import schemas
from app import config
from app import modules
import app.utils as utils
from datetime import datetime, timedelta, UTC
from typing import List


class ApiServiceArduino(modules.ApiService):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.__token: str | None = None
        self.__token_expiration: datetime | None = None

    async def __fetch_token(self) -> None:
        response: schemas.ApiResponseSchema = await self.post(
            endpoint=f"/v1/clients/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": config.CONFIG_ENV.get("CLIENT_ID_ARDUINO"),
                "client_secret": config.CONFIG_ENV.get("CLIENT_SECRET_ARDUINO"),
                "audience": self.get_base_url()
            }
        )
        if not response.data:
            raise ValueError(
                f"Erro ao obter token: resposta sem dados: {response}")

        self.__token = response.data.get("access_token")
        expires_in = response.data.get("expires_in")

        if not self.__token or not expires_in:
            raise ValueError(
                f"Token ou tempo de expiração ausente: {response.data}")

        self.__token_expiration = datetime.now(
            UTC) + timedelta(seconds=expires_in)

    async def __is_error_status_code(self, response: schemas.ApiResponseSchema, _retry: bool) -> schemas.ApiResponseSchema:
        if response.status_code == 401 and not _retry:
            self.__token = None
            await self.iot_properties(_retry=True)
            return
        if response.status_code != 200:
            raise Exception(
                f"Erro na requisição: {response.status_code} - {response.data}")

    async def iot_properties(self, _retry=False) -> utils.Result:
        try:
            response: schemas.ApiResponseSchema = await self.get(
                endpoint=f"/v2/things/{config.CONFIG_ENV.get("THING_ID_ARDUINO")}/properties",
                headers={"Authorization": f"Bearer {self.__token}"},
            )
            await self.__is_error_status_code(response, _retry)

            dto_from_front_end: List = schemas.transform_dataclass_arduino(
                response.data)

            return utils.Success(dto_from_front_end)
        except Exception as e:
            return utils.Failure(e)

    async def get_token(self) -> utils.Result:
        try:
            if self.__token is None or datetime.now(UTC) >= self.__token_expiration:
                await self.__fetch_token()
            return utils.Success(self.__token)
        except Exception as e:
            return utils.Failure(e)

    def get_token_expiration(self) -> datetime | None:
        return self.__token_expiration

    def __str__(self):
        return super().__str__() + f" token: {self.__token} token_expiration: {self.__token_expiration}"


api_service_arduino: ApiServiceArduino = ApiServiceArduino(
    "https://api2.arduino.cc/iot")
