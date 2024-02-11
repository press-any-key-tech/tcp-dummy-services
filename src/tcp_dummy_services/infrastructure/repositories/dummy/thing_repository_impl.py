from typing import List, Optional, Dict
from automapper import mapper
from tcp_dummy_services.domain.entities import Thing

from tcp_dummy_services.domain.exceptions import ThingNotFoundException
from tcp_dummy_services.domain.exceptions import ThingAlreadyExistsException

from tcp_dummy_services.core.logging import logger
from ksuid import Ksuid


class ThingRepositoryImpl(PotRepository):
    """Repository implementation for Thing"""

    things: Dict[str, Thing]

    def __init__(self):

        self.things = []

    async def create(
        self,
        *,
        # current_user: User,
        entity: Thing,
    ) -> Thing:
        """
        Create a thing in memory

        Args:
            entity (thing): thing to create
        Returns:
            pot (thing): thing created
        """

        if entity.id in self.things:
            raise ThingAlreadyExistsException(
                f"Thing with id [{entity.id}] already exists"
            )

        # Set a new id
        entity.id = str(Ksuid())
        self.things[entity.id] = entity

        return entity

    async def get_list(
        self,
    ) -> List[Thing]:
        """Return a list of things

        Raises:
            ex: _description_

        Returns:
            List[Thing]: _description_
        """

        return list(self.things.values())

    async def get_by_id(self, id: str) -> Pot:
        """Gets thing by id

        Args:
            id: str

        Returns:
            Thing
        """

        if id not in self.things:
            logger.debug("Item with id: %s not found", id)
            raise ThingNotFoundException(f"Item with id: {id} not found")

        return self.things[id]

    async def delete(self, id: str) -> None:
        """Delete thing by id

        Args:
            request (Request): request (from fastAPI)
            id: str

        Returns:
            None
        """

        if id not in self.things:
            logger.debug("Item with id: %s not found", id)
            raise ThingNotFoundException(f"Item with id: {id} not found")

        del self.things[id]

    async def update(
        self,
        *,
        id: str,
        new_entity: Thing,
        # current_user: User
    ) -> Optional[Thing]:
        """UJpdate Thing

        Args:
            id (str): _description_
            new_entity (Thing): _description_

        Raises:
            ItemNotFoundException: _description_
            ex: _description_

        Returns:
            Optional[Thing]: _description_
        """

        if id not in self.things:
            logger.debug("Item with id: %s not found", id)
            raise ThingNotFoundException(f"Item with id: {id} not found")

        self.things[id] = new_entity

        return new_entity


things_repository = ThingRepositoryImpl()
