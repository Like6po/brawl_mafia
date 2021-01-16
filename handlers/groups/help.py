import asyncio

from aiogram import types

from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import ChatNotFound, Unauthorized

from filters import GroupFilter
from keyboards.inline.help import help_kb
from loader import dp


@dp.message_handler(Command('help'), GroupFilter())
async def help_group(message: types.Message):
    try:
        await dp.bot.send_message(message.from_user.id,
                                  'ℹ️ Здесь вы можете получить информацию с помощью кнопок!',
                                  reply_markup=help_kb())
    except ChatNotFound:
        temp_message = await message.reply(
            'Чтобы я отправил вам ответ на команду, перейдите в переписку со мной и нажмите кнопку '
            '"СТАРТ", затем пропишите команду снова.')
        await asyncio.sleep(5)
        await temp_message.delete()
    except Unauthorized:
        temp_message = await message.reply(
            'Чтобы я отправил вам ответ на команду, перейдите в переписку со мной и разблокируйте меня,'
            ' затем пропишите команду снова.')
        await asyncio.sleep(5)
        await temp_message.delete()
    await message.delete()
