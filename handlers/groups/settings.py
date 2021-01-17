from asyncio import sleep

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.utils.exceptions import ChatNotFound, Unauthorized
from aiogram.utils.markdown import hbold

from data.db_models import Chat
from filters import GroupFilter
from keyboards.inline.settings import settings_kb_show_to_admin
from loader import dp, db


@dp.message_handler(Command('settings'), GroupFilter(), AdminFilter())
async def settings1(message: types.Message):
    await message.delete()
    chat_id = message.chat.id
    chat_data: Chat = await db.get_chat(chat_id)
    try:
        await dp.bot.send_message(message.from_user.id,
                                  f"Какие параметры беседы вы хотите поменять?\n\n"
                                  f"{hbold('🕗 Тайминги:')}\n"
                                  f"Регистрация: {chat_data.register_time}\n"
                                  f"Ночь: {chat_data.night_time}\n"
                                  f"День: {chat_data.day_time}\n"
                                  f"Голосование: {chat_data.vote_time}\n"
                                  f"Подтверждение: {chat_data.accept_time}\n\n"
                                  f"{hbold('🤬 Молчанка:')}\n"
                                  f"Изгнаные говорят: {'Да' if chat_data.is_dead_talk else 'Нет'}\n"
                                  f"Не играющие говорят: {'Да' if chat_data.is_nonplayers_talk else 'Нет'}\n\n"
                                  f"{hbold('💬 Остальное')}\n"
                                  f"Пин регистрации: {'Да' if chat_data.is_pin_register else 'Нет'}\n"
                                  f"Бустеры: {'Да' if chat_data.is_active_boosts else 'Нет'}\n"
                                  f"Показ ролей: {'Да' if chat_data.is_show_dead_roles else 'Нет'}\n"
                                  f"Тайное голосование: {'Да' if chat_data.is_show_day_votes else 'Нет'}\n"
                                  f"Приветственное сообщение: {'Да' if chat_data.is_show_hello_msg else 'Нет'}\n"
                                  f"Разрешать медиа при размуте: {'Да' if chat_data.is_allow_attachments_unmute else 'Нет'}",
                                  reply_markup=settings_kb_show_to_admin(chat_id))
    except ChatNotFound:
        temp_message = await message.reply(
            'Чтобы я отправил вам ответ на команду, перейдите в переписку со мной и нажмите кнопку '
            '"СТАРТ", затем пропишите команду снова.')
        await sleep(5)
        await temp_message.delete()
    except Unauthorized:
        temp_message = await message.reply(
            'Чтобы я отправил вам ответ на команду, перейдите в переписку со мной и разблокируйте меня,'
            ' затем пропишите команду снова.')
        await sleep(5)
        await temp_message.delete()


@dp.message_handler(Command('settings'), GroupFilter())
async def settings2(message: types.Message):
    await message.delete()
    await message.answer(f"{message.from_user.get_mention()} эта команда только для администраторов чата!")
