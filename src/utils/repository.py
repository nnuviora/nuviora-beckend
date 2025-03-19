from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select

from database import async_session_maker


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
    async def update(self, data: dict, *args: Any, **kwargs: Any) -> dict:
        pass

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> bool:
        pass


class SqlLayer(AbstractRepository):
    model = None

    async def insert(self, data: dict) -> dict:
        async with async_session_maker() as session:
            try:
                stmt = self.model(**data)
                session.add(stmt)
                await session.commit()
                await session.refresh(stmt)
                return await stmt.to_dict()
            except Exception as e:
                await session.rollback()
                raise Exception(f"Insert Error in {self.model.__class__.__name__}: {e}")
            
    async def get(self, *args: Any, **kwargs: Any) -> dict:
        async with async_session_maker() as session:
            try:
                stmt = select(self.model).filter_by(**kwargs)
                res = await session.execute(stmt)
                obj = res.scalar_one_or_none()
                if obj is None:
                    return False
                return await obj.to_dict()
            except Exception as e:
                raise Exception(f"Get Error in {self.model.__class__.__name__}: {e}")
            
    async def get_all(self, *args: Any, **kwargs: Any) -> list[dict]:
        async with async_session_maker() as session:
            try:
                stmt = select(self.model).filter_by(**kwargs)
                res = await session.execute(stmt)
                return [await row.to_dict() for row in res.scalars().all() if row]
            except Exception as e:
                raise Exception(f"Get-all Error in {self.model.__class__.__name__}: {e}")
            
    async def update(self, data: dict, *args: Any, **kwargs: Any) -> dict:
        async with async_session_maker() as session:
            try:
                stmt = await session.execute(select(self.model).filter_by(**kwargs))
                res = stmt.scalar_one_or_none()

                if not res: 
                    return False
                
                for key, value in data.items():
                    setattr(res, key, value)
                
                await session.commit()
                await session.refresh(res)
                return res
            except Exception as e:
                await session.rollback()
                raise Exception(f"Update Error in {self.model.__class__.__name__}: {e}")
            
    async def delete(self, *args: Any, **kwargs: Any) -> bool:
        async with async_session_maker() as session:
            try:
                stmt = await session.execute(select(self.model).filter_by(**kwargs))
                res = stmt.scalar_one_or_none()

                if not res:
                    return False
                
                await session.delete(res)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                raise Exception(f"Delete Error in {self.model.__class__.__name__}: {e}")