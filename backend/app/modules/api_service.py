import httpx
from app import schemas
from abc import ABC


class ApiService(ABC):
    def __init__(self, base_url: str):
        self.__base_url: str = base_url

    def __return_response_default(self, response: httpx.Response) -> schemas.ApiResponseSchema:
        return schemas.ApiResponseSchema(
            status_code=response.status_code,
            data=response.json() if response.content else None,
            ok=response.is_success,
        )

    async def get(self, endpoint: str, headers: dict = None, params: dict = None) -> schemas.ApiResponseSchema:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(f"{self.__base_url}{endpoint}", headers=headers, params=params)
            return self.__return_response_default(response)

    async def post(self, endpoint: str, headers: dict = None, data: dict = None, json: dict = None):
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(f"{self.__base_url}{endpoint}", headers=headers, data=data, json=json)
            return self.__return_response_default(response)

    async def put(self, endpoint: str, headers: dict = None, data: dict = None, json: dict = None):
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.put(f"{self.__base_url}{endpoint}", headers=headers, data=data, json=json)
            return self.__return_response_default(response)

    async def delete(self, endpoint: str, headers: dict = None):
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.delete(f"{self.__base_url}{endpoint}", headers=headers)
            return self.__return_response_default(response)

    def get_base_url(self):
        return self.__base_url

    def set_base_url(self, base_url: str):
        self.__base_url = base_url

    def __str__(self):
        return f"base_url: {self.__base_url}"
