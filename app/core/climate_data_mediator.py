from app import services
from app import modules
from app import logs
from app import utils
from app import schemas


class ClimateDataMediator:
    def __init__(self, api_service: modules.ApiService, record_service: services.ClimateRecordService, connected_clients: set):
        self.__api_service: modules.ApiService = api_service
        self.__record_service: services.ClimateRecordService = record_service
        self.__connected_clients: set = connected_clients

    async def handle_send_data_job(self) -> None:
        logs.logger.info("Coletando dados da Arduino API...")
        result: utils.Result = await self.__api_service.get_token()

        if result.is_failure:
            logs.logger.error(f"Erro ao obter token na inicialização: {result.failure()}")
            return

        result = await self.__api_service.iot_properties()
        if result.is_failure:
            logs.logger.warning(f"Erro ao coletar dados: {result.failure()}")
            return

        raw_data_iot: list[dict] = result.unwrap()

        await self.__send_to_clients(raw_data_iot)

        result = await self.__save_to_db(raw_data_iot)
        if result.is_failure:
            logs.logger.warning(f"Erro ao armazenar dados: {result.failure()}")
            return

    async def __send_to_clients(self, data: list) -> None:
        logs.logger.info("Enviando dados para clientes conectados")
        disconnected = set()
        for ws in list(self.__connected_clients):
            try:
                await ws.send_json(data)
            except:
                disconnected.add(ws)
        self.__connected_clients -= disconnected

    async def __save_to_db(self, raw_list: list) -> utils.Result:
        parsed = schemas.extract_temperature_and_humidity([
            schemas.ArduinoDataResponseSchema(**item) for item in raw_list
        ])
        return await self.__record_service.register_record(parsed)
    
    def get_connected_clients(self) -> set:
        return self.__connected_clients
    
    def __str__(self) -> str:
        return f"api_service: {self.__api_service}, record_service: {self.__record_service}, connected_clients: {self.__connected_clients}"

climate_mediator: ClimateDataMediator = ClimateDataMediator(
    services.api_service_arduino,
    services.climate_record_service,
    set()
) 