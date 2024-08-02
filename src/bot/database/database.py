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


from functools import wraps
from typing import Callable


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from  database import models
from utils.config import DATABASE_URL


engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.get_base_model().metadata.create_all)


def db_session(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper
