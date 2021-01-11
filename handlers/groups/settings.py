from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter

from filters import GroupFilter
from keyboards.inline.settings import settings_kb_show_to_admin
from loader import dp


@dp.message_handler(Command('settings'), GroupFilter(), AdminFilter())
async def settings1(message: types.Message):
    await message.delete()
    await dp.bot.send_message(message.from_user.id,
                              "Какие параметры беседы вы хотите поменять?",
                              reply_markup=settings_kb_show_to_admin(message.chat.id))


@dp.message_handler(Command('settings'), GroupFilter())
async def settings2(message: types.Message):
    await message.delete()
    await message.answer(f"{message.from_user.get_mention()} эта команда только для администраторов чата!")
