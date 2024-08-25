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



def create_main_kb(language: str):
    return Rkm(
        keyboard=[
            [Kb(text=texts[language].main_kb_bt_2), Kb(text=texts[language].main_kb_bt_4)],
            [Kb(text=texts[language].bt_consultation)],
        ],
    )


def create_main_in_kb(language: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts[language].main_kb_bt_2, callback_data='services'),
                InlineKeyboardButton(text=texts[language].main_kb_bt_4, callback_data='contacts'),
            ],
            [InlineKeyboardButton(text=texts[language].bt_consultation, callback_data='consultation')],
        ]
    )

def create_consultation_in_kb(language: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts[language].bt_consultation, callback_data='consultation')],
            [InlineKeyboardButton(text=texts[language].bt_back, callback_data='contacts_back')],
        ]
    )


def create_kb_services(language: str, active_index=0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'{texts[language].services_kb_selected} {text}' if index == active_index else text,
                    callback_data='consultation' if text == texts[language].bt_consultation else f'services:{index}',
                )
            ]
            for index, text in enumerate(
                [
                    texts[language].services_kb_bt_1,
                    texts[language].services_kb_bt_2,
                    texts[language].services_kb_bt_3,
                    texts[language].services_kb_bt_4,
                    texts[language].bt_consultation,
                ],
            )
        ] +
        [
            [
                InlineKeyboardButton(
                    text=texts[language].bt_back,
                    callback_data='back',
                ),
            ],
        ]
    )


def create_kb_name(language: str, tg_firstname: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=tg_firstname,
                    callback_data='consultation_name',
                ),
            ],
            [
                InlineKeyboardButton(
                    text=texts[language].bt_back,
                    callback_data='back',
                ),
            ],
        ]
    )


def create_kb_consultation_services(language: str, services: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f'consultation_category:{index}',
                )
            ] for index, text in services.items()
        ] +
        [
            [
                InlineKeyboardButton(
                    text=texts[language].bt_back,
                    callback_data='back',
                ),
            ],
        ]
    )


def create_kb_consultation_chat(language: str, url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts[language].consultation_3_kb_bt_chat,
                    url=url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=texts[language].bt_back,
                    callback_data='back',
                ),
            ],
        ]
    )
