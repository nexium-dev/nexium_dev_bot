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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton as Kb, InlineKeyboardMarkup, InlineKeyboardButton

from utils import texts


class Rkm(ReplyKeyboardMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, resize_keyboard=True)



class Keyboards:
    MAIN = Rkm(
        keyboard=[
            [Kb(text=texts.main_kb_bt_1)],
            [Kb(text=texts.main_kb_bt_2), Kb(text=texts.main_kb_bt_3)],
            [Kb(text=texts.main_kb_bt_4), Kb(text=texts.main_kb_bt_5)],
            [Kb(text=texts.main_kb_bt_6)],
        ],
    )

class InlineKeyboards:
    MAIN = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.welcome_message_kb_bt_1, url='https://nexium.me')],
        ]
    )
