from typing import List
from tcp_dummy_services.domain.entities import Thing
from tcp_dummy_services.core.logging import logger
from tcp_dummy_services.domain.exceptions import ThingNotFoundException
from tcp_dummy_services.infrastructure.repositories.dummy import things_repository


class WriteService:
    """Command operations"""

    async def create(
        self,
        entity: Thing,
    ) -> Thing:
        """Create a Thing

        Args:
            request (Thing): _description_

        Returns:
            Thing: _description_
        """

        logger.debug("Entering. thing: %s", entity)

        result: Thing = await things_repository.create(entity=entity)

        return result

    async def delete_by_id(self, id: str):
        """Delete thing by id

        Args:
            id (str): _description_

        Raises:
            PotNotFoundException: _description_
        """

        logger.debug("Entering. id: %s", id)

        try:
            await things_repository.delete_by_id(id=id)
        except ThingNotFoundException:
            # Domain exception raise if thing doesn't exists
            raise ThingNotFoundException(f"Thing with id [{id}] not found")

    async def update(
        self,
        id: str,
        entity: Thing,
        # current_user: User
    ) -> Thing:
        """Updates the given thing

        Args:
            id (str): _description_
            entity (Thing): _description_

        Raises:
            PotNotFoundException: _description_

        Returns:
            Thing: _description_
        """

        logger.debug("Entering. id: %s entity: %s", id, entity)

        try:
            result: Thing = await things_repository.update(id=id, entity=entity)
            return result
        except ThingNotFoundException:
            # Domain exception raise if thing doesn't exists
            raise ThingNotFoundException(f"Thing with id [{id}] not found")
