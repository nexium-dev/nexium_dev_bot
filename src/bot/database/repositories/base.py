#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from typing import TypeVar, Generic, Type, Optional, List

from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import BaseModel


ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by(self, obj_in: dict) -> Optional[ModelType]:
        conditions = [getattr(self.model, key) == value for key, value in obj_in.items()]
        query = select(self.model).where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj_in: dict) -> ModelType:
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id_: int, obj_in: dict) -> Optional[ModelType]:
        query = update(
            table=self.model,
        ).where(
            self.model.id == id_,
        ).values(
            **obj_in,
        ).execution_options(
            synchronize_session='fetch',
        )
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(id_)

    async def delete(self, id_: int) -> None:
        query = delete(
            table=self.model
        ).where(
            self.model.id == id_,
        ).execution_options(
            synchronize_session='fetch',
        )
        await self.session.execute(query)
        await self.session.commit()