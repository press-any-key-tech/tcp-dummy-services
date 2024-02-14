from abc import ABCMeta, abstractmethod
from typing import Optional, List
from tcp_dummy_services.domain.entities import Thing


class ThingRepository(metaclass=ABCMeta):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Thing]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self) -> List[Thing]:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, *, entity: Thing) -> Optional[Thing]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, pot: Thing) -> Optional[Thing]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
