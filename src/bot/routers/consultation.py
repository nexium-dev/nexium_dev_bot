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


from datetime import datetime
from io import BytesIO

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from pyrogram import Client
from pyrogram.types import ChatPrivileges
from pytz import timezone, UTC
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.consultation import ConsultationRepository
from database.repositories.user import UserRepository
from keyboards import create_kb_name, create_kb_consultation_services, create_kb_consultation_chat
from routers.main import go_main
from utils import texts, States
from utils.bot import bot
from utils.config import BOT_USERNAME, USER_ID, USER_HASH, ADMIN_USERNAME
from utils.funcs import extract_number_from_text_by_prefix
from utils.notification import create_admin_notification
from utils.photos import create_group_photo, create_invite_photo, create_client_photo


router = Router(name=__name__)


services = {
    1: texts.consultation_services_kb_bt_1,
    2: texts.consultation_services_kb_bt_2,
    3: texts.consultation_services_kb_bt_3,
    4: texts.consultation_services_kb_bt_4,
    5: texts.consultation_services_kb_bt_5,
    6: texts.consultation_services_kb_bt_6,
    7: texts.consultation_services_kb_bt_7,
    8: texts.consultation_services_kb_bt_8,
    9: texts.consultation_services_kb_bt_9,
}



async def set_name(tg_user_id: int, name: str, state: FSMContext):
    name = name.title()
    data = await state.get_data()
    data['name'] = name
    await state.set_data(
        data=data,
    )

    await bot.delete_message(chat_id=tg_user_id, message_id=data.get('name_message_id'))
    await bot.send_message(
        chat_id=tg_user_id,
        text=texts.consultation_2.format(name=name),
        reply_markup=create_kb_consultation_services(services=services),
    )


@router.callback_query(F.data == 'consultation')
async def start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    tg_user_id = callback_query.from_user.id

    data = await state.get_data()
    for message_id in data['messages_to_delete']:
        await bot.delete_message(chat_id=tg_user_id, message_id=message_id)

    await state.set_state(States.CONSULTATION)
    message = await bot.send_message(
        chat_id=tg_user_id,
        text=texts.consultation_1,
        reply_markup=create_kb_name(tg_firstname=callback_query.from_user.first_name),
    )
    await state.set_data(
        data={
            'name': None,
            'category': None,
            'name_message_id': message.message_id,
            'category_message_id': None,
        },
    )


@router.callback_query(States.CONSULTATION, F.data == 'consultation_name')
async def set_name_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    tg_user_id = callback_query.from_user.id

    await set_name(
        tg_user_id=tg_user_id,
        name=callback_query.from_user.first_name,
        state=state,
    )


@router.message(States.CONSULTATION)
async def set_name_message(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    if data['name']:
        return

    await set_name(
        tg_user_id=message.from_user.id,
        name=message.text,
        state=state,
    )


@router.callback_query(States.CONSULTATION, F.data.contains('consultation_category'))
@db_session
async def consultation_category_kb_query(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    tg_user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    category_index = extract_number_from_text_by_prefix(prefix='consultation_category', text=callback_query.data)
    data = await state.get_data()
    name = data['name']
    category = services[category_index]


    photos = await callback_query.from_user.get_profile_photos(limit=1)
    if len(photos.photos) == 0:
        client_photo = await create_client_photo(text=''.join([word[0] for word in name.split()][:2]))
    else:
        photo = photos.photos[0][-1]
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        client_photo = BytesIO(file_bytes.read())

    group_photo = await create_group_photo(client_photo=client_photo)
    invite_photo = await create_invite_photo(
        group_photo=group_photo,
        title=category[2:][:30] + "..." if len(category[2:]) > 32 else category[2:],
        time=datetime.now(timezone('Europe/Moscow')).strftime('%H:%M'),
    )
    group_photo.seek(0)
    invite_photo.seek(0)

    # Create group
    async with Client(
            name='manager',
            api_id=USER_ID,
            api_hash=USER_HASH,
            device_model='Manager Bot',
            app_version='v 1.0',
        ) as client:
        client: Client
        group = await client.create_supergroup(title=f'{category} / {name}')
        await client.add_chat_members(chat_id=group.id, user_ids=[BOT_USERNAME, ADMIN_USERNAME])
        [await client.promote_chat_member(
            chat_id=group.id,
            user_id=un,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_pin_messages=True,
            ),
        ) for un in [BOT_USERNAME, ADMIN_USERNAME]]
        if username:
            await client.add_chat_members(chat_id=group.id, user_ids=[username])

    await bot.set_chat_photo(chat_id=group.id, photo=BufferedInputFile(group_photo.read(), filename='group_photo.jpg'))
    await bot.send_message(chat_id=group.id, text=texts.consultation_group)
    invite_link = await bot.create_chat_invite_link(chat_id=group.id)
    group_url = invite_link.invite_link
    reply_markup = create_kb_consultation_chat(url=group_url)

    chat_member = await bot.get_chat_member(chat_id=group.id, user_id=callback_query.from_user.id)
    if chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.RESTRICTED, ChatMemberStatus.KICKED]:
        await bot.send_photo(
            chat_id=tg_user_id,
            photo=BufferedInputFile(invite_photo.read(), filename='invite_photo.jpg'),
            caption=texts.consultation_3_not_added,
            reply_markup=reply_markup,
        )
    else:
        await bot.send_photo(
            chat_id=tg_user_id,
            photo=BufferedInputFile(invite_photo.read(), filename='invite_photo.jpg'),
            caption=texts.consultation_3_added,
            reply_markup=reply_markup,
        )

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    consultation_repo = ConsultationRepository(session=session)
    await consultation_repo.create(
        obj_in={
            'user_id': user.id,
            'name': name,
            'category': category,
            'datetime': datetime.now(UTC),
            'group_id': group.id,
            'group_url': group_url,
        }
    )
    await create_admin_notification(
        text=texts.admin_notification_consultation.format(
            username=callback_query.from_user.username,
            tg_user_id=tg_user_id,
            name=name,
            category=category,
        ),
    )



@router.callback_query(F.data == 'back')
async def kb_back(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await go_main(tg_user_id=callback_query.from_user.id, state=state)
