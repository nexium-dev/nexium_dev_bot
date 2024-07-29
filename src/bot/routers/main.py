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

from keyboards import Keyboards, InlineKeyboards
from utils import texts, States

router = Router(name=__name__)


@router.message(States.MAIN, F.text == texts.main_kb_bt_1)
async def main(message: Message) -> None:
    await message.answer(text=texts.about)


@router.message(Command('start', 'restart'))
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(States.MAIN)
    await message.answer_sticker(
        sticker=texts.welcome_message_sticker,
        reply_markup=Keyboards.MAIN,
    )
    await message.answer(
        text=texts.welcome_message,
        reply_markup=InlineKeyboards.MAIN,
    )
