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


from aiogram import Router
from aiogram.types import ChatMember, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.consultation import ConsultationRepository
from utils import texts


router = Router(name=__name__)


@router.chat_member()
@db_session
async def join(chat_member: ChatMemberUpdated, session: AsyncSession) -> None:
    print(chat_member.new_chat_member.status)
    if chat_member.new_chat_member.status == 'left':
        return

    tg_user_id = chat_member.from_user.id

    consultation_repo = ConsultationRepository(session=session)
    consultation = await consultation_repo.get_by(obj_in={'group_id': chat_member.chat.id})
    if not consultation:
        return

    if tg_user_id != consultation.user.tg_user_id:
        await chat_member.answer(
            text=texts.consultation_join.format(
                name=chat_member.from_user.first_name,
                tg_user_id=tg_user_id,
                category=consultation.category,
            ),
        )
