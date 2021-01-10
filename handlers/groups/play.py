import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter

from filters import GroupFilter
from loader import Game, dp


@dp.message_handler(Command('play'), GroupFilter(), AdminFilter())
async def play1(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if chat_obj:
        chat_obj.register_is_end_ahead_of_time = True
    else:
        await message.delete()
        temp_message = await message.answer(f'⚠️ {message.from_user.get_mention()}, сначала нужно начать новую игру!')
        await asyncio.sleep(3)
        await temp_message.delete()


@dp.message_handler(Command('play'), GroupFilter())
async def play2(message: types.Message):
    await message.delete()
    temp_message = await message.answer(f"{message.from_user.get_mention()} эта команда"
                                        f" только для администраторов чата!")
    await asyncio.sleep(5)
    await temp_message.delete()
