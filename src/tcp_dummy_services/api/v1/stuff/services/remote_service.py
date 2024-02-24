from typing import List
from tcp_dummy_services.domain.entities import Thing
from tcp_dummy_services.core.logging import logger
from tcp_dummy_services.domain.exceptions import ThingNotFoundException
from tcp_dummy_services.infrastructure.repositories.dummy import things_repository
import aiohttp
from tcp_dummy_services.core import settings
import json


class RemoteService:
    """Query operations"""

    async def request(self, url: str, method: str, data: dict = None) -> dict:
        """
        Request to the remote service

        Args:
            url (str): url to request
            method (str): method to use
            data (dict): data to send

        Returns:
            dict: response from the remote service
        """

        logger.debug("Entering. url: %s, method: %s, data: %s", url, method, data)

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data) as response:
                result_str: str = await response.text()
                if response.status != 200:
                    raise Exception(f"Error: {response.status} - {result_str}")
                result = json.loads(result_str)
                logger.debug("Result:", result)
                return result

    async def get_list(self) -> List[Thing]:
        """
        Get a list of Things


        Returns:
            List[Thing]: domain entity to return
        """

        logger.debug("Entering")
        url: str = "/".join([settings.THINGS_BASE_URL.rstrip("/"), "things"])
        result: List[Thing] = await self.request(url=url, method="GET")
        return result

    async def get_by_id(self, id: str) -> Thing:
        """
        Search thing by id

        Args:

            id (str): id of the thing

        Returns:

            thing: domain entity to return
        """

        logger.debug("Entering. id: %s", id)

        url: str = "/".join([settings.THINGS_BASE_URL.rstrip("/"), "things", id])
        result: Thing = await self.request(url=url, method="GET")
        return result
