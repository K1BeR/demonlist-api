from dataclasses import dataclass
from aiohttp import ClientSession, client_exceptions
from utils import handle_response
from urllib.parse import urljoin
import asyncio


@dataclass(frozen=True)
class Response:
    body: str
    headers: dict
    status: int


class Client:
    def __init__(self):
        self._base = "https://demonlist.org"
        self._session = ClientSession()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def __del__(self):
        asyncio.ensure_future(self.disconnect())

    async def request(self, method, path, *, data=None):
        """
        Sending a request to the server.
        :param method: request method
        :type method: str
        :param path: path to the page
        :type path: str
        :param data: outgoing data
        :type data: dict or None
        :return: None
        """
        if data is None:
            data = {}

        try:
            response = await self._session.request(
                method,
                urljoin(self._base, path),
                data=data,
                headers=self._headers
            )
        except client_exceptions.ClientConnectorError as e:
            raise ConnectionError("Could not connect to API.") from e
        else:
            await handle_response(response)
            try:
                return Response(await response.text(), dict(response.headers), int(response.status))
            except client_exceptions.ContentTypeError as e:
                raise RuntimeError(await response.text()) from e

    async def disconnect(self):
        """
        Closing a client session.
        """
        await self._session.close()
