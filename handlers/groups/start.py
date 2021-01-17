import asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import MessageToReplyNotFound

from data.game_models import Conv
from filters import GroupFilter

from keyboards.inline.start import start_join_kb
from loader import Game, bot, db, dp
from utils.misc.game_process.timer_to_start import timer_to_start_game


@dp.message_handler(CommandStart(), GroupFilter())
async def start(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if not chat_obj:
        chat = await db.get_chat(message.chat.id)
        if message.chat.username:
            await db.set_chat(message.chat.id, chat_title=message.chat.title, chat_username=message.chat.username)
        else:
            await db.set_chat(message.chat.id, chat_title=message.chat.title)

        register_message = await message.answer(
            f"📢 Регистрация открыта!\nДо конца регистрации: {chat.register_time} секунд 🕗!",
            reply_markup=start_join_kb(message.chat.id))
        print(f'начат подбор в беседе {message.chat.id} {message.chat.title}')

        Game.add_chat(Conv(chat_id=message.chat.id,
                           is_pin_register=chat.is_pin_register,
                           is_active_boosts=chat.is_active_boosts,
                           is_dead_talk=chat.is_dead_talk,
                           is_nonplayers_talk=chat.is_nonplayers_talk,
                           register_time=chat.register_time,
                           register_message_id=register_message.message_id,
                           night_time=chat.night_time,
                           day_time=chat.day_time,
                           vote_time=chat.vote_time,
                           accept_time=chat.accept_time,
                           is_show_dead_roles=chat.is_show_dead_roles,
                           is_show_day_votes=chat.is_show_day_votes,
                           is_allow_attachments_unmute=chat.is_allow_attachments_unmute))
        if chat.is_pin_register:
            await register_message.pin()

        return await timer_to_start_game(register_message, chat.register_time, message.chat.id)

    if chat_obj.phase == 'starting':
        # если регистрация, ответить, что идет регистрация
        try:
            return await bot.send_message(message.chat.id,
                                          f"❌ {message.from_user.get_mention()}, регистрация уже идёт!",
                                          reply_to_message_id=chat_obj.register_message_id)
        except MessageToReplyNotFound:
            return await message.answer(f"❌ {message.from_user.get_mention()}, регистрация уже идёт!")

    if chat_obj.phase in ['day', 'voting', 'voting1']:
        # если день, ответить, что игра идет
        await message.delete()
        temp_message = await message.answer(f"❌ {message.from_user.get_mention()}, игра уже идёт!")
        await asyncio.sleep(5)
        return await temp_message.delete()

    if chat_obj.phase == 'night':
        # если ночь, удалить
        return await message.delete()

