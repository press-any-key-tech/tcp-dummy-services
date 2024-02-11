from typing import List
from tcp_dummy_services.domain.entities import Thing
from tcp_dummy_services.core.logging import logger
from tcp_dummy_services.domain.exceptions import ThingNotFoundException
from tcp_dummy_services.infrastructure.repositories.dummy import things_repository


class ReadService:
    """Query operations"""

    async def get_list(self) -> List[Thing]:
        """
        Get a list of Things


        Returns:
            List[Thing]: domain entity to return
        """

        return await things_repository.get_list()

    async def get_by_id(self, id: str) -> Thing:
        """
        Search thing by id

        Args:

            id (str): id of the thing

        Returns:

            thing: domain entity to return
        """

        logger.debug("Entering. id: %s", id)

        try:
            entity: Thing = await things_repository.get_by_id(id=id)
            return entity
        except ThingNotFoundException:
            # Domain exception raise if thing doesn't exists
            raise ThingNotFoundException(f"Thing with id [{id}] not found")
