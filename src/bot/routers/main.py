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


from re import search

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto

from keyboards import Keyboards, InlineKeyboards, create_kb_services
from utils import texts, States

router = Router(name=__name__)


@router.message(States.MAIN, F.text == texts.main_kb_bt_1)
async def kb_bt_1(message: Message) -> None:
    await message.answer(text=texts.about)


@router.message(States.MAIN, F.text == texts.main_kb_bt_2)
async def kb_bt_2(message: Message) -> None:
    await message.answer_photo(
        photo=FSInputFile(path='static/images/services_1.png'),
        caption=texts.services_1,
        reply_markup=create_kb_services(),
    )

@router.callback_query(F.data.contains('services'))
async def kb_query(callback_query: CallbackQuery):
    service_index = int(search(r'services_(\d+)', str(callback_query.data)).group(1))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(path=f'static/images/services_{service_index+1}.png'),
            caption={
                0: texts.services_1,
                1: texts.services_2,
                2: texts.services_3,
                3: texts.services_4,
            }[service_index],
        reply_markup=create_kb_services(active_index=service_index)),
    )
    await callback_query.message.edit_caption(
        caption={
            0: texts.services_1,
            1: texts.services_2,
            2: texts.services_3,
            3: texts.services_4,
        }[service_index],
        reply_markup=create_kb_services(active_index=service_index)
    )


@router.message(Command('start', 'restart'))
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(States.MAIN)
    await message.answer_sticker(
        sticker=texts.welcome_sticker,
        reply_markup=Keyboards.MAIN,
    )
    await message.answer(
        text=texts.welcome,
        reply_markup=InlineKeyboards.MAIN,
    )
