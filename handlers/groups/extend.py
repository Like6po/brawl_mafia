import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter

from filters import GroupFilter
from loader import Game, dp


@dp.message_handler(Command('extend'), GroupFilter(), AdminFilter())
async def extend(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if chat_obj:
        if chat_obj.phase == 'starting':
            # флаг продлить регистрацию
            chat_obj.extend_time_register = True
            # отправить, что продлено
            await message.reply(f'📢 Время подбора продлено на {chat_obj.register_time // 2} секунд 🕗!')
        else:
            await message.delete()
            temp_message = await message.answer(f"❌ {message.from_user.get_mention()}, игра уже запущена!")
            await asyncio.sleep(3)
            await temp_message.delete()
    else:
        await message.delete()
        temp_message = await message.answer(f'⚠️ {message.from_user.get_mention()}, сначала нужно начать новую игру!')
        await asyncio.sleep(3)
        await temp_message.delete()


@dp.message_handler(Command('extend'), GroupFilter())
async def close2(message: types.Message):
    await message.delete()
    temp_message = await message.answer(f"{message.from_user.get_mention()} эта команда "
                                        f"только для администраторов чата!")
    await asyncio.sleep(5)
    await temp_message.delete()
