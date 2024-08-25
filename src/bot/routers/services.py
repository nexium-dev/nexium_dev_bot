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
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.user import UserRepository
from keyboards import create_kb_services
from routers.main import go_main
from utils import texts, States
from utils.bot import bot
from utils.funcs import extract_number_from_text_by_prefix


router = Router(name=__name__)


@router.callback_query(F.data == 'services')
@db_session
async def services(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback_query.answer()
    tg_user_id = callback_query.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    # Delete messages
    data = await state.get_data()
    for message_id in data['messages_to_delete']:
        await bot.delete_message(chat_id=tg_user_id, message_id=message_id)

    message = await bot.send_photo(
        chat_id=tg_user_id,
        photo=FSInputFile(path=f'static/images/{user.language}/services_1.png'),
        caption=texts[user.language].services_1,
        reply_markup=create_kb_services(language=user.language),
    )
    await state.set_state(States.SERVICES)
    await state.set_data({'messages_to_delete': [message.message_id]})



@router.callback_query(F.data.contains('services:'))
@db_session
async def kb_query(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.answer()

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': callback_query.from_user.id})

    service_index = extract_number_from_text_by_prefix(prefix='services', text=callback_query.data)
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(path=f'static/images/{user.language}/services_{service_index+1}.png'),
            caption={
                0: texts[user.language].services_1,
                1: texts[user.language].services_2,
                2: texts[user.language].services_3,
                3: texts[user.language].services_4,
            }[service_index],
        reply_markup=create_kb_services(active_index=service_index, language=user.language)),
    )
    await callback_query.message.edit_caption(
        caption={
            0: texts[user.language].services_1,
            1: texts[user.language].services_2,
            2: texts[user.language].services_3,
            3: texts[user.language].services_4,
        }[service_index],
        reply_markup=create_kb_services(active_index=service_index, language=user.language)
    )


@router.callback_query(States.SERVICES, F.data == 'back')
@db_session
async def kb_back(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.message.delete()

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': callback_query.from_user.id})

    await go_main(user=user, state=state)
