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


from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.user import UserRepository
from database.repositories.utm import UtmRepository
from keyboards import Keyboards, InlineKeyboards
from utils import texts, States
from utils.funcs import extract_number_from_command


router = Router(name=__name__)


@router.message(States.MAIN, F.text == texts.main_kb_bt_1)
async def kb_bt_1(message: Message) -> None:
    await message.answer(text=texts.about)


@router.message(Command('start', 'restart'))
@db_session
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    tg_user_id = message.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    if not user:
        utm = None
        utm_id = extract_number_from_command(message.text)
        if utm_id:
            utm_repo = UtmRepository(session=session)
            utm = await utm_repo.get_by_id(id_=utm_id)

        await user_repo.create(
            obj_in={
                'tg_user_id': tg_user_id,
                'firstname': message.from_user.first_name,
                'lastname': message.from_user.last_name,
                'utm_id': utm.id if utm else None,
            },
        )

    await state.set_state(States.MAIN)
    await message.answer_sticker(
        sticker=texts.welcome_sticker,
        reply_markup=Keyboards.MAIN,
    )
    await message.answer(
        text=texts.welcome,
        reply_markup=InlineKeyboards.MAIN,
    )
