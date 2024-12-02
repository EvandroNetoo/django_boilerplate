import os
from abc import ABC, abstractmethod
from asyncio import gather
from dataclasses import asdict
from typing import Literal
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from .models import CustomerIn


class AsaasBase(ABC):
    _DEBUG = os.environ.get('DEBUG', '1') == '1'
    _API_KEY = os.environ.get('ASAAS_API_KEY', '')

    @classmethod
    def get_base_url(cls) -> str:
        """Retorna a URL base dependendo do valor de DEBUG."""
        return (
            'https://sandbox.asaas.com/api/v3/'
            if cls._DEBUG
            else 'https://api.asaas.com/v3/'
        )

    @property
    @abstractmethod
    def BASE_ENDPOINT(self) -> str:
        """Deve retornar o endpoint base específico da classe filha."""
        pass

    @classmethod
    async def _send_request(
        cls,
        *,
        method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET',
        extra_endpoint: str = '',
        json=None,
        headers: dict[str, str] = None,
        params: dict[str, str] = None,
    ) -> Response:
        url = cls._mount_url(extra_endpoint)

        if headers is None:
            headers = {}

        headers['access_token'] = cls._API_KEY
        headers['Content-Type'] = 'application/json'

        if params is None:
            params = {}

        async with AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                headers=headers,
                params=params,
            )

            return response

    @classmethod
    def _mount_url(cls, extra_endpoint: str = '') -> str:
        url = urljoin(cls.get_base_url(), cls.BASE_ENDPOINT)

        if extra_endpoint:
            url = urljoin(url, extra_endpoint)

        return url


class AsaasCostumer(AsaasBase):
    BASE_ENDPOINT = 'customers/'

    @classmethod
    async def create(cls, customer: CustomerIn) -> Response:
        return await cls._send_request(
            method='POST',
            json=asdict(customer),
        )

    @classmethod
    async def list(cls, params: dict[str, str] = None) -> Response:
        return await cls._send_request(
            method='GET',
            params=params,
        )

    @classmethod
    async def update(cls, customer_id: str, customer: CustomerIn) -> Response:
        return await cls._send_request(
            method='PUT',
            extra_endpoint=str(customer_id),
            json=asdict(customer),
        )

    @classmethod
    async def delete(cls, customer_id: str) -> Response:
        return await cls._send_request(
            method='DELETE',
            extra_endpoint=str(customer_id),
        )


class AsaasTasks:
    @classmethod
    async def delete_all_customers(cls) -> Response:
        MAX_LIMIT = 100
        
        has_more = True
        offset = 0
        page = 1

        while has_more:
            response = await AsaasCostumer.list(
                params={'offset': offset, 'limit': MAX_LIMIT}
            )
            if not response.is_success:
                raise Exception(
                    f'Error on request: Status code: {response.status_code} - Text: {response.text}'
                )

            data = response.json()
            customers = data['data']
            await gather(*[
                AsaasCostumer.delete(customer['id']) for customer in customers
            ])
            offset = page * MAX_LIMIT
            page += 1
            has_more = data['hasMore']


class AsaasApi:
    @classmethod
    def get_debug(cls) -> bool:
        return AsaasBase._DEBUG

    @classmethod
    def set_debug(cls, value: bool):
        AsaasBase._DEBUG = value

    @classmethod
    def get_api_key(cls) -> str:
        return AsaasBase._API_KEY

    @classmethod
    def set_api_key(cls, value: str):
        AsaasBase._API_KEY = value

    @classmethod
    def get_base_url(cls) -> str:
        return AsaasBase.get_base_url()

    customers = AsaasCostumer()
    tasks = AsaasTasks()


# response = asyncio.run(AsaasApi.customers.create(CustomerIn('Evandro', '015.314.820-90')))

# print(response.is_success)
# print(response.text)
# print(response.status_code)
