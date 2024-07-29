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


from yaml import safe_load
from pydantic import BaseModel


class Texts(BaseModel):
    welcome_message_sticker: str
    welcome_message: str
    welcome_message_kb_bt_1: str
    main_kb_bt_1: str
    main_kb_bt_2: str
    main_kb_bt_3: str
    main_kb_bt_4: str
    main_kb_bt_5: str
    main_kb_bt_6: str
    about: str


with open('texts.yaml', 'r', encoding='utf-8') as file:
    data = safe_load(file)


texts = Texts(**data)
