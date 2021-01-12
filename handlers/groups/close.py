import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.utils.exceptions import MessageToDeleteNotFound

from filters import GroupFilter
from loader import Game, dp
from utils.misc.game_process.service_defs import unmute_chat


@dp.message_handler(Command('close'), GroupFilter(), AdminFilter())
async def close1(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if not chat_obj:
        await message.delete()
        temp_message = await message.answer(f'⚠️ {message.from_user.get_mention()}, сначала нужно начать новую игру!')
        await asyncio.sleep(3)
        return await temp_message.delete()
    try:
        await dp.bot.delete_message(message.chat.id, chat_obj.register_message_id)
    except MessageToDeleteNotFound:
        pass
    await message.reply("⚠️ Игра успешно остановлена! Новый подбор можно начать с помощью команды /start")
    await unmute_chat(chat_obj)
    Game.remove_chat(chat_obj)


@dp.message_handler(Command('close'), GroupFilter())
async def close2(message: types.Message):
    await message.delete()
    temp_message = await message.answer(f"{message.from_user.get_mention()} эта команда "
                                        f"только для администраторов чата!")
    await asyncio.sleep(5)
    await temp_message.delete()

