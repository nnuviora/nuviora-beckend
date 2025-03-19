from abc import ABC, abstractmethod
from typing import Any, Union
import uuid

from database import async_session_maker
from utils.logging import loggerObj


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def insert(self, data: dict) -> dict:
        pass
    
    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> dict:
        pass

    @abstractmethod
    async def get_all(self, *args: Any, **kwargs: Any) -> list[dict]:
        pass

    @abstractmethod
    async def update(self, id: Union[int, uuid.UUID], data: dict) -> dict:
        pass

    @abstractmethod
    async def delete(self, id: Union[int, uuid.UUID]) -> bool:
        pass


class SqlLayer(AbstractRepository):
    model = None

    async def insert(self, data: dict) -> dict:
        async with async_session_maker() as session:
            try:
                obj = self.model(**data)
                session.add(obj)
                await session.commit()
                loggerObj.info(f"Inserted new {self.model.__name__} ID {obj.id}")
                return obj
            except Exception as e:
                #raise Exception(f"Insert Error in {self.model.__class__.__name__}: {e}")
                loggerObj.error(f"Insert Error in {self.model.__name__}: {e}", exc_info=True)
                raise
            
    async def get(self, *args: Any, **kwargs: Any) -> dict:
        async with async_session_maker() as session:
            try:
                #pass
                obj = await session.get(self.model, kwargs.get("id"))
                loggerObj.debug(f"Fetched {self.model.__name__} with ID: {kwargs.get('id')}")
                return obj
            except Exception as e:
                raise Exception(f"Get Error in {self.model.__class__.__name__}: {e}")
            
    async def get_all(self, *args: Any, **kwatgs: Any) -> list[dict]:
        async with async_session_maker() as session:
            try:
                pass
            except Exception as e:
                raise Exception(f"Get-all Error in {self.model.__class__.__name__}: {e}")
            
    async def update(self, id: Union[int, uuid.UUID], data: dict) -> dict:
        async with async_session_maker() as session:
            try:
                pass
            except Exception as e:
                raise Exception(f"Update Error in {self.model.__class__.__name__}: {e}")
            
    async def delete(self, id: Union[int, uuid.UUID]) -> bool:
        async with async_session_maker() as session:
            try:
                pass
            except Exception as e:
                raise Exception(f"Delete Error in {self.model.__class__.__name__}: {e}")